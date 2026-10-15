import sqlite3
from pathlib import Path

import requests

url = "https://openlibrary.org/search.json?q=python&limit=5"

response = requests.get(url, timeout=15)
response.raise_for_status()

data = response.json()
books = data["docs"]

database_path = Path(__file__).resolve().parent.parent / "data" / "output" / "books.db"
book_rows = []

for book in books:
    title = book.get("title") or "Unknown"
    author_names = book.get("author_name")
    if isinstance(author_names, list):
        author = ", ".join(str(name) for name in author_names if name) or "Unknown"
    else:
        author = str(author_names) if author_names else "Unknown"

    publication_year = book.get("first_publish_year")
    if publication_year is not None:
        try:
            publication_year = int(publication_year)
        except (TypeError, ValueError):
            publication_year = None

    book_rows.append((str(title), author, publication_year))

with sqlite3.connect(database_path) as connection:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publication_year INTEGER
        )
        """
    )
    connection.execute("DELETE FROM books")
    connection.executemany(
        """
        INSERT INTO books (title, author, publication_year)
        VALUES (?, ?, ?)
        """,
        book_rows,
    )
    connection.commit()
    stored_books = connection.execute(
        """
        SELECT title, author, publication_year
        FROM books
        ORDER BY id
        """
    ).fetchall()

print("Books retrieved:", len(books))

for title, author, publication_year in stored_books:
    print("Title:", title)
    print("Authors:", author)
    print("Publication year:", publication_year if publication_year is not None else "Unknown")
    print("-" * 30)