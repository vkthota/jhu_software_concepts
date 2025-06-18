# module_5/query_data.py
"""
This script runs a series of predefined queries against the 'applicants'
database table and prints the formatted results to the console.

It is intended to be run as a standalone script from the command line.
"""
import os
import psycopg2
from psycopg2 import sql

def execute_query(query, params=None):
    """
    Connects to the database, executes a given SQL query, and returns results.

    Args:
        query (psycopg2.sql.SQL): The SQL query object to be executed.
        params (tuple, optional): A tuple of parameters to be safely
                                  substituted into the query. Defaults to None.

    Returns:
        list: A list of tuples containing the query results, or None if
              an error occurs.
    """
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL secret not found.")
        return None
    try:
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Database query error: {e}")
    return None

# --- Helper functions to get formatted output for each query ---

def _get_query_1_output():
    """Fetches and formats the output for Query 1."""
    query = sql.SQL("SELECT COUNT(*) FROM applicants WHERE semester_start = %s;")
    result = execute_query(query, ("Fall 2025",))
    answer = f"{result[0][0]:,}" if result else "Query Failed"
    return f"1. Applicants for Fall 2025: {answer}"

def _get_query_2_output():
    """Fetches and formats the output for Query 2."""
    query = sql.SQL("SELECT 100.0 * COUNT(*) FILTER"
                    " (WHERE student_type = 'International') / COUNT(*)"
                    " FROM applicants;")
    result = execute_query(query)
    answer = f"{result[0][0]:.2f}%" if result and result[0][0] is not None else "Query Failed"
    return f"2. Percentage of International Students: {answer}"

def _get_query_3_output():
    """Fetches and formats the output for Query 3."""
    query = sql.SQL("SELECT AVG(gpa), AVG(gre_total), AVG(gre_v), "
                    "AVG(gre_q), AVG(gre_aw) FROM applicants;")
    result = execute_query(query)
    output = "3. Average Scores (All Terms):\n"
    if result and result[0]:
        gpa, total, v, q, aw = result[0]
        output += f"   - GPA: {gpa:.2f}\n" if gpa else "   - GPA: N/A\n"
        output += f"   - GRE Total: {total:.2f}\n" if total else "   - GRE Total: N/A\n"
        output += f"   - GRE Verbal: {v:.2f}\n" if v else "   - GRE Verbal: N/A\n"
        output += f"   - GRE Quant: {q:.2f}\n" if q else "   - GRE Quant: N/A\n"
        output += f"   - GRE AW: {aw:.2f}" if aw else "   - GRE AW: N/A"
    else:
        output += "   Query Failed or No Data"
    return output

def _get_query_4_output():
    """Fetches and formats the output for Query 4."""
    query = sql.SQL("SELECT AVG(gpa) FROM applicants"
                    " WHERE student_type = %s AND semester_start = %s;")
    result = execute_query(query, ("American", "Fall 2025"))
    answer = f"{result[0][0]:.2f}" if result and result[0][0] is not None else "No Data"
    return f"4. Avg GPA of American Students in Fall 2025: {answer}"

def _get_query_5_output():
    """Fetches and formats the output for Query 5."""
    query = sql.SQL("SELECT 100.0 * COUNT(*) FILTER"
                    " (WHERE applicant_status = 'Accepted') / NULLIF(COUNT(*), 0)"
                    " FROM applicants WHERE semester_start = %s;")
    result = execute_query(query, ("Fall 2025",))
    answer = f"{result[0][0]:.2f}%" if result and result[0][0] is not None else "No Data"
    return f"5. Percent Acceptances for Fall 2025: {answer}"

def _get_query_6_output():
    """Fetches and formats the output for Query 6."""
    query = sql.SQL("SELECT AVG(gpa) FROM applicants"
                    " WHERE semester_start = %s AND applicant_status = %s;")
    result = execute_query(query, ("Fall 2025", "Accepted"))
    answer = f"{result[0][0]:.2f}" if result and result[0][0] is not None else "No Data"
    return f"6. Average GPA of Accepted Students in Fall 2025: {answer}"

def _get_query_7_output():
    """Fetches and formats the output for Query 7."""
    query = sql.SQL("SELECT COUNT(*) FROM applicants"
                    " WHERE university ILIKE %s AND program_name ILIKE %s"
                    " AND degree = %s;")
    result = execute_query(query, ("%Johns Hopkins%", "%Computer Science%", "Masters"))
    answer = result[0][0] if result else "Query Failed"
    label = "7. Johns Hopkins Masters in Computer Science Applicants:"
    return f"{label} {answer}"

def main():
    """Main function to run and print all predefined queries."""
    print("Running database queries...")
    print("=" * 30)
    print(_get_query_1_output())
    print("-" * 30)
    print(_get_query_2_output())
    print("-" * 30)
    print(_get_query_3_output())
    print("-" * 30)
    print(_get_query_4_output())
    print("-" * 30)
    print(_get_query_5_output())
    print("-" * 30)
    print(_get_query_6_output())
    print("-" * 30)
    print(_get_query_7_output())
    print("=" * 30)

if __name__ == "__main__":
    main()
