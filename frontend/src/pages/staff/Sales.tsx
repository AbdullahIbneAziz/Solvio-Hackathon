import { useEffect, useState } from 'react'
import { Plus } from 'lucide-react'
import { getSales, createSale, getProducts, getCustomers } from '@/services/mock'
import toast from 'react-hot-toast'
import { Sale, Product, Customer } from '@/types'

export default function StaffSales() {
  const [sales, setSales] = useState<Sale[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [formData, setFormData] = useState({ product_id: '', customer_id: '', quantity: '' })

  useEffect(() => {
    fetchSales()
    fetchProducts()
    fetchCustomers()
  }, [])

  const fetchSales = async () => {
    try {
      const data = await getSales()
      setSales(data)
    } catch (error) {
      toast.error('Failed to fetch sales')
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

  const fetchCustomers = async () => {
    try {
      const data = await getCustomers()
      setCustomers(data)
    } catch (error) {
      console.error('Failed to fetch customers')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await createSale({
        product_id: parseInt(formData.product_id),
        customer_id: formData.customer_id ? parseInt(formData.customer_id) : undefined,
        quantity: parseFloat(formData.quantity)
      })
      toast.success('Sale recorded successfully')
      setShowModal(false)
      setFormData({ product_id: '', customer_id: '', quantity: '' })
      fetchSales()
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Operation failed')
    }
  }

  if (loading) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Sales</h1>
          <p className="text-gray-600 mt-2">Record and manage sales</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
        >
          <Plus className="w-5 h-5" />
          Record Sale
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Product</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Quantity</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Total</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {sales.map((sale) => (
              <tr key={sale.id}>
                <td className="px-6 py-4 whitespace-nowrap">{sale.sale_date}</td>
                <td className="px-6 py-4">Product #{sale.product_id}</td>
                <td className="px-6 py-4">{sale.quantity}</td>
                <td className="px-6 py-4 font-medium">৳{sale.total_price.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Record Sale</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
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
                      {product.name} - ৳{product.unit_price}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Customer (Optional)</label>
                <select
                  value={formData.customer_id}
                  onChange={(e) => setFormData({ ...formData, customer_id: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg"
                >
                  <option value="">No Customer</option>
                  {customers.map((customer) => (
                    <option key={customer.id} value={customer.id}>
                      {customer.name}
                    </option>
                  ))}
                </select>
              </div>
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
              <div className="flex gap-2 justify-end">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 border rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Record
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

