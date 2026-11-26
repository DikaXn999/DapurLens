BEGIN;

-- Tambahkan role; akun lama otomatis mendapat PENGGUNA.
ALTER TABLE users
ADD COLUMN role VARCHAR NOT NULL DEFAULT 'PENGGUNA';

-- Pastikan akun lama yang is_active-nya NULL menjadi aktif.
UPDATE users
SET is_active = TRUE
WHERE is_active IS NULL;

-- Tetapkan default dan constraint pada database.
ALTER TABLE users
ALTER COLUMN is_active SET DEFAULT TRUE;

ALTER TABLE users
ALTER COLUMN is_active SET NOT NULL;

COMMIT;
