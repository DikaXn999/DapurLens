import os

from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv(Path(__file__).resolve().parent / ".env")

# DATABASE_URL wajib disediakan melalui environment variable.
# Tidak ada fallback agar aplikasi gagal secara eksplisit jika belum dikonfigurasi.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL belum diatur (lihat .env.example)")

engine = create_engine(DATABASE_URL)

# sessionmaker = "pabrik" yang membuat sesi database baru tiap ada request.
# Kenapa perlu sesi baru tiap request (bukan satu sesi global)?
# Supaya satu user tidak "menabrak" transaksi user lain yang sedang berjalan.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = kelas induk untuk semua model ORM kita (lihat models.py).
# SQLAlchemy pakai ini untuk tahu tabel apa saja yang perlu dibuat.
Base = declarative_base()


def get_db():
    """
    Dependency Injection ala FastAPI: fungsi ini dipanggil FastAPI otomatis
    tiap ada request yang butuh akses database (lihat main.py, parameter
    `db: Session = Depends(get_db)`). "yield" memastikan sesi selalu ditutup
    setelah request selesai, walaupun terjadi error di tengah jalan.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
