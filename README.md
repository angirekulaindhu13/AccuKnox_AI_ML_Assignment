# AccuKnox AI/ML Trainee Assessment

## Project overview

This repository contains three small Python assessment exercises:

1. Retrieve Python-related book search results from the Open Library API and store them in SQLite.
2. Fetch synthetic student scores from a local HTTP mock API, calculate their average, and save a Matplotlib bar chart.
3. Import users from a CSV file into SQLite while ignoring duplicate email addresses.

The scripts are run individually from the repository root. They use paths relative to their own locations for input and output files.

## Assessment objectives

- Make an HTTP request and use JSON data in a SQLite database.
- Consume an HTTP JSON endpoint, calculate an average, and visualize the results.
- Read and validate CSV records, then persist them with duplicate handling.

## Technologies and dependencies

- Python 3
- `requests` — HTTP requests in `test_books_api.py` and `fetch_student_scores.py`
- `matplotlib` — chart creation in `fetch_student_scores.py`
- SQLite via Python's built-in `sqlite3` module
- Python standard-library modules: `csv`, `http.server`, `json`, `math`, and `pathlib`

There is no dependency manifest in the repository. Install the two third-party packages, `requests` and `matplotlib`, as shown below. The mock API uses Python's built-in HTTP server and requires no web framework.

## Project folder structure

```text
AccuKnox_AI_ML_Assignment/
├── data/
│   ├── input/
│   │   └── users.csv
│   └── output/
│       ├── books.db
│       ├── student_scores.png
│       └── users.db
├── src/
│   ├── fetch_student_scores.py
│   ├── import_users_csv.py
│   ├── mock_student_api.py
│   └── test_books_api.py
├── tests/                   # Empty in the current project
├── .venv/                   # Existing local virtual environment
└── README.md
```

The `.venv/` directory is a local virtual environment; it is not needed in version control. The three files under `data/output/` are the database and chart output locations used by the scripts.

## Question 1: Open Library API to SQLite

`src/test_books_api.py` sends a GET request to:

```text
https://openlibrary.org/search.json?q=python&limit=5
```

It reads the returned `docs`, extracts each book's title, author name(s), and first publication year, and stores them in the `books` table in `data/output/books.db`. Missing titles or authors are represented as `Unknown`; an unavailable or invalid publication year is stored as `NULL` and displayed as `Unknown`.

The table has `id`, `title`, `author`, and `publication_year` columns. On each run, the script deletes the existing rows from `books` before inserting the current response; it does not append historical search results. The request requires network access to Open Library.

## Question 2: Student scores, average calculation, and Matplotlib bar chart

`src/fetch_student_scores.py` requests JSON from the local endpoint `http://127.0.0.1:8000/students`. It validates the response records, prints the student count and average test score, then saves a bar chart to `data/output/student_scores.png`.

**This project has not integrated an external student-score API.** The endpoint is served by `src/mock_student_api.py` and returns fabricated, synthetic sample records. The client uses those records only when the local mock server is running.

Start the mock API in one terminal and leave it running. In a second terminal, activate the same environment and run the client:

```powershell
# Terminal 1: start the mock API
.\.venv\Scripts\Activate.ps1
python .\src\mock_student_api.py
```

```powershell
# Terminal 2: fetch scores and create the chart
.\.venv\Scripts\Activate.ps1
python .\src\fetch_student_scores.py
```

The mock server listens on `127.0.0.1:8000` and serves the `/students` route until stopped with `Ctrl+C`. If the server is not running, the client cannot fetch the scores.

## Question 3: CSV to SQLite import with duplicate handling

`src/import_users_csv.py` reads `data/input/users.csv`, which must contain `name` and `email` columns. It rejects rows with a missing name or email, then stores valid records in the `users` table in `data/output/users.db`.

The email column has a case-insensitive unique constraint. Inserts use `INSERT OR IGNORE`, so an email already in the database—including one that differs only in letter case—is not inserted again. Existing records are retained on subsequent runs. If the database already contains duplicate email records, the script stops and reports them rather than proceeding with the import.

## Installation instructions

Run these commands from the repository root in PowerShell. If the existing `.venv/` is unavailable or you prefer a fresh environment, create it first:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install requests matplotlib
```

If PowerShell does not allow activation in your session, use the environment's interpreter directly for the install and run commands:

```powershell
.\.venv\Scripts\python.exe -m pip install requests matplotlib
```

No separate database setup is required. The scripts create their tables when needed, and this checkout already contains `data/output/`.

## Commands to run each script

Run from the repository root after installing the dependencies:

```powershell
# Question 1: Open Library search and SQLite storage
python .\src\test_books_api.py

# Question 2: start the mock API in a separate terminal first
python .\src\mock_student_api.py

# Question 2: in another terminal, while the mock API is running
python .\src\fetch_student_scores.py

# Question 3: CSV import into SQLite
python .\src\import_users_csv.py
```

## Expected outputs and output file locations

- **Question 1:** Prints the number of books retrieved and each stored book's title, authors, and publication year. Creates or refreshes `data/output/books.db`, containing the `books` table.
- **Question 2 mock server:** Prints that the synthetic student API is available at `http://127.0.0.1:8000/students`. It continues serving until interrupted.
- **Question 2 client:** Prints the number of students, average test score, and saved chart path. The mock data currently defined in the server contains five records with scores 82, 91, 76, 88, and 95; for that data the average is `86.40`. The chart is saved to `data/output/student_scores.png`.
- **Question 3:** Prints the number of records inserted and the stored users. Creates or updates `data/output/users.db`, containing the `users` table. Re-running the import skips email addresses already present.

Database rows and the chart are generated or refreshed by running the corresponding script; their presence in the folder does not indicate that a run succeeded in a particular environment.

## Known limitations

- The Open Library exercise depends on network access and on the API returning the expected JSON structure. Its search is fixed to `q=python` and limited to five results.
- The student-score client uses only the local synthetic mock API; it does not connect to an external student service. The mock server must be started separately and is bound to the local machine.
- The CSV import uses the checked-in `data/input/users.csv`. It ignores email duplicates instead of updating existing user details.
- The `tests/` directory is empty in the current project structure; no test suite is included there.

## Candidate

**Indhu Angirekula**
