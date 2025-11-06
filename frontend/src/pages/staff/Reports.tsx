import { useState } from 'react'
import { Download } from 'lucide-react'
// Using mock data, just show toasts and pretend download
import toast from 'react-hot-toast'

export default function StaffReports() {
  const [reportType, setReportType] = useState('sales')
  const [format, setFormat] = useState('json')
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const handleDownload = async () => {
    try {
      const params = new URLSearchParams()
      if (startDate) params.append('start_date', startDate)
      if (endDate) params.append('end_date', endDate)
      params.append('format', format)

      toast.success(format === 'csv' ? 'Report downloaded (mock)' : 'Report data loaded (mock)')
    } catch (error) {
      toast.error('Failed to generate report')
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Reports</h1>
        <p className="text-gray-600 mt-2">Generate branch reports</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Report Type</label>
            <select
              value={reportType}
              onChange={(e) => setReportType(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="sales">Sales Report</option>
              <option value="inventory">Inventory Report</option>
              <option value="customers">Customer Report</option>
            </select>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Start Date</label>
              <input
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2">End Date</label>
              <input
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                className="w-full px-4 py-2 border rounded-lg"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Format</label>
            <select
              value={format}
              onChange={(e) => setFormat(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
            >
              <option value="json">JSON</option>
              <option value="csv">CSV</option>
            </select>
          </div>

          <button
            onClick={handleDownload}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            <Download className="w-5 h-5" />
            {format === 'csv' ? 'Download Report' : 'View Report'}
          </button>
        </div>
      </div>
    </div>
  )
}

