# Commercial Cloth Store — Backend API

Python **FastAPI** backend for a commercial clothing e-commerce site, backed by **MySQL**, with rotating **log files** for application activity and exceptions.

## Features

- REST API for **categories**, **products**, **customers**, and **orders**
- MySQL via SQLAlchemy + PyMySQL
- Single rotating log file: `logs/cloth_store.log` (app activity and exceptions)
- Global exception handlers (validation, HTTP, database, unhandled)
- Order placement with stock validation and automatic totals

## Project structure

```
python-cloth/
├── app/
│   ├── main.py              # FastAPI app + exception handlers
│   ├── config.py            # Settings from .env
│   ├── database.py          # MySQL connection
│   ├── logging_config.py    # Log file setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic request/response schemas
│   ├── routers/             # API endpoints
│   └── services/            # Business logic (orders)
├── logs/                    # Generated log files
├── scripts/
│   ├── cloth_store.sql      # Full schema + sample data
│   ├── init_database.sql    # Database creation only
│   └── seed_data.py         # Sample products
├── run.py
├── requirements.txt
└── .env.example
```

## Setup

### 1. Prerequisites

- Python 3.11+
- MySQL 8.0+

### 2. Create MySQL database

**Full schema + sample data** (recommended):

```bash
mysql -u root -p < scripts/cloth_store.sql
```

**Database only** (tables created by the API on startup):

```bash
mysql -u root -p < scripts/init_database.sql
```

### 3. Install dependencies

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
```

### 4. Configure environment

Copy `.env.example` to `.env` and set your MySQL credentials:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=cloth_store
```

### 5. Run the API

```bash
python run.py
```

API docs: http://localhost:8000/docs

### 6. Seed sample data (optional)

```bash
python scripts/seed_data.py
```

## API endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET/POST | `/api/v1/categories` | List / create categories |
| GET/PUT/DELETE | `/api/v1/categories/{id}` | Category CRUD |
| GET/POST | `/api/v1/products` | List / create products |
| GET/PUT/DELETE | `/api/v1/products/{id}` | Product CRUD |
| GET/POST | `/api/v1/customers` | List / create customers |
| GET/PUT | `/api/v1/customers/{id}` | Customer read/update |
| GET/POST | `/api/v1/orders` | List / place orders |
| GET | `/api/v1/orders/{id}` | Order details |
| PATCH | `/api/v1/orders/{id}/status?status_value=shipped` | Update order status |

## Logging

All logs (INFO, WARNING, ERROR, exceptions with stack traces) are written to **`logs/cloth_store.log`**.

Logs rotate at 5 MB with 5 backup files. Set `LOG_LEVEL` in `.env` (DEBUG, INFO, WARNING, ERROR).

## Example: place an order

```bash
# 1. Create customer
curl -X POST http://localhost:8000/api/v1/customers \
  -H "Content-Type: application/json" \
  -d "{\"full_name\":\"Jane Doe\",\"email\":\"jane@example.com\",\"address\":\"123 Main St\"}"

# 2. Place order (use customer_id and product_id from DB)
curl -X POST http://localhost:8000/api/v1/orders \
  -H "Content-Type: application/json" \
  -d "{\"customer_id\":1,\"items\":[{\"product_id\":1,\"quantity\":2}],\"shipping_address\":\"123 Main St\"}"
```

## License

MIT
