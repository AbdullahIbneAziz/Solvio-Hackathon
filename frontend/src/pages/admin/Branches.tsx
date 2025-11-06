import { useEffect, useState } from 'react'
import { Plus, Edit, Trash2 } from 'lucide-react'
import { getBranches, createBranch, updateBranch, deleteBranch } from '@/services/mock'
import toast from 'react-hot-toast'
import { Branch } from '@/types'

export default function AdminBranches() {
  const [branches, setBranches] = useState<Branch[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingBranch, setEditingBranch] = useState<Branch | null>(null)
  const [formData, setFormData] = useState({ name: '', address: '' })

  useEffect(() => {
    fetchBranches()
  }, [])

  const fetchBranches = async () => {
    try {
      const data = await getBranches()
      setBranches(data)
    } catch (error) {
      toast.error('Failed to fetch branches')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingBranch) {
        await updateBranch(editingBranch.id, formData)
        toast.success('Branch updated successfully')
      } else {
        await createBranch(formData)
        toast.success('Branch created successfully')
      }
      setShowModal(false)
      setEditingBranch(null)
      setFormData({ name: '', address: '' })
      fetchBranches()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Operation failed')
    }
  }

  const handleEdit = (branch: Branch) => {
    setEditingBranch(branch)
    setFormData({ name: branch.name, address: branch.address || '' })
    setShowModal(true)
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this branch?')) return
    try {
      await deleteBranch(id)
      toast.success('Branch deleted successfully')
      fetchBranches()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Delete failed')
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Branches</h1>
          <p className="text-gray-600 mt-2">Manage your business branches</p>
        </div>
        <button
          onClick={() => {
            setEditingBranch(null)
            setFormData({ name: '', address: '' })
            setShowModal(true)
          }}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus className="w-5 h-5" />
          Add Branch
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Name</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Address</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {branches.map((branch) => (
              <tr key={branch.id}>
                <td className="px-6 py-4 whitespace-nowrap font-medium">{branch.name}</td>
                <td className="px-6 py-4">{branch.address || '-'}</td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex gap-2">
                    <button
                      onClick={() => handleEdit(branch)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <Edit className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(branch.id)}
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
              {editingBranch ? 'Edit Branch' : 'Add Branch'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Name</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  required
                  className="w-full px-4 py-2 border rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Address</label>
                <textarea
                  value={formData.address}
                  onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg"
                  rows={3}
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false)
                    setEditingBranch(null)
                  }}
                  className="px-4 py-2 border rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {editingBranch ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

