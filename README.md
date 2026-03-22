# 📊 DMQL Project – E-commerce Data Modeling with PostgreSQL

---

## 📌 Project Objective

The goal of this project is to **design, implement, and populate** a well-structured relational database using a real-world e-commerce dataset.

We:

* Designed a **normalized schema (up to 3NF)**
* Created an **ERD (Entity Relationship Diagram)**
* Implemented the schema in **PostgreSQL (Neon Cloud)**
* Built a **Python data ingestion pipeline**
* Ensured **data integrity & idempotency**
* Applied **basic security (RBAC)**

---

## ⚙️ Tech Stack

* **Python** (Pandas, SQLAlchemy)
* **PostgreSQL** (Neon – Serverless DB)
* **GitHub** (Version Control)
* **SQL** (Schema + Queries)

---

## 🗂️ Project Structure

```
DMQL/
│
├── data/                     # Raw dataset (CSV files)
│
├── scripts/
│   ├── ingest_data.py       # Data loading pipeline
│   ├── run_schema.py        # Executes schema.sql
│
├── sql/
│   ├── schema.sql           # Database schema (tables + constraints)
│   ├── security.sql         # RBAC roles (analyst, app_user)
│
├── ERD.png                  # Entity Relationship Diagram
├── report.md                # 3NF justification report
├── README.md                # Project documentation
└── .gitignore               # Ignore sensitive files
```

---

## 🧠 Database Design

### ✔️ Key Entities

* Customers
* Orders
* Products
* Sellers
* Order Items (Bridge Table)
* Payments
* Reviews

### ✔️ Normalization

* Schema is designed up to **Third Normal Form (3NF)**
* Eliminates redundancy
* Ensures data consistency
* Uses **bridge table (order_items)** for many-to-many relationships

---

## 🚀 Step-by-Step Setup & Execution

Follow these steps to run the project from scratch:

---

### 🔹 Step 1: Clone Repository

```bash
git clone <your-repo-link>
cd DMQL
```

---

### 🔹 Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
```

---

### 🔹 Step 3: Install Dependencies

```bash
pip install pandas sqlalchemy psycopg2-binary python-dotenv
```

---

### 🔹 Step 4: Setup Environment Variables

Create a `.env` file in the root folder:

```env
DATABASE_URL=your_neon_database_url
```

⚠️ Make sure:

* Use **direct connection (not pooler)**
* Keep `.env` private (already in `.gitignore`)

---

### 🔹 Step 5: Create Database Schema

```bash
python scripts/run_schema.py
```

✔️ This will:

* Create all tables
* Apply constraints (PK, FK, NOT NULL, CHECK)

---

### 🔹 Step 6: Load Data into Database

```bash
python scripts/ingest_data.py
```

✔️ This will:

* Clean & transform data
* Handle missing values
* Insert data in correct order
* Avoid duplicates (idempotent)

---

### 🔹 Step 7: Verify Data in Neon

Go to Neon → Tables → Run queries like:

```sql
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM order_items;
```

---

## 🔐 Security (RBAC)

Roles implemented:

* **analyst**

  * Read-only access (SELECT)

* **app_user**

  * SELECT, INSERT, UPDATE access

To apply:

```sql
-- Run in Neon SQL Editor
\i sql/security.sql
```

---

## ⚡ Key Features

* ✔️ Fully normalized database (3NF)
* ✔️ Idempotent data ingestion
* ✔️ Foreign key integrity maintained
* ✔️ Clean schema design
* ✔️ Cloud-hosted PostgreSQL (Neon)
* ✔️ Role-based access control

---

## 📊 Sample Queries

```sql
-- Total orders
SELECT COUNT(*) FROM orders;

-- Order status distribution
SELECT order_status, COUNT(*) FROM orders GROUP BY order_status;

-- Total revenue
SELECT SUM(payment_value) FROM payments;
```

---

## 🎬 Demo Video

👉 *(Add your YouTube unlisted link here)*

---

## 📌 Conclusion

This project demonstrates:

* Real-world **data modeling**
* Practical **database design**
* Efficient **ETL pipeline creation**
* Cloud database deployment



