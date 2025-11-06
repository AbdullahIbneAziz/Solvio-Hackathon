// Simple mock services and types for the standalone frontend
export type Branch = { id: number; name: string; address?: string; created_at?: string }
export type User = { id: number; email: string; role: 'admin' | 'staff'; branch_id?: number }
export type Product = { id: number; name: string; description?: string; category?: string; unit_price: number; created_at?: string }
export type Inventory = { id: number; branch_id: number; product_id: number; quantity: number; min_threshold: number; updated_at?: string }
export type Customer = { id: number; name: string; email?: string; phone?: string; branch_id: number; created_at?: string }
export type Sale = { id: number; branch_id: number; product_id: number; customer_id?: number; quantity: number; total_price: number; sale_date: string; staff_id: number; created_at?: string }

let branches: Branch[] = [
  { id: 1, name: 'Main Branch', address: 'Downtown', created_at: new Date().toISOString() },
]

let products: Product[] = [
  { id: 1, name: 'Rice 5kg', category: 'Grocery', unit_price: 8.99 },
  { id: 2, name: 'Milk 1L', category: 'Dairy', unit_price: 1.2 },
]

let inventories: Inventory[] = [
  { id: 1, branch_id: 1, product_id: 1, quantity: 120, min_threshold: 20 },
  { id: 2, branch_id: 1, product_id: 2, quantity: 30, min_threshold: 15 },
]

let customers: Customer[] = [
  { id: 1, name: 'John Doe', email: 'john@example.com', phone: '0123456789', branch_id: 1 },
]

let sales: Sale[] = [
  { id: 1, branch_id: 1, product_id: 1, customer_id: 1, quantity: 2, total_price: 17.98, sale_date: new Date().toISOString().slice(0,10), staff_id: 1 },
]

let users: User[] = [
  { id: 1, email: 'admin@mail.com', role: 'admin' },
  { id: 2, email: 'staff@mail.com', role: 'staff', branch_id: 1 },
]

// Auth mocks
export async function mockLogin(email: string, password: string) {
  const user = users.find(u => u.email === email)
  if (!user) throw new Error('Incorrect email or password')
  return { user, access_token: 'mock', refresh_token: 'mock' }
}

// Admin mocks
export async function getBranches() { return branches }
export async function createBranch(data: Omit<Branch, 'id'>) {
  const id = Math.max(0, ...branches.map(b=>b.id)) + 1
  const br = { id, ...data }
  branches.push(br)
  return br
}
export async function updateBranch(id: number, data: Partial<Branch>) {
  branches = branches.map(b => b.id===id ? { ...b, ...data } : b)
  return branches.find(b=>b.id===id)!
}
export async function deleteBranch(id: number) { branches = branches.filter(b=>b.id!==id) }

export async function getStaff() { return users.filter(u=>u.role==='staff') }
export async function createStaff(data: { email: string; password: string; branch_id?: number }) {
  const id = Math.max(0, ...users.map(u=>u.id)) + 1
  const user: User = { id, email: data.email, role: 'staff', branch_id: data.branch_id }
  users.push(user)
  return user
}
export async function updateStaff(id: number, data: Partial<User> & { password?: string }) {
  users = users.map(u => u.id===id ? { ...u, ...data } : u)
  return users.find(u=>u.id===id)!
}
export async function deleteStaff(id: number) { users = users.filter(u=>u.id!==id) }

export async function getProducts() { return products }
export async function createProduct(data: Omit<Product, 'id'>) {
  const id = Math.max(0, ...products.map(p=>p.id)) + 1
  const pr = { id, ...data }
  products.push(pr)
  return pr
}
export async function updateProduct(id: number, data: Partial<Product>) {
  products = products.map(p => p.id===id ? { ...p, ...data } : p)
  return products.find(p=>p.id===id)!
}
export async function deleteProduct(id: number) { products = products.filter(p=>p.id!==id) }

// Staff mocks
export async function getInventory() { return inventories }
export async function createInventory(data: Omit<Inventory, 'id'>) {
  const id = Math.max(0, ...inventories.map(i=>i.id)) + 1
  const it = { id, ...data }
  inventories.push(it)
  return it
}
export async function updateInventory(id: number, data: Partial<Inventory>) {
  inventories = inventories.map(i=>i.id===id ? { ...i, ...data } : i)
  return inventories.find(i=>i.id===id)!
}
export async function deleteInventory(id: number) { inventories = inventories.filter(i=>i.id!==id) }

export async function getCustomers() { return customers }
export async function createCustomer(data: Omit<Customer, 'id'>) {
  const id = Math.max(0, ...customers.map(c=>c.id)) + 1
  const cu = { id, ...data }
  customers.push(cu)
  return cu
}
export async function updateCustomer(id: number, data: Partial<Customer>) {
  customers = customers.map(c=>c.id===id ? { ...c, ...data } : c)
  return customers.find(c=>c.id===id)!
}
export async function deleteCustomer(id: number) { customers = customers.filter(c=>c.id!==id) }

export async function getSales() { return sales }
export async function createSale(data: { product_id: number; customer_id?: number; quantity: number }) {
  const product = products.find(p=>p.id===data.product_id)!
  const id = Math.max(0, ...sales.map(s=>s.id)) + 1
  const total_price = product.unit_price * data.quantity
  const sale: Sale = { id, branch_id: 1, product_id: data.product_id, customer_id: data.customer_id, quantity: data.quantity, total_price, sale_date: new Date().toISOString().slice(0,10), staff_id: 2 }
  sales.push(sale)
  const inv = inventories.find(i=>i.product_id===data.product_id && i.branch_id===1)
  if (inv) inv.quantity = Math.max(0, inv.quantity - data.quantity)
  return sale
}

export async function getAdminDashboard() {
  const total_revenue = sales.reduce((a,s)=>a+s.total_price, 0)
  const sales_count = sales.length
  const low_stock_items = inventories.filter(i=>i.quantity<=i.min_threshold).length
  const total_customers = customers.length
  const new_customers = customers.length
  const top_products = products.map(p=>({ name: p.name, total_revenue: sales.filter(s=>s.product_id===p.id).reduce((a,s)=>a+s.total_price,0), total_quantity: sales.filter(s=>s.product_id===p.id).reduce((a,s)=>a+s.quantity,0) })).sort((a,b)=>b.total_revenue-a.total_revenue).slice(0,5)
  const sales_trend = sales.slice(-7).map(s=>({ date: s.sale_date, revenue: s.total_price, count: 1 }))
  return { summary: { total_sales: total_revenue, sales_count, recent_sales: total_revenue, total_products: products.length, low_stock_items, total_customers, new_customers }, top_products, sales_trend }
}

export const getStaffDashboard = getAdminDashboard


