import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/Card'
import { TrendingUp, Package, Users, MessageSquare, Send } from 'lucide-react'
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function AIAssistant() {
  const [activeTab, setActiveTab] = useState<'sales' | 'demand' | 'engagement' | 'chatbot'>('sales')
  const [chatMessage, setChatMessage] = useState('')
  const [chatHistory, setChatHistory] = useState<Array<{ role: 'user' | 'assistant'; message: string }>>([
    { role: 'assistant', message: 'Hello! I\'m your AI assistant. How can I help you with your branch operations?' }
  ])

  // Mock data for sales forecasting
  const salesForecast = [
    { date: '2025-11-01', predicted: 800, actual: 750 },
    { date: '2025-11-02', predicted: 900, actual: 880 },
    { date: '2025-11-03', predicted: 1000, actual: null },
    { date: '2025-11-04', predicted: 950, actual: null },
    { date: '2025-11-05', predicted: 1100, actual: null },
    { date: '2025-11-06', predicted: 1050, actual: null },
    { date: '2025-11-07', predicted: 1200, actual: null },
  ]

  // Mock data for demand forecasting
  const demandForecast = [
    { product: 'Rice 5kg', current_demand: 30, predicted_demand: 35, trend: 'increasing' },
    { product: 'Milk 1L', current_demand: 20, predicted_demand: 25, trend: 'increasing' },
    { product: 'Bread', current_demand: 15, predicted_demand: 18, trend: 'stable' },
  ]

  // Mock customer engagement data
  const customerEngagement = [
    { customer: 'John Doe', last_purchase: '2025-11-01', total_purchases: 10, engagement_score: 80 },
    { customer: 'Jane Smith', last_purchase: '2025-10-28', total_purchases: 5, engagement_score: 60 },
  ]

  const handleSendMessage = () => {
    if (!chatMessage.trim()) return

    setChatHistory(prev => [...prev, { role: 'user', message: chatMessage }])

    const responses = [
      "For your branch, I recommend focusing on restocking high-demand items.",
      "Your sales trend looks positive. Keep up the good customer service!",
      "Consider reaching out to customers who haven't purchased recently.",
      "I can help you with inventory management, sales predictions, and customer insights.",
    ]
    const randomResponse = responses[Math.floor(Math.random() * responses.length)]

    setTimeout(() => {
      setChatHistory(prev => [...prev, { role: 'assistant', message: randomResponse }])
    }, 500)

    setChatMessage('')
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">AI Assistant</h1>
        <p className="text-gray-600 mt-2">Get intelligent insights for your branch operations</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b">
        <button
          onClick={() => setActiveTab('sales')}
          className={`px-4 py-2 font-medium transition ${
            activeTab === 'sales'
              ? 'border-b-2 border-blue-600 text-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <TrendingUp className="w-4 h-4 inline mr-2" />
          Sales Forecasting
        </button>
        <button
          onClick={() => setActiveTab('demand')}
          className={`px-4 py-2 font-medium transition ${
            activeTab === 'demand'
              ? 'border-b-2 border-blue-600 text-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Package className="w-4 h-4 inline mr-2" />
          Demand Forecasting
        </button>
        <button
          onClick={() => setActiveTab('engagement')}
          className={`px-4 py-2 font-medium transition ${
            activeTab === 'engagement'
              ? 'border-b-2 border-blue-600 text-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <Users className="w-4 h-4 inline mr-2" />
          Customer Engagement
        </button>
        <button
          onClick={() => setActiveTab('chatbot')}
          className={`px-4 py-2 font-medium transition ${
            activeTab === 'chatbot'
              ? 'border-b-2 border-blue-600 text-blue-600'
              : 'text-gray-600 hover:text-gray-900'
          }`}
        >
          <MessageSquare className="w-4 h-4 inline mr-2" />
          AI Chatbot
        </button>
      </div>

      {/* Sales Forecasting */}
      {activeTab === 'sales' && (
        <Card>
          <CardHeader>
            <CardTitle>Branch Sales Forecasting (Next 7 Days)</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={salesForecast}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="predicted" stroke="#3b82f6" name="Predicted Sales (৳)" strokeWidth={2} />
                <Line type="monotone" dataKey="actual" stroke="#10b981" name="Actual Sales (৳)" strokeWidth={2} strokeDasharray="5 5" />
              </LineChart>
            </ResponsiveContainer>
            <div className="mt-4 p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold text-blue-900 mb-2">AI Insights</h3>
              <p className="text-blue-800">
                Your branch sales are predicted to increase by 12% over the next week. 
                Peak sales expected on Day 7 with estimated revenue of ৳1,200.
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Demand Forecasting */}
      {activeTab === 'demand' && (
        <div className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Product Demand Forecasting</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {demandForecast.map((item, idx) => (
                  <div key={idx} className="p-4 border rounded-lg">
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-semibold">{item.product}</h3>
                      <span className={`px-3 py-1 rounded-full text-sm ${
                        item.trend === 'increasing' ? 'bg-green-100 text-green-800' :
                        item.trend === 'decreasing' ? 'bg-red-100 text-red-800' :
                        'bg-gray-100 text-gray-800'
                      }`}>
                        {item.trend}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-4 mt-2">
                      <div>
                        <p className="text-sm text-gray-600">Current Demand</p>
                        <p className="text-lg font-semibold">{item.current_demand} units/day</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Predicted Demand</p>
                        <p className="text-lg font-semibold text-blue-600">{item.predicted_demand} units/day</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-4 p-4 bg-green-50 rounded-lg">
                <h3 className="font-semibold text-green-900 mb-2">Recommendations</h3>
                <ul className="list-disc list-inside text-green-800 space-y-1">
                  <li>Restock Rice 5kg - high demand expected</li>
                  <li>Monitor Milk 1L inventory levels</li>
                </ul>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Customer Engagement */}
      {activeTab === 'engagement' && (
        <Card>
          <CardHeader>
            <CardTitle>Customer Engagement Analysis</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {customerEngagement.map((customer, idx) => (
                <div key={idx} className="p-4 border rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold">{customer.customer}</h3>
                    <div className="flex items-center gap-2">
                      <div className="w-32 bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            customer.engagement_score >= 70 ? 'bg-green-500' :
                            customer.engagement_score >= 50 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${customer.engagement_score}%` }}
                        />
                      </div>
                      <span className="font-semibold">{customer.engagement_score}%</span>
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-4 mt-2 text-sm">
                    <div>
                      <p className="text-gray-600">Last Purchase</p>
                      <p className="font-medium">{customer.last_purchase}</p>
                    </div>
                    <div>
                      <p className="text-gray-600">Total Purchases</p>
                      <p className="font-medium">{customer.total_purchases}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-4 p-4 bg-purple-50 rounded-lg">
              <h3 className="font-semibold text-purple-900 mb-2">Engagement Insights</h3>
              <p className="text-purple-800">
                Focus on maintaining relationships with high-engagement customers. 
                Consider re-engagement campaigns for customers with lower scores.
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* AI Chatbot */}
      {activeTab === 'chatbot' && (
        <Card className="h-[600px] flex flex-col">
          <CardHeader>
            <CardTitle>AI Assistant Chatbot</CardTitle>
          </CardHeader>
          <CardContent className="flex-1 flex flex-col">
            <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-4 bg-gray-50 rounded-lg">
              {chatHistory.map((chat, idx) => (
                <div
                  key={idx}
                  className={`flex ${chat.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      chat.role === 'user'
                        ? 'bg-blue-600 text-white'
                        : 'bg-white border text-gray-800'
                    }`}
                  >
                    <p>{chat.message}</p>
                  </div>
                </div>
              ))}
            </div>
            <div className="flex gap-2">
              <input
                type="text"
                value={chatMessage}
                onChange={(e) => setChatMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask me anything about your branch..."
                className="flex-1 px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                onClick={handleSendMessage}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 flex items-center gap-2"
              >
                <Send className="w-5 h-5" />
                Send
              </button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

