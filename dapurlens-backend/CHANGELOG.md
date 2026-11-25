# Changelog

Semua perubahan penting pada DapurLens Backend dicatat di sini.

## [Unreleased]

### Security
- Mendokumentasikan penggunaan environment variable untuk DATABASE_URL dan SECRET_KEY.
- Mendokumentasikan perilaku aplikasi ketika konfigurasi wajib belum tersedia.
- Mendokumentasikan penggunaan .env dan .env.example serta pengecualian file .env dari Git.

### Testing
- Menambahkan unit test untuk memverifikasi penanganan konfigurasi environment yang hilang.
- Menambahkan pytest sebagai dependensi pengembangan.

### Documentation
- Menambahkan panduan instalasi, konfigurasi environment, menjalankan API, dan pengujian.
