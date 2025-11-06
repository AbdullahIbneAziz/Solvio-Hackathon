import { useEffect, useState } from 'react'
import { Plus, Edit } from 'lucide-react'
import { getInventory, createInventory, updateInventory, getProducts } from '@/services/mock'
import toast from 'react-hot-toast'
import { Inventory, Product } from '@/types'

export default function StaffInventory() {
  const [inventory, setInventory] = useState<Inventory[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [editingItem, setEditingItem] = useState<Inventory | null>(null)
  const [formData, setFormData] = useState({ product_id: '', quantity: '', min_threshold: '10' })

  useEffect(() => {
    fetchInventory()
    fetchProducts()
  }, [])

  const fetchInventory = async () => {
    try {
      const data = await getInventory()
      setInventory(data)
    } catch (error) {
      toast.error('Failed to fetch inventory')
    } finally {
      setLoading(false)
    }
  }

  const fetchProducts = async () => {
    try {
      const data = await getProducts()
      setProducts(data)
    } catch (error) {
      console.error('Failed to fetch products')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingItem) {
        await updateInventory(editingItem.id, {
          quantity: parseFloat(formData.quantity),
          min_threshold: parseFloat(formData.min_threshold)
        })
        toast.success('Inventory updated successfully')
      } else {
        await createInventory({
          branch_id: 1,
          product_id: parseInt(formData.product_id),
          quantity: parseFloat(formData.quantity),
          min_threshold: parseFloat(formData.min_threshold)
        })
        toast.success('Inventory item created successfully')
      }
      setShowModal(false)
      setEditingItem(null)
      setFormData({ product_id: '', quantity: '', min_threshold: '10' })
      fetchInventory()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Operation failed')
    }
  }

  const handleEdit = (item: Inventory) => {
    setEditingItem(item)
    setFormData({
      product_id: item.product_id.toString(),
      quantity: item.quantity.toString(),
      min_threshold: item.min_threshold.toString()
    })
    setShowModal(true)
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Inventory</h1>
          <p className="text-gray-600 mt-2">Manage branch inventory</p>
        </div>
        <button
          onClick={() => {
            setEditingItem(null)
            setFormData({ product_id: '', quantity: '', min_threshold: '10' })
            setShowModal(true)
          }}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus className="w-5 h-5" />
          Add Item
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Min Threshold</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {inventory.map((item) => {
              const isLowStock = item.quantity <= item.min_threshold
              return (
                <tr key={item.id} className={isLowStock ? 'bg-red-50' : ''}>
                  <td className="px-6 py-4 whitespace-nowrap font-medium">Product #{item.product_id}</td>
                  <td className="px-6 py-4">{item.quantity}</td>
                  <td className="px-6 py-4">{item.min_threshold}</td>
                  <td className="px-6 py-4">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      isLowStock ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                    }`}>
                      {isLowStock ? 'Low Stock' : 'OK'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <button
                      onClick={() => handleEdit(item)}
                      className="text-blue-600 hover:text-blue-800"
                    >
                      <Edit className="w-5 h-5" />
                    </button>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">
              {editingItem ? 'Update Inventory' : 'Add Inventory Item'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              {!editingItem && (
                <div>
                  <label className="block text-sm font-medium mb-2">Product</label>
                  <select
                    value={formData.product_id}
                    onChange={(e) => setFormData({ ...formData, product_id: e.target.value })}
                    required
                    className="w-full px-4 py-2 border rounded-lg"
                  >
                    <option value="">Select Product</option>
                    {products.map((product) => (
                      <option key={product.id} value={product.id}>
                        {product.name}
                      </option>
                    ))}
                  </select>
                </div>
              )}
              <div>
                <label className="block text-sm font-medium mb-2">Quantity</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.quantity}
                  onChange={(e) => setFormData({ ...formData, quantity: e.target.value })}
                  required
                  className="w-full px-4 py-2 border rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Min Threshold</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.min_threshold}
                  onChange={(e) => setFormData({ ...formData, min_threshold: e.target.value })}
                  required
                  className="w-full px-4 py-2 border rounded-lg"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => {
                    setShowModal(false)
                    setEditingItem(null)
                  }}
                  className="px-4 py-2 border rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  {editingItem ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

