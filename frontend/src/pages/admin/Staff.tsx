import { useEffect, useState } from 'react'
import { Plus, Edit, Trash2 } from 'lucide-react'
import { getStaff, createStaff, updateStaff, deleteStaff, getBranches } from '@/services/mock'
import toast from 'react-hot-toast'
import { User } from '@/types'
import { Branch } from '@/types'

export default function AdminStaff() {
  const [staff, setStaff] = useState<User[]>([])
  const [branches, setBranches] = useState<Branch[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingStaff, setEditingStaff] = useState<User | null>(null)
  const [formData, setFormData] = useState({ email: '', password: '', branch_id: '' })

  useEffect(() => {
    fetchStaff()
    fetchBranches()
  }, [])

  const fetchStaff = async () => {
    try {
      const data = await getStaff()
      setStaff(data)
    } catch (error) {
      toast.error('Failed to fetch staff')
    } finally {
      setLoading(false)
    }
  }

  const fetchBranches = async () => {
    try {
      const data = await getBranches()
      setBranches(data)
    } catch (error) {
      console.error('Failed to fetch branches')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const payload = {
        email: formData.email,
        password: formData.password,
        branch_id: formData.branch_id ? parseInt(formData.branch_id) : null,
        role: 'staff' as const
      }
      
      if (editingStaff) {
        await updateStaff(editingStaff.id, payload)
        toast.success('Staff updated successfully')
      } else {
        await createStaff(payload)
        toast.success('Staff created successfully')
      }
      setShowModal(false)
      setEditingStaff(null)
      setFormData({ email: '', password: '', branch_id: '' })
      fetchStaff()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Operation failed')
    }
  }

  const handleEdit = (staffMember: User) => {
    setEditingStaff(staffMember)
    setFormData({ email: staffMember.email, password: '', branch_id: staffMember.branch_id?.toString() || '' })
    setShowModal(true)
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this staff member?')) return
    try {
      await deleteStaff(id)
      toast.success('Staff deleted successfully')
      fetchStaff()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Delete failed')
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Staff Management</h1>
          <p className="text-gray-600 mt-2">Manage staff accounts</p>
        </div>
        <button
          onClick={() => {
            setEditingStaff(null)
            setFormData({ email: '', password: '', branch_id: '' })
            setShowModal(true)
          }}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus className="w-5 h-5" />
          Add Staff
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Email</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Branch</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {staff.map((staffMember) => (
              <tr key={staffMember.id}>
                <td className="px-6 py-4 whitespace-nowrap font-medium">{staffMember.email}</td>
                <td className="px-6 py-4">{staffMember.branch_id || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleEdit(staffMember)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <Edit className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(staffMember.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">
              {editingStaff ? 'Edit Staff' : 'Add Staff'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                  className="w-full px-4 py-2 border rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Password</label>
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required={!editingStaff}
                  className="w-full px-4 py-2 border rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Branch</label>
                <select
                  value={formData.branch_id}
                  onChange={(e) => setFormData({ ...formData, branch_id: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg"
                >
                  <option value="">Select Branch</option>
                  {branches.map((branch) => (
                    <option key={branch.id} value={branch.id}>
                      {branch.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false)
                    setEditingStaff(null)
                  }}
                  className="px-4 py-2 border rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {editingStaff ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

