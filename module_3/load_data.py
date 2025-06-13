"""
Module 3 Data Loading Script (Updated)

Description:
This script connects to a PostgreSQL database, creates a table to store 
applicant data, and populates it from 'applicant_data.json'. This final version 
cleans and validates the data before insertion, checking for valid GRE score 
ranges and handling data type mismatches.

Prerequisites:
1.  A `DATABASE_URL` secret must be configured in the Replit environment.
2.  Required Python packages installed: `psycopg2-binary`.
3.  The `applicant_data.json` file must be present in the same directory.

Usage:
From the Replit Shell, run:
`python load_data.py`
"""

# ------------------- IMPORTS -------------------
import os
import psycopg2
import json

# ------------------- CONFIGURATION -------------------
JSON_FILE_PATH = 'applicant_data.json' 

# ------------------- SCRIPT EXECUTION -------------------

def main():
    """Main function to run the data loading process."""
    print("--- Starting data loading script ---")

    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise ValueError("DATABASE_URL secret not found. Please set it up in the Replit Secrets tool.")

    conn = None
    try:
        conn = psycopg2.connect(db_url)
        print("Database connection established.")

        with conn.cursor() as cur:
            # --- Step 1: Define and Create the Database Table ---
            cur.execute("DROP TABLE IF EXISTS applicants;")
            print("Dropped existing 'applicants' table (if it existed).")

            create_table_query = """
            CREATE TABLE applicants (
                id SERIAL PRIMARY KEY,
                university TEXT,
                program_name TEXT,
                degree TEXT,
                applicant_status TEXT,
                decision_date TEXT,
                date_added DATE,
                semester_start TEXT,
                student_type TEXT,
                gpa FLOAT,
                gre_total INTEGER,
                gre_v INTEGER,
                gre_q INTEGER,
                gre_aw FLOAT,
                comment TEXT,
                url TEXT
            );
            """
            cur.execute(create_table_query)
            print("Table 'applicants' created with the correct schema.")

            # --- Step 2: Load and Clean JSON Data ---
            print(f"Loading data from file: {JSON_FILE_PATH}")
            with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
                applicants_list = json.load(f)

            print(f"JSON data loaded. Found {len(applicants_list)} records.")

            # --- FIX: Pre-process and validate data in Python ---
            print("Cleaning and validating data before insertion...")

            # Updated validation ranges to use a standard 4.0 GPA scale.
            validation_ranges = {
                'GPA': (0.0, 4.0), # Standard 4.0 GPA scale
                'GRE Total': (260, 340),
                'GRE V': (130, 170),
                'GRE Q': (130, 170),
                'GRE AW': (0.0, 6.0)
            }

            for applicant in applicants_list:
                # First, clean spaces from numeric string fields
                for key in validation_ranges.keys():
                    if key in applicant and isinstance(applicant[key], str):
                        applicant[key] = applicant[key].replace(' ', '.')

                # Now, validate the numeric ranges
                for key, (min_val, max_val) in validation_ranges.items():
                    if key in applicant and applicant[key] not in [None, 'N/A', '']:
                        try:
                            value = float(applicant[key])
                            if not (min_val <= value <= max_val):
                                # More descriptive logging
                                print(f"Invalid value '{value}' for {key}. Out of range ({min_val}-{max_val}). Setting to NULL.")
                                applicant[key] = 'N/A' # Invalidate the data
                        except (ValueError, TypeError):
                            # Handle cases where conversion to float fails
                            print(f"Non-numeric value '{applicant[key]}' for {key}. Setting to NULL.")
                            applicant[key] = 'N/A'

            cleaned_json_data_string = json.dumps(applicants_list)
            print("Data cleaning and validation complete.")

            # --- Step 3: Insert Records into the Database ---
            insert_from_json_query = """
            INSERT INTO applicants (
                university, program_name, degree, applicant_status, decision_date,
                date_added, semester_start, student_type, gpa, gre_total, gre_v,
                gre_q, gre_aw, comment, url
            )
            SELECT
                element->>'University',
                element->>'Program Name',
                element->>'Degree',
                element->>'Applicant Status',
                element->>'Decision Date',
                (NULLIF(element->>'Date Added', 'N/A'))::date,
                element->>'Semester Start',
                element->>'Student Type',
                (NULLIF(element->>'GPA', 'N/A'))::float,
                (NULLIF(element->>'GRE Total', 'N/A'))::integer,
                (NULLIF(element->>'GRE V', 'N/A'))::integer,
                (NULLIF(element->>'GRE Q', 'N/A'))::integer,
                (NULLIF(element->>'GRE AW', 'N/A'))::float,
                element->>'Comment',
                element->>'URL'
            FROM json_array_elements(%s) AS element;
            """

            cur.execute(insert_from_json_query, (cleaned_json_data_string,))

            conn.commit()
            print(f"Transaction committed. {cur.rowcount} new records were processed.")

    except psycopg2.Error as e:
        print(f"A database error occurred: {e}")
        if conn:
            conn.rollback()
    except FileNotFoundError:
        print(f"Error: The file '{JSON_FILE_PATH}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
        print("--- Script finished ---")

if __name__ == "__main__":
    main()
