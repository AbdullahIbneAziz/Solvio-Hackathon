import { useEffect, useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { TrendingUp, DollarSign, Package, Users, AlertTriangle } from 'lucide-react'
import { getAdminDashboard } from '../../services/mock'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function AdminDashboard() {
  const [dashboardData, setDashboardData] = useState<any>(null)
  const [aiInsights, setAiInsights] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
    fetchAIInsights()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const data = await getAdminDashboard()
      setDashboardData(data)
    } catch (error) {
      console.error('Failed to fetch dashboard data', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchAIInsights = async () => {
    try {
      const data = await getAdminDashboard()
      setAiInsights({ shortage_warnings: { current_low_stock: [], predicted_shortages: [] }, ...data })
    } catch (error) {
      console.error('Failed to fetch AI insights', error)
    }
  }

  if (loading) {
    return <div className="flex items-center justify-center h-64">Loading...</div>
  }

  const summary = dashboardData?.summary || {}
  const salesTrend = dashboardData?.sales_trend || []
  const topProducts = dashboardData?.top_products || []
  const shortages = aiInsights?.shortage_warnings || {}

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
        <p className="text-gray-600 mt-2">Overview of your business operations</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-sm font-medium">Total Sales (30d)</CardTitle>
            <DollarSign className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">৳{summary.total_sales?.toFixed(2) || '0.00'}</div>
            <p className="text-xs text-gray-500 mt-1">{summary.sales_count || 0} transactions</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-sm font-medium">Total Products</CardTitle>
            <Package className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{summary.total_products || 0}</div>
            <p className="text-xs text-gray-500 mt-1">In warehouse</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-sm font-medium">Total Customers</CardTitle>
            <Users className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{summary.total_customers || 0}</div>
            <p className="text-xs text-gray-500 mt-1">{summary.new_customers || 0} new this month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="text-sm font-medium">Low Stock Items</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{summary.low_stock_items || 0}</div>
            <p className="text-xs text-gray-500 mt-1">Requires attention</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Sales Trend (Last 7 Days)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={salesTrend}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="revenue" stroke="#3b82f6" name="Revenue (৳)" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Top Products by Revenue</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={topProducts.slice(0, 5)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="total_revenue" fill="#10b981" name="Revenue (৳)" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* AI Insights */}
      {shortages && (shortages.current_low_stock?.length > 0 || shortages.predicted_shortages?.length > 0) && (
        <Card className="border-red-200 bg-red-50">
          <CardHeader>
            <CardTitle className="text-red-800">AI Inventory Warnings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {shortages.current_low_stock?.map((item: any) => (
                <div key={item.inventory_id} className="flex items-center justify-between p-3 bg-white rounded">
                  <div>
                    <p className="font-medium">{item.product_name}</p>
                    <p className="text-sm text-gray-600">Current: {item.current_quantity} | Threshold: {item.min_threshold}</p>
                  </div>
                  <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">
                    {item.severity === 'critical' ? 'Critical' : 'Warning'}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

