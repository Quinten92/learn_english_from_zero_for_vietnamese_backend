# 🗄️ Database Configuration Guide

## Tổng quan

Project sử dụng **2 cách kết nối** đến Supabase PostgreSQL:

| Cách | Tool | Biến môi trường | Mục đích |
|------|------|-----------------|----------|
| **1. Direct PostgreSQL** | SQLAlchemy + Alembic | `DATABASE_URL` | Tạo/migrate tables (DDL) |
| **2. Supabase Client API** | supabase-py | `SUPABASE_URL` + `SUPABASE_KEY` | CRUD data trong app (DML) |

---

## 🔐 Tại sao cần cả 2?

### DATABASE_URL (Password) - Cho Alembic
```
✅ Cần quyền DDL: CREATE TABLE, ALTER TABLE, DROP TABLE
✅ Chạy migrations (1 lần khi deploy)
❌ Bypass Row Level Security (RLS)
❌ Không nên dùng cho runtime queries
```

### SUPABASE_KEY (Anon Key) - Cho App Runtime
```
✅ Row Level Security (RLS) bảo vệ data
✅ Chỉ access data được phép theo policy
✅ Có rate limiting & audit log
✅ An toàn cho client-side (nếu cần)
❌ Không thể tạo/sửa schema
```

---

## 📋 Environment Variables

### File `.env` (Local Development)

```env
# ===========================================
# SUPABASE CONFIGURATION
# ===========================================

# 1. Supabase Client API (cho app runtime - CRUD data)
# Lấy từ: Supabase Dashboard → Project Settings → API → anon public
SUPABASE_URL=https://mgztjcjelknkpwlipqxi.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# 2. Direct PostgreSQL (cho Alembic migrations)
# Lấy từ: Supabase Dashboard → Project Settings → Database → Connection string
# ⚠️ Password có ký tự đặc biệt cần URL encode:
#    . → %2E
#    * → %2A
#    @ → %40
#    # → %23
DATABASE_URL=postgresql://postgres.mgztjcjelknkpwlipqxi:YieJ%2E2x%2E%2A4q7mWv@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres

# ===========================================
# APP CONFIGURATION
# ===========================================
DEBUG=true
```

### Railway Variables (Production)

Thêm vào Railway Dashboard → Service → Variables:

| Key | Value | Mô tả |
|-----|-------|-------|
| `SUPABASE_URL` | `https://mgztjcjelknkpwlipqxi.supabase.co` | Supabase project URL |
| `SUPABASE_KEY` | `eyJ...` | Anon public key |
| `DATABASE_URL` | `postgresql://...` | Direct PostgreSQL connection |

---

## 🔧 Cách lấy credentials từ Supabase

### 1. SUPABASE_URL & SUPABASE_KEY

1. Vào https://supabase.com/dashboard
2. Chọn project **"learnenglishzero-stg"**
3. Click **Project Settings** (⚙️) → **API**
4. Copy:
   - **Project URL** → `SUPABASE_URL`
   - **anon public** key → `SUPABASE_KEY`

### 2. DATABASE_URL

1. Vào https://supabase.com/dashboard
2. Chọn project **"learnenglishzero-stg"**
3. Click **Project Settings** (⚙️) → **Database**
4. Mục **Connection string** → Tab **URI**
5. Copy và thay `[YOUR-PASSWORD]` bằng password thực

**Format:**
```
postgresql://postgres.[project-ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres
```

---

## 🚀 Workflow sử dụng

### Khi phát triển (Local)

```bash
# 1. Sửa models trong app/models/
# 2. Tạo migration (dùng DATABASE_URL)
alembic revision --autogenerate -m "add new table"

# 3. Apply migration (dùng DATABASE_URL)
alembic upgrade head

# 4. Chạy app (dùng SUPABASE_KEY cho queries)
uvicorn app.main:app --reload
```

### Khi deploy (Production)

```bash
# 1. Push code → Railway auto deploy
git push origin main

# 2. Chạy migration trên production (1 lần)
# Railway → Service → Settings → Custom Start Command
# Hoặc chạy manual qua Railway CLI
alembic upgrade head
```

---

## 📁 Files liên quan

```
learn_english_from_zero_for_vietnamese_backend/
├── .env                    # Local environment (git ignored)
├── .env.example            # Template cho team
├── app/
│   ├── config.py           # Load settings từ env vars
│   ├── database.py         # Supabase client (dùng KEY)
│   └── models/             # SQLAlchemy models (dùng DATABASE_URL)
├── alembic/
│   └── env.py              # Alembic config (dùng DATABASE_URL)
└── alembic.ini             # Alembic settings
```

---

## ⚠️ Lưu ý bảo mật

1. **KHÔNG commit `.env`** vào git (đã có trong .gitignore)
2. **KHÔNG dùng `service_role` key** - chỉ dùng `anon` key
3. **URL encode password** nếu có ký tự đặc biệt
4. **Rotate credentials** định kỳ trong production

---

## 🆘 Troubleshooting

| Lỗi | Nguyên nhân | Fix |
|-----|-------------|-----|
| `Could not parse SQLAlchemy URL` | Password chưa encode | Encode ký tự đặc biệt |
| `password authentication failed` | Sai password | Kiểm tra lại password |
| `connection refused` | Sai host/port | Kiểm tra connection string |
| `permission denied` | Dùng anon key cho DDL | Dùng DATABASE_URL |
| `relation does not exist` | Chưa chạy migration | `alembic upgrade head` |
