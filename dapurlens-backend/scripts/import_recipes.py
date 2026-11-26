
import argparse
import sys
from pathlib import Path

from openpyxl import load_workbook
from sqlalchemy.exc import SQLAlchemyError

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from app.database import SessionLocal
from app.models import Food
from app.utils import slugify


EXCEL_PATH = BACKEND_DIR.parent / "DapurLens_50_Resep_Khas-Daerah.xlsx"
SHEET_NAME = "Data Resep"

GRADIENT_FROM = "#F3B6A8"
GRADIENT_TO = "#E39C90"

REQUIRED_COLUMNS = [
    "Nama Makanan",
    "Asal Daerah",
    "Deskripsi Singkat",
    "Bahan-bahan",
    "Langkah Memasak",
    "Emoji (opsional)",
]


def clean_text(value):
    if value is None:
        return ""
    return str(value).strip()


def split_lines(value):
    if not value:
        return []

    return [
        line.strip()
        for line in str(value).splitlines()
        if line.strip()
    ]


def validate_row(row):
    errors = []

    for column in REQUIRED_COLUMNS:
        if not clean_text(row.get(column)):
            errors.append(f"Kolom '{column}' kosong")

    ingredients = split_lines(row.get("Bahan-bahan"))
    steps = split_lines(row.get("Langkah Memasak"))

    if not ingredients:
        errors.append("Daftar bahan kosong")

    if not steps:
        errors.append("Daftar langkah memasak kosong")

    name = clean_text(row.get("Nama Makanan"))

    if name and not slugify(name):
        errors.append("Nama makanan tidak menghasilkan slug yang valid")

    return errors


def read_recipes(excel_path):
    if not excel_path.exists():
        raise FileNotFoundError(
            f"File Excel tidak ditemukan: {excel_path}"
        )

    workbook = load_workbook(
        excel_path,
        read_only=True,
        data_only=True,
    )

    try:
        if SHEET_NAME not in workbook.sheetnames:
            raise ValueError(
                f"Sheet '{SHEET_NAME}' tidak ditemukan. "
                f"Sheet tersedia: {workbook.sheetnames}"
            )

        sheet = workbook[SHEET_NAME]
        rows = sheet.iter_rows(values_only=True)

        headers = next(rows, None)

        if not headers:
            raise ValueError("Sheet Excel kosong.")

        header_map = {
            clean_text(header): index
            for index, header in enumerate(headers)
            if header is not None
        }

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in header_map
        ]

        if missing_columns:
            raise ValueError(
                f"Kolom wajib tidak ditemukan: {missing_columns}"
            )

        recipes = []

        for excel_row, values in enumerate(rows, start=2):
            row = {
                column: values[index]
                if index < len(values)
                else None
                for column, index in header_map.items()
            }

            if not any(clean_text(value) for value in row.values()):
                continue

            errors = validate_row(row)

            recipes.append({
                "row": excel_row,
                "data": row,
                "errors": errors,
            })

        return recipes

    finally:
        workbook.close()


def import_recipes(excel_path, commit=False):
    recipes = read_recipes(excel_path)

    valid_rows = [item for item in recipes if not item["errors"]]
    invalid_rows = [item for item in recipes if item["errors"]]

    print(f"\nTotal baris resep: {len(recipes)}")
    print(f"Data valid: {len(valid_rows)}")
    print(f"Data tidak valid: {len(invalid_rows)}")

    for item in invalid_rows:
        print(f"\n[ERROR] Baris Excel {item['row']}")
        for error in item["errors"]:
            print(f"  - {error}")

    if not commit:
        print("\n[DRY RUN] Database tidak diubah.")
        print("Gunakan --commit untuk menyimpan data.")
        return

    db = SessionLocal()

    imported = 0
    skipped = 0
    failed = 0

    # Slug yang sudah ada di database.
    seen_slugs = {
        slug for (slug,) in db.query(Food.slug).all()
    }

    try:
        for item in valid_rows:
            row = item["data"]
            name = clean_text(row["Nama Makanan"])
            base_slug = slugify(name)

            # Hindari duplikasi slug.
            if base_slug in seen_slugs:
                print(f"[SKIP] Baris {item['row']}: {name}")
                skipped += 1
                continue

            # Buat slug unik jika terjadi benturan.
            slug = base_slug
            suffix = 2

            while slug in seen_slugs:
                slug = f"{base_slug}-{suffix}"
                suffix += 1

            try:
                # Savepoint: kegagalan satu resep tidak
                # membatalkan transaksi resep lainnya.
                with db.begin_nested():
                    food = Food(
                        slug=slug,
                        name=name,
                        region=clean_text(row["Asal Daerah"]),
                        tags=["daerah"],
                        emoji=clean_text(row["Emoji (opsional)"]),
                        description=clean_text(row["Deskripsi Singkat"]),
                        gradient_from=GRADIENT_FROM,
                        gradient_to=GRADIENT_TO,
                        ingredients=split_lines(row["Bahan-bahan"]),
                        steps=split_lines(row["Langkah Memasak"]),
                    )

                    db.add(food)
                    db.flush()

                seen_slugs.add(slug)
                imported += 1

                print(f"[OK] {name} -> {slug}")

            except SQLAlchemyError as error:
                failed += 1
                print(
                    f"[ERROR] Baris {item['row']}: {name} - {error}"
                )

        # Commit seluruh resep yang berhasil.
        db.commit()

        print("\n========== HASIL IMPORT ==========")
        print(f"Berhasil : {imported}")
        print(f"Dilewati : {skipped}")
        print(f"Gagal    : {failed}")
        print("==================================")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(
        description="Import resep daerah dari Excel ke database DapurLens."
    )

    parser.add_argument(
        "--file",
        type=Path,
        default=EXCEL_PATH,
        help="Lokasi file Excel resep.",
    )

    parser.add_argument(
        "--commit",
        action="store_true",
        help="Simpan resep ke database. Tanpa opsi ini hanya dry-run.",
    )

    args = parser.parse_args()

    try:
        import_recipes(args.file, commit=args.commit)

    except (FileNotFoundError, ValueError, SQLAlchemyError) as error:
        print(f"\n[GAGAL] {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()