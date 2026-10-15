import csv
import sqlite3
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "input" / "users.csv"
DATABASE_PATH = PROJECT_ROOT / "data" / "output" / "users.db"


def main():
	try:
		with CSV_PATH.open("r", newline="", encoding="utf-8-sig") as csv_file:
			reader = csv.DictReader(csv_file)
			required_columns = {"name", "email"}
			if reader.fieldnames is None or not required_columns.issubset(reader.fieldnames):
				raise ValueError("CSV must contain 'name' and 'email' columns")

			users = []
			for line_number, row in enumerate(reader, start=2):
				name = (row.get("name") or "").strip()
				email = (row.get("email") or "").strip()
				if not name or not email:
					raise ValueError(
						f"CSV row {line_number} must contain both name and email"
					)
				users.append((name, email))

		DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
		with sqlite3.connect(DATABASE_PATH) as connection:
			connection.execute(
				"""
				CREATE TABLE IF NOT EXISTS users (
					id INTEGER PRIMARY KEY,
					name TEXT NOT NULL,
					email TEXT NOT NULL COLLATE NOCASE UNIQUE
				)
				"""
			)
			duplicate_emails = connection.execute(
				"""
				SELECT email
				FROM users
				GROUP BY email COLLATE NOCASE
				HAVING COUNT(*) > 1
				"""
			).fetchall()
			if duplicate_emails:
				emails = ", ".join(email for (email,) in duplicate_emails)
				raise ValueError(
					"Existing duplicate email records must be reviewed before import: "
					f"{emails}"
				)

			connection.execute(
				"CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email_unique "
				"ON users (email COLLATE NOCASE)"
			)
			insert_cursor = connection.executemany(
				"INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)",
				users,
			)
			inserted_count = insert_cursor.rowcount
			connection.commit()
			stored_users = connection.execute(
				"SELECT id, name, email FROM users ORDER BY id"
			).fetchall()

		print(f"Records inserted: {inserted_count}")
		print("Stored users:")
		for user_id, name, email in stored_users:
			print(f"{user_id}: {name} <{email}>")

	except (OSError, sqlite3.Error, ValueError, csv.Error) as error:
		print(f"User import failed: {error}")
		raise SystemExit(1) from error


if __name__ == "__main__":
	main()
