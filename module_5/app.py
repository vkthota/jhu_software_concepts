# module_5/app.py
"""
This module contains a Flask web application that connects to a PostgreSQL
database to retrieve and display applicant data.
"""

import os
from flask import Flask, render_template
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

def execute_query(query, params=None):
    """
    Connects to the database, executes a given SQL query, and returns results.

    This function is designed to be reusable and securely handles queries
    by using parameterized inputs.

    Args:
        query (psycopg2.sql.SQL): The SQL query object to be executed.
        params (tuple, optional): A tuple of parameters to be safely
                                  substituted into the query. Defaults to None.

    Returns:
        list: A list of tuples containing the query results, or an empty
              list if an error occurs or no results are found.
    """
    db_url = os.environ.get('DATABASE_URL')
    try:
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Database query error: {e}")
    return []

# --- Helper functions for each query ---

def _get_query_1_data(semester):
    """Fetches the total number of applicants for a given semester."""
    question = "1. How many applicants for Fall 2025?"
    query = sql.SQL("SELECT COUNT(*) FROM applicants WHERE semester_start = %s;")
    result = execute_query(query, (semester,))
    answer = f"{result[0][0]:,}" if result else "Query Failed"
    return (question, answer)

def _get_query_2_data():
    """Fetches the percentage of international students."""
    question = "2. Percentage of International Students:"
    query = sql.SQL("SELECT 100.0 * COUNT(*) FILTER"
                    " (WHERE student_type = 'International') / COUNT(*)"
                    " FROM applicants;")
    result = execute_query(query)
    answer = f"{result[0][0]:.2f}%" if result and result[0][0] is not None else "Query Failed"
    return (question, answer)

def _get_query_3_data():
    """Fetches the average scores across all terms."""
    question = "3. Average Scores (All Terms):"
    query = sql.SQL("SELECT AVG(gpa), AVG(gre_total), AVG(gre_v), AVG(gre_q),"
                    " AVG(gre_aw) FROM applicants;")
    result = execute_query(query)
    answer_list = []
    if result and result[0] is not None:
        avg_gpa, avg_gre_total, avg_gre_v, avg_gre_q, avg_gre_aw = result[0]
        answer_list.append(f"GPA: {avg_gpa:.2f}" if avg_gpa else "GPA: N/A")
        answer_list.append(f"GRE Total: {avg_gre_total:.2f}" if avg_gre_total else "GRE T: N/A")
        answer_list.append(f"GRE Verbal: {avg_gre_v:.2f}" if avg_gre_v else "GRE V: N/A")
        answer_list.append(f"GRE Quant: {avg_gre_q:.2f}" if avg_gre_q else "GRE Q: N/A")
        answer_list.append(f"GRE AW: {avg_gre_aw:.2f}" if avg_gre_aw else "GRE AW: N/A")
    answer = " | ".join(answer_list) if answer_list else "No Data"
    return (question, answer)

def _get_query_4_data(student_type, semester):
    """Fetches the average GPA for a student type in a given semester."""
    question = "4. Avg GPA of American Students in Fall 2025:"
    query = sql.SQL("SELECT AVG(gpa) FROM applicants"
                    " WHERE student_type = %s AND semester_start = %s;")
    result = execute_query(query, (student_type, semester))
    answer = f"{result[0][0]:.2f}" if result and result[0][0] is not None else "No Data"
    return (question, answer)

def _get_query_5_data(semester):
    """Fetches the percentage of acceptances for a given semester."""
    question = "5. Percent Acceptances for Fall 2025:"
    query = sql.SQL("SELECT 100.0 * COUNT(*) FILTER"
                    " (WHERE applicant_status = 'Accepted') / NULLIF(COUNT(*), 0)"
                    " FROM applicants WHERE semester_start = %s;")
    result = execute_query(query, (semester,))
    answer = f"{result[0][0]:.2f}%" if result and result[0][0] is not None else "No Data"
    return (question, answer)

def _get_query_6_data(semester, status):
    """Fetches the average GPA of accepted students for a given semester."""
    question = "6. Avg GPA of Accepted Students in Fall 2025:"
    query = sql.SQL("SELECT AVG(gpa) FROM applicants"
                    " WHERE semester_start = %s AND applicant_status = %s;")
    result = execute_query(query, (semester, status))
    answer = f"{result[0][0]:.2f}" if result and result[0][0] is not None else "No Data"
    return (question, answer)

def _get_query_7_data(university, program, degree):
    """Fetches the count of applicants for a specific program."""
    question = "7. Johns Hopkins Masters in Computer Science Applicants:"
    query = sql.SQL("SELECT COUNT(*) FROM applicants"
                    " WHERE university ILIKE %s AND program_name ILIKE %s"
                    " AND degree = %s;")
    result = execute_query(query, (university, program, degree))
    answer = result[0][0] if result else "Query Failed"
    return (question, answer)

@app.route('/')
def index():
    """
    Handles requests to the main page.

    Executes all required queries by calling helper functions and renders
    them in the main HTML template.
    """
    query_results = [
        _get_query_1_data("Fall 2025"),
        _get_query_2_data(),
        _get_query_3_data(),
        _get_query_4_data("American", "Fall 2025"),
        _get_query_5_data("Fall 2025"),
        _get_query_6_data("Fall 2025", "Accepted"),
        _get_query_7_data("%Johns Hopkins%", "%Computer Science%", "Masters")
    ]

    return render_template('index.html', query_results=query_results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
