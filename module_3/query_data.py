# query_data.py (Updated for Fall 2025 Analysis)

import os
import psycopg2

def execute_query(query):
    """Connects, runs a query, and returns results."""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("Error: DATABASE_URL secret not found.")
        return None
    try:
        with psycopg2.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()
    except psycopg2.Error as e:
        print(f"Database query error: {e}")
    return None

if __name__ == "__main__":

    print("Running database queries for Fall 2025...")
    print("=" * 30)

    # --- Query 1: How many entries for Fall 2025? ---
    query_1 = "SELECT COUNT(*) FROM applicants WHERE term = 'Fall 2025';"
    result_1 = execute_query(query_1)
    count_fall_2025 = result_1[0][0] if result_1 else "Query Failed"
    print(f"1. Applicants for Fall 2025: {count_fall_2025}")
    print("-" * 30)

    # --- Query 2: What percentage of entries are from international students? (Unaffected by term) ---
    query_2 = "SELECT 100.0 * COUNT(*) FILTER (WHERE us_or_international = 'International') / COUNT(*) FROM applicants;"
    result_2 = execute_query(query_2)
    percent_international = f"{result_2[0][0]:.2f}%" if result_2 and result_2[0][0] is not None else "Query Failed"
    print(f"2. Percentage of International Students: {percent_international}")
    print("-" * 30)

    # --- Query 3: What is the average GPA, GRE, GRE V, GRE AW? (Unaffected by term) ---
    query_3 = "SELECT AVG(gpa), AVG(gre), AVG(gre_v), AVG(gre_aw) FROM applicants;"
    result_3 = execute_query(query_3)
    print("3. Average Scores (All Terms):")
    if result_3:
        avg_gpa, avg_gre, avg_gre_v, avg_gre_aw = result_3[0]
        print(f"   - GPA: {avg_gpa:.2f}" if avg_gpa is not None else "   - GPA: N/A")
        print(f"   - GRE Total: {avg_gre:.2f}" if avg_gre is not None else "   - GRE Total: N/A")
        print(f"   - GRE Verbal: {avg_gre_v:.2f}" if avg_gre_v is not None else "   - GRE Verbal: N/A")
        print(f"   - GRE AW/Quant: {avg_gre_aw:.2f}" if avg_gre_aw is not None else "   - GRE AW/Quant: N/A")
    else:
        print("   Query Failed or No Data")
    print("-" * 30)

    # --- Query 4: What is their average GPA of American students in Fall 2025? ---
    query_4 = """
    SELECT AVG(gpa) FROM applicants 
    WHERE us_or_international = 'American or Other' AND term = 'Fall 2025';
    """
    result_4 = execute_query(query_4)
    avg_gpa_american_fall25 = f"{result_4[0][0]:.2f}" if result_4 and result_4[0][0] is not None else "No Data"
    print(f"4. Avg GPA of American Students in Fall 2025: {avg_gpa_american_fall25}")
    print("-" * 30)

    # --- Query 5: What percent of entries for Fall 2025 are Acceptances? ---
    query_5 = """
    SELECT 100.0 * COUNT(*) FILTER (WHERE status = 'Acceptance') / NULLIF(COUNT(*), 0) 
    FROM applicants WHERE term = 'Fall 2025';
    """
    result_5 = execute_query(query_5)
    percent_accepted_fall25 = f"{result_5[0][0]:.2f}%" if result_5 and result_5[0][0] is not None else "No Data"
    print(f"5. Percent Acceptances for Fall 2025: {percent_accepted_fall25}")
    print("-" * 30)

    # --- Query 6: What is the average GPA of applicants who applied for Fall 2025 who are Acceptances? ---
    query_6 = """
    SELECT AVG(gpa) FROM applicants 
    WHERE term = 'Fall 2025' AND status = 'Acceptance';
    """
    result_6 = execute_query(query_6)
    avg_gpa_accepted_fall25 = f"{result_6[0][0]:.2f}" if result_6 and result_6[0][0] is not None else "No Data"
    print(f"6. Average GPA of Accepted Students in Fall 2025: {avg_gpa_accepted_fall25}")
    print("-" * 30)

    # --- Query 7: How many entries are from applicants who applied to JHU for a masters degrees in Computer Science? ---
    query_7 = """
    SELECT COUNT(*) FROM applicants 
    WHERE program ILIKE '%JHU%' 
    AND program ILIKE '%Computer Science%' 
    AND degree = 'Masters';
    """
    result_7 = execute_query(query_7)
    count_jhu_cs_masters = result_7[0][0] if result_7 else "Query Failed"
    print(f"7. JHU Masters in Computer Science Applicants: {count_jhu_cs_masters}")
    print("=" * 30)