# module_5/load_data.py
"""
Module 5 Data Loading Script

Description:
This script connects to a PostgreSQL database using credentials from environment
variables. It first drops any existing 'applicants' table, then creates a new
one with a defined schema. Finally, it loads data from a local JSON file,
cleans and validates the data in Python, and inserts the sanitized records
into the database.

Prerequisites:
- A `DATABASE_URL` secret configured in the environment.
- Required Python packages: `psycopg2-binary`.
- `applicant_data.json` file present in the same directory.

Usage:
From the shell, run: `python load_data.py`
"""
import os
import json
import psycopg2

JSON_FILE_PATH = 'applicant_data.json'

def _create_applicants_table(cur):
    """Drops and recreates the 'applicants' table."""
    cur.execute("DROP TABLE IF EXISTS applicants;")
    print("Dropped existing 'applicants' table.")

    create_table_query = """
    CREATE TABLE applicants (
        id SERIAL PRIMARY KEY, university TEXT, program_name TEXT,
        degree TEXT, applicant_status TEXT, decision_date TEXT,
        date_added DATE, semester_start TEXT, student_type TEXT,
        gpa FLOAT, gre_total INTEGER, gre_v INTEGER,
        gre_q INTEGER, gre_aw FLOAT, comment TEXT, url TEXT
    );"""
    cur.execute(create_table_query)
    print("Table 'applicants' created.")

def _load_and_clean_json_data(filepath):
    """Loads JSON data from a file and cleans it."""
    print(f"Loading and cleaning data from {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        applicants_list = json.load(f)

    validation_ranges = {
        'GPA': (0.0, 4.0), 'GRE Total': (260, 340), 'GRE V': (130, 170),
        'GRE Q': (130, 170), 'GRE AW': (0.0, 6.0)
    }
    for applicant in applicants_list:
        for key, (min_val, max_val) in validation_ranges.items():
            if key in applicant and applicant[key] not in [None, 'N/A', '']:
                if isinstance(applicant[key], str):
                    applicant[key] = applicant[key].replace(' ', '.')
                try:
                    value = float(applicant[key])
                    if not min_val <= value <= max_val:
                        applicant[key] = 'N/A'
                except (ValueError, TypeError):
                    applicant[key] = 'N/A'
    print(f"Cleaning complete. Found {len(applicants_list)} records.")
    return json.dumps(applicants_list)

def _insert_data(cur, json_data_string):
    """Inserts the cleaned JSON data into the applicants table."""
    insert_query = """
    INSERT INTO applicants (
        university, program_name, degree, applicant_status, decision_date,
        date_added, semester_start, student_type, gpa, gre_total, gre_v,
        gre_q, gre_aw, comment, url
    )
    SELECT
        d->>'University', d->>'Program Name', d->>'Degree',
        d->>'Applicant Status', d->>'Decision Date',
        (NULLIF(d->>'Date Added', 'N/A'))::date, d->>'Semester Start',
        d->>'Student Type', (NULLIF(d->>'GPA', 'N/A'))::float,
        (NULLIF(d->>'GRE Total', 'N/A'))::integer,
        (NULLIF(d->>'GRE V', 'N/A'))::integer,
        (NULLIF(d->>'GRE Q', 'N/A'))::integer,
        (NULLIF(d->>'GRE AW', 'N/A'))::float, d->>'Comment', d->>'URL'
    FROM json_array_elements(%s) AS d;
    """
    cur.execute(insert_query, (json_data_string,))
    print(f"Executing insert. {cur.rowcount} records were processed.")

def main():
    """Main function to run the entire data loading process."""
    print("--- Starting data loading script ---")
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL secret not found. Please set it up.")

    conn = None
    try:
        conn = psycopg2.connect(db_url)
        print("Database connection established.")
        with conn.cursor() as cur:
            _create_applicants_table(cur)
            cleaned_json_data = _load_and_clean_json_data(JSON_FILE_PATH)
            _insert_data(cur, cleaned_json_data)
        conn.commit()
        print("Transaction committed.")
    except psycopg2.Error as e:
        print(f"A database error occurred: {e}")
        if conn:
            conn.rollback()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"A file or data error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
        print("--- Script finished ---")

if __name__ == "__main__":
    main()
