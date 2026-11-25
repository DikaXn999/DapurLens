# DapurLens Backend

Backend API DapurLens menggunakan FastAPI, SQLAlchemy, dan PostgreSQL.

## 1. Persiapan

Buat dan aktifkan virtual environment:

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1

Instal dependensi:

    python -m pip install -r requirements-dev.txt

## 2. Konfigurasi Environment

Jika file app/.env belum tersedia, salin template:

    Copy-Item .\app\.env.example .\app\.env

Jangan jalankan perintah tersebut jika app/.env sudah ada karena konfigurasi lokal akan tertimpa.

Isi app/.env dengan variabel berikut:

- DATABASE_URL: URL koneksi PostgreSQL.
- SECRET_KEY: kunci acak untuk JWT.
- GEMINI_API_KEY: API key Google Gemini.

Buat SECRET_KEY menggunakan:

    python -c "import secrets; print(secrets.token_urlsafe(32))"

Jangan commit atau membagikan file .env. File ini sudah dikecualikan melalui .gitignore.

Aplikasi akan berhenti dengan pesan yang jelas jika DATABASE_URL atau SECRET_KEY belum tersedia.

## 3. Menjalankan API

    python -m uvicorn app.main:app --reload

API tersedia di http://127.0.0.1:8000.

Dokumentasi API tersedia di http://127.0.0.1:8000/docs.

## 4. Pengujian

    python -m pytest -v
