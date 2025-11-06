import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AuthProvider } from './contexts/AuthContext'
import LoginPage from './pages/LoginPage'
import AdminLayout from './layouts/AdminLayout'
import StaffLayout from './layouts/StaffLayout'
import AdminDashboard from './pages/admin/Dashboard'
import AdminBranches from './pages/admin/Branches'
import AdminStaff from './pages/admin/Staff'
import AdminProducts from './pages/admin/Products'
import AdminReports from './pages/admin/Reports'
import AdminAIAssistant from './pages/admin/AIAssistant'
import StaffDashboard from './pages/staff/Dashboard'
import StaffAIAssistant from './pages/staff/AIAssistant'
import StaffSales from './pages/staff/Sales'
import StaffInventory from './pages/staff/Inventory'
import StaffCustomers from './pages/staff/Customers'
import StaffReports from './pages/staff/Reports'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <AuthProvider>
      <Router>
        <Toaster position="top-right" />
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/admin/*"
            element={
              <ProtectedRoute requiredRole="admin">
                <AdminLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard" element={<AdminDashboard />} />
            <Route path="branches" element={<AdminBranches />} />
            <Route path="staff" element={<AdminStaff />} />
            <Route path="products" element={<AdminProducts />} />
            <Route path="reports" element={<AdminReports />} />
            <Route path="ai-assistant" element={<AdminAIAssistant />} />
          </Route>
          <Route
            path="/staff/*"
            element={
              <ProtectedRoute requiredRole="staff">
                <StaffLayout />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="dashboard" replace />} />
            <Route path="dashboard" element={<StaffDashboard />} />
            <Route path="sales" element={<StaffSales />} />
            <Route path="inventory" element={<StaffInventory />} />
            <Route path="customers" element={<StaffCustomers />} />
            <Route path="reports" element={<StaffReports />} />
            <Route path="ai-assistant" element={<StaffAIAssistant />} />
          </Route>
          <Route path="/" element={<Navigate to="/login" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  )
}

export default App

