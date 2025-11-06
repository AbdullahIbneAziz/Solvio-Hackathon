import { Outlet, Link, useLocation } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { LayoutDashboard, ShoppingCart, Package, Users, FileText, LogOut, Bot } from 'lucide-react'
import toast from 'react-hot-toast'

const navItems = [
  { path: '/staff/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/staff/sales', label: 'Sales', icon: ShoppingCart },
  { path: '/staff/inventory', label: 'Inventory', icon: Package },
  { path: '/staff/customers', label: 'Customers', icon: Users },
  { path: '/staff/reports', label: 'Reports', icon: FileText },
  { path: '/staff/ai-assistant', label: 'AI Assistant', icon: Bot },
]

export default function StaffLayout() {
  const { logout, user } = useAuth()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 bg-white border-r min-h-screen">
          <div className="p-6 border-b">
            <h1 className="text-xl font-bold text-blue-600">SME Management</h1>
            <p className="text-sm text-gray-500 mt-1">Staff Panel</p>
          </div>
          
          <nav className="p-4">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition ${
                    isActive
                      ? 'bg-blue-50 text-blue-600 font-medium'
                      : 'text-gray-700 hover:bg-gray-50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  {item.label}
                </Link>
              )
            })}
          </nav>

          <div className="absolute bottom-0 w-64 p-4 border-t">
            <div className="mb-4 px-4">
              <p className="text-sm font-medium text-gray-900">{user?.email}</p>
              <p className="text-xs text-gray-500">Staff Member</p>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-3 w-full px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition"
            >
              <LogOut className="w-5 h-5" />
              Logout
            </button>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

