import os
import re
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import Session

from .models import GuestScan

# Bisa diubah lewat environment variable tanpa menyentuh kode.
GUEST_SCAN_LIMIT = int(os.getenv("GUEST_SCAN_LIMIT", "3"))

# Hanya huruf/angka/underscore/strip, 8-64 karakter (UUID lolos).
_GUEST_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{8,64}$")


def validate_guest_id(guest_id: Optional[str]) -> str:
    if not guest_id or not _GUEST_ID_PATTERN.match(guest_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Header X-Guest-Id wajib dan valid untuk memindai tanpa login",
        )
    return guest_id


def reserve_guest_scan(db: Session, guest_id: str) -> int:
    """
    "Pesan" satu jatah pindai SEBELUM memanggil AI. Mengembalikan sisa jatah;
    melempar 429 kalau jatah sudah habis.
    """
    # Pastikan baris untuk guest ini ada (diam saja kalau sudah ada).
    db.execute(pg_insert(GuestScan).values(guest_id=guest_id, used=0).on_conflict_do_nothing())

    # Satu UPDATE ... WHERE used < LIMIT: database yang menentukan, jadi dua
    # request bersamaan tidak bisa "menyalip" batas.
    result = db.execute(
        update(GuestScan)
        .where(GuestScan.guest_id == guest_id, GuestScan.used < GUEST_SCAN_LIMIT)
        .values(used=GuestScan.used + 1)
    )
    if result.rowcount == 0:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Batas {GUEST_SCAN_LIMIT}x pemindaian gratis sudah habis. Daftar atau masuk untuk lanjut memindai.",
        )

    used = db.execute(select(GuestScan.used).where(GuestScan.guest_id == guest_id)).scalar_one()
    db.commit()
    return GUEST_SCAN_LIMIT - used


def refund_guest_scan(db: Session, guest_id: str) -> None:
    """Kembalikan jatah kalau pemindaian gagal karena salah kami (mis. AI error)."""
    db.execute(
        update(GuestScan)
        .where(GuestScan.guest_id == guest_id, GuestScan.used > 0)
        .values(used=GuestScan.used - 1)
    )
    db.commit()


def get_guest_remaining(db: Session, guest_id: str) -> int:
    used = db.execute(select(GuestScan.used).where(GuestScan.guest_id == guest_id)).scalar_one_or_none()
    return GUEST_SCAN_LIMIT - (used or 0)