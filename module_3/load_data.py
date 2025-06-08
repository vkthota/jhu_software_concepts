"""
Module 3 Data Loading Script

Description:
This script connects to a PostgreSQL database hosted on Replit, creates a table 
to store graduate school applicant data, and then populates this table with data 
from a specified JSON file. This version is robustly designed to handle 
mismatches between JSON key names and database columns, automatically generates a 
unique primary key, and sanitizes missing data (e.g., "N/A" values) during
insertion.

Prerequisites:
1.  A `DATABASE_URL` secret must be configured in the Replit environment.
2.  Required Python packages installed via `requirements.txt`: `psycopg2-binary`.
3.  A JSON data file present at the path specified in `JSON_FILE_PATH`.

Usage:
From the Replit Shell, navigate into the module_3 directory and run:
`python load_data.py`
"""

# ------------------- IMPORTS -------------------
import os
import psycopg2
import json

# ------------------- CONFIGURATION -------------------
# This path should be relative to where the script is run.
# Since we run it from inside module_3, it's just the filename.
JSON_FILE_PATH = 'applicant_data.json' 

# ------------------- SCRIPT EXECUTION -------------------

def main():
    """Main function to run the data loading process."""
    print("--- Starting data loading script (Final Version) ---")

    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL secret not found. Please set it up in the Replit Secrets tool.")

    conn = None
    try:
        # Connect directly using psycopg2
        conn = psycopg2.connect(db_url)
        print("Database connection established.")

        # Use a 'with' statement for the cursor to ensure it's properly closed.
        with conn.cursor() as cur:

            # --- Step 1: Define and Create the Database Table ---
            # `p_id SERIAL PRIMARY KEY` creates an auto-incrementing unique ID for each row.
            create_table_query = """
            CREATE TABLE IF NOT EXISTS applicants (
                p_id SERIAL PRIMARY KEY,
                program TEXT,
                comments TEXT,
                date_added DATE,
                status TEXT,
                url TEXT,
                term TEXT,
                us_or_international TEXT,
                gpa FLOAT,
                gre FLOAT,
                gre_v FLOAT,
                gre_aw FLOAT,
                degree TEXT
            );
            """
            cur.execute(create_table_query)
            print("Table 'applicants' is ready.")

            # --- Step 2: Load JSON Data from File ---
            print(f"Loading data from file: {JSON_FILE_PATH}")
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
                json_data_string = f.read()
            # Validate the JSON and get the record count for logging.
            applicants_list = json.loads(json_data_string)
            print(f"JSON data validated. Found {len(applicants_list)} records.")

            # --- Step 3: Insert Records into the Database ---
            # This query maps JSON keys to table columns and handles "N/A" values.
            insert_from_json_query = """
            INSERT INTO applicants (
                program, url, degree, date_added, status, comments,
                term, us_or_international, gpa, gre, gre_v, gre_aw
            )
            SELECT
                element->>'Program Field',
                element->>'URL Link',
                element->>'Program Degree Level',
                (NULLIF(element->>'Date Added', 'N/A'))::date,
                element->>'Applicant Status',
                element->>'Comments',
                element->>'Program Start Term',
                element->>'Student Status',
                (NULLIF(element->>'GPA', 'N/A'))::float,
                (NULLIF(element->>'GRE Total or General', 'N/A'))::float,
                (NULLIF(element->>'GRE Verbal', 'N/A'))::float,
                (NULLIF(element->>'GRE Quant', 'N/A'))::float
            FROM json_array_elements(%s) AS element
            ON CONFLICT (p_id) DO NOTHING;
            """

            cur.execute(insert_from_json_query, (json_data_string,))

            # We must explicitly commit the transaction to save the changes.
            conn.commit()
            print(f"Transaction committed. {cur.rowcount} new records were processed.")

    except psycopg2.Error as e:
        print(f"A database error occurred: {e}")
        if conn:
            conn.rollback() # Roll back the transaction on error
    except FileNotFoundError:
        print(f"Error: The file '{JSON_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # Ensure the connection is always closed.
        if conn:
            conn.close()
            print("Database connection closed.")
        print("--- Script finished ---")

if __name__ == "__main__":
    main()