export interface User {
  id: number
  email: string
  role: 'admin' | 'staff'
  branch_id?: number
}

export interface Branch {
  id: number
  name: string
  address?: string
  created_at: string
}

export interface Product {
  id: number
  name: string
  description?: string
  category?: string
  unit_price: number
  created_at: string
}

export interface Inventory {
  id: number
  branch_id: number
  product_id: number
  quantity: number
  min_threshold: number
  updated_at: string
}

export interface Sale {
  id: number
  branch_id: number
  product_id: number
  customer_id?: number
  quantity: number
  total_price: number
  sale_date: string
  staff_id: number
  created_at: string
}

export interface Customer {
  id: number
  name: string
  email?: string
  phone?: string
  branch_id: number
  created_at: string
}

