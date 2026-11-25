# Changelog

Semua perubahan penting pada DapurLens Backend dicatat di sini.

## [Unreleased]

### Security
- Memindahkan konfigurasi `SECRET_KEY` JWT dan `DATABASE_URL` ke environment variable.
- Menghapus ketergantungan pada kredensial hardcoded.
- Memastikan aplikasi berhenti dengan pesan yang jelas jika konfigurasi wajib belum tersedia.
- Mengecualikan file `.env` dari Git dan menyediakan `.env.example` sebagai template.

### Testing
- Menambahkan unit test untuk memverifikasi penanganan konfigurasi environment yang hilang.
- Menambahkan `pytest` sebagai dependensi pengembangan.

### Documentation
- Menambahkan panduan instalasi, konfigurasi environment, menjalankan API, dan pengujian.
