# SME Management System - Solvio Hackathon

A comprehensive multi-branch SME management system with AI-powered forecasting, featuring role-based access (Admin/Staff), inventory management, sales tracking, customer management, and intelligent insights.

## Features

### Admin Features
- Branch management (CRUD operations)
- Staff account management
- Product/warehouse management
- Aggregated dashboard with sales, inventory, and customer metrics
- AI-powered insights (demand forecasting, shortage detection)
- Comprehensive reports with CSV export

### Staff Features
- Branch-specific sales management
- Branch inventory management
- Customer management
- Branch dashboard with insights
- Branch-specific reports

### AI/ML Features
- Sales forecasting (ARIMA and simple moving average)
- Demand prediction for top products
- Inventory shortage detection and warnings
- Trend analysis

## Tech Stack

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- SQLite (PostgreSQL ready)
- JWT Authentication
- ARIMA forecasting (statsmodels)
- Pandas for data processing

**Frontend:**
- React + TypeScript
- Vite
- Tailwind CSS
- Recharts for data visualization
- React Router
- Axios for API calls

## Setup Instructions

### Backend

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
```

3. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the server:
```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Initial Setup

1. Register an admin account:
   - Use the `/api/auth/register` endpoint or create directly in the database
   - Example: POST to `/api/auth/register` with email and password

2. Login and start using the system!

## Project Structure

```
backend/
  app/
    api/          # API routes
    models/       # Database models
    schemas/      # Pydantic schemas
    services/     # Business logic
    ai/           # AI/ML modules
    utils/        # Utilities

frontend/
  src/
    components/   # Reusable components
    pages/        # Page components
    contexts/     # React contexts
    services/     # API clients
    types/        # TypeScript types
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login
- `POST /api/auth/register` - Register admin (initial setup)

### Admin Endpoints
- `GET /api/admin/dashboard` - Dashboard data
- `GET/POST/PUT/DELETE /api/admin/branches` - Branch management
- `GET/POST/PUT/DELETE /api/admin/staff` - Staff management
- `GET/POST/PUT/DELETE /api/admin/products` - Product management
- `GET /api/admin/reports/*` - Report generation
- `GET /api/admin/ai/*` - AI insights

### Staff Endpoints
- `GET /api/staff/dashboard` - Branch dashboard
- `GET/POST/PUT/DELETE /api/staff/sales` - Sales management
- `GET/POST/PUT/DELETE /api/staff/inventory` - Inventory management
- `GET/POST/PUT/DELETE /api/staff/customers` - Customer management
- `GET /api/staff/reports/*` - Branch reports
- `GET /api/staff/ai/*` - AI insights

## License

MIT License

