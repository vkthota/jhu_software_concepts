# module_3/app.py

from flask import Flask, render_template
import os
import psycopg2

app = Flask(__name__)

def execute_query(query):
    """A reusable function to connect and run a query."""
    db_url = os.environ.get('DATABASE_URL')
    try:
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Database query error: {e}")
    return []

@app.route('/')
def index():
    """
    This function runs when a user visits the main page.
    It executes all 7 queries and passes the results to the HTML template.
    """
    # A list to hold all our question and answer pairs
    query_results = []

    # --- Query 1 ---
    query_1 = "SELECT COUNT(*) FROM applicants WHERE semester_start = 'Fall 2025';"
    result_1 = execute_query(query_1)
    answer_1 = f"{result_1[0][0]:,}" if result_1 else "Query Failed"
    query_results.append(("1. How many applicants for Fall 2025?", answer_1))

    # --- Query 2 ---
    query_2 = "SELECT 100.0 * COUNT(*) FILTER (WHERE student_type = 'International') / COUNT(*) FROM applicants;"
    result_2 = execute_query(query_2)
    answer_2 = f"{result_2[0][0]:.2f}%" if result_2 and result_2[0][0] is not None else "Query Failed"
    query_results.append(("2. Percentage of International Students:", answer_2))

    # --- Query 3 ---
    query_3 = "SELECT AVG(gpa), AVG(gre_total), AVG(gre_v), AVG(gre_q), AVG(gre_aw) FROM applicants;"
    result_3 = execute_query(query_3)
    answer_3_list = []
    if result_3 and result_3[0] is not None:
        avg_gpa, avg_gre_total, avg_gre_v, avg_gre_q, avg_gre_aw = result_3[0]
        answer_3_list.append(f"GPA: {avg_gpa:.2f}" if avg_gpa else "GPA: N/A")
        answer_3_list.append(f"GRE Total: {avg_gre_total:.2f}" if avg_gre_total else "GRE Total: N/A")
        answer_3_list.append(f"GRE Verbal: {avg_gre_v:.2f}" if avg_gre_v else "GRE Verbal: N/A")
        answer_3_list.append(f"GRE Quant: {avg_gre_q:.2f}" if avg_gre_q else "GRE Quant: N/A")
        answer_3_list.append(f"GRE AW: {avg_gre_aw:.2f}" if avg_gre_aw else "GRE AW: N/A")
    query_results.append(("3. Average Scores (All Terms):", " | ".join(answer_3_list) if answer_3_list else "No Data"))

    # --- Query 4 ---
    query_4 = "SELECT AVG(gpa) FROM applicants WHERE student_type = 'American' AND semester_start = 'Fall 2025';"
    result_4 = execute_query(query_4)
    answer_4 = f"{result_4[0][0]:.2f}" if result_4 and result_4[0][0] is not None else "No Data"
    query_results.append(("4. Avg GPA of American Students in Fall 2025:", answer_4))

    # --- Query 5 ---
    query_5 = "SELECT 100.0 * COUNT(*) FILTER (WHERE applicant_status = 'Accepted') / NULLIF(COUNT(*), 0) FROM applicants WHERE semester_start = 'Fall 2025';"
    result_5 = execute_query(query_5)
    answer_5 = f"{result_5[0][0]:.2f}%" if result_5 and result_5[0][0] is not None else "No Data"
    query_results.append(("5. Percent Acceptances for Fall 2025:", answer_5))

    # --- Query 6 ---
    query_6 = "SELECT AVG(gpa) FROM applicants WHERE semester_start = 'Fall 2025' AND applicant_status = 'Accepted';"
    result_6 = execute_query(query_6)
    answer_6 = f"{result_6[0][0]:.2f}" if result_6 and result_6[0][0] is not None else "No Data"
    query_results.append(("6. Avg GPA of Accepted Students in Fall 2025:", answer_6))

    # --- Query 7 ---
    query_7 = "SELECT COUNT(*) FROM applicants WHERE university ILIKE '%Johns Hopkins%' AND program_name ILIKE '%Computer Science%' AND degree = 'Masters';"
    result_7 = execute_query(query_7)
    answer_7 = result_7[0][0] if result_7 else "Query Failed"
    query_results.append(("7. Johns Hopkins Masters in Computer Science Applicants:", answer_7))

    # render_template looks for files in a 'templates' folder
    return render_template('index.html', query_results=query_results)

if __name__ == '__main__':
    # host='0.0.0.0' is required to run in most cloud environments (like Replit)
    app.run(host='0.0.0.0', port=8080)
