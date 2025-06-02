import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

# --- Constants for scrape.py --- 
GRADCAFE_BASE_URL = "https://www.thegradcafe.com"
HTTP_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
DETAIL_DIV_CLASSES = "tw-inline-flex tw-items-center tw-rounded-md tw-bg-stone-50 tw-px-2 tw-py-1 tw-text-xs tw-font-medium tw-text-stone-700 tw-ring-1 tw-ring-inset tw-ring-stone-600/20".split()

# --- "Private" Helper Functions ---
def _get_empty_admission_entry():
    return {
        "University": "N/A", "URL Link": "N/A", "Program Field": "N/A", "Program Degree Level": "N/A",
        "Date Added": "N/A", "Applicant Status": "N/A", "Decision Date String": "N/A",
        "Decision Full Text": "N/A", "GPA": "N/A", "GRE Verbal": "N/A", "GRE Quant": "N/A",
        "GRE AWA": "N/A", "GRE Total or General": "N/A", "TOEFL": "N/A", "Student Status": "N/A",
        "Program Start Term": "N/A", "Comments Cue": "N/A", "Comments": "N/A"
    }

def _fetch_page_soup(url):
    # print(f"Fetching URL: {url}") # minimal for this module
    try:
        response = requests.get(url, headers=HTTP_HEADERS, timeout=10)
        response.raise_for_status()
        # print("Successfully fetched the page.")
        return BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.Timeout: print(f"Error: The request timed out for {url}")
    except requests.exceptions.HTTPError as e: print(f"Error: HTTP Error occurred for {url}: {e}")
    except requests.exceptions.RequestException as e: print(f"Error: Could not fetch URL {url}: {e}")
    except Exception as e: print(f"An unexpected error occurred during fetch for {url}: {e}")
    return None

def _parse_entry_details(elements_to_search, entry_data_dict):
    for detail_div in elements_to_search:
        text_content = detail_div.get_text(strip=True)
        parsed_this_detail = False

        if entry_data_dict.get("GPA", "N/A") == "N/A":
            gpa_match = re.search(r'GPA\s*([\d\.]+)(?:\s*/\s*[\d\.]+)?', text_content, re.IGNORECASE)
            if gpa_match: entry_data_dict["GPA"] = gpa_match.group(1); parsed_this_detail = True
        if parsed_this_detail: continue

        if "GRE" in text_content.upper():
            updated_any_gre = False
            if entry_data_dict.get("GRE Verbal", "N/A") == "N/A":
                v_match = re.search(r'V\s*[:\s]?\s*(\d{2,3})', text_content, re.IGNORECASE)
                if v_match: entry_data_dict["GRE Verbal"] = v_match.group(1); updated_any_gre = True
            if entry_data_dict.get("GRE Quant", "N/A") == "N/A":
                q_match = re.search(r'Q\s*[:\s]?\s*(\d{2,3})', text_content, re.IGNORECASE)
                if q_match: entry_data_dict["GRE Quant"] = q_match.group(1); updated_any_gre = True
            if entry_data_dict.get("GRE AWA", "N/A") == "N/A":
                aw_match = re.search(r'AW\s*[:\s]?\s*(\d\.\d|\d)', text_content, re.IGNORECASE)
                if aw_match: entry_data_dict["GRE AWA"] = aw_match.group(1); updated_any_gre = True
            if not updated_any_gre and entry_data_dict.get("GRE Total or General", "N/A") == "N/A":
                general_gre_match = re.search(r'GRE\s+(\d{3})', text_content, re.IGNORECASE)
                if general_gre_match: entry_data_dict["GRE Total or General"] = general_gre_match.group(1); updated_any_gre = True
            if updated_any_gre: parsed_this_detail = True
        if parsed_this_detail: continue

        if entry_data_dict.get("TOEFL", "N/A") == "N/A":
            toefl_match = re.search(r'TOEFL\s*[:\s]?\s*(\d{2,3})', text_content, re.IGNORECASE)
            if toefl_match: entry_data_dict["TOEFL"] = toefl_match.group(1); parsed_this_detail = True
        if parsed_this_detail: continue

        if entry_data_dict.get("Program Start Term", "N/A") == "N/A":
            term_match = re.search(r'(Fall|Spring|Summer|Winter)\s*(\d{4})', text_content, re.IGNORECASE)
            if term_match: entry_data_dict["Program Start Term"] = f"{term_match.group(1)} {term_match.group(2)}"; parsed_this_detail = True
        if parsed_this_detail: continue

        if entry_data_dict.get("Student Status", "N/A") == "N/A":
            if "international" in text_content.lower(): entry_data_dict["Student Status"] = "International"; parsed_this_detail = True
        if parsed_this_detail: continue

        decision_keywords = ["accepted", "rejected", "wait listed", "admitted", "denied"]
        if any(keyword in text_content.lower() for keyword in decision_keywords):
            if entry_data_dict.get("Applicant Status") == "Other" or entry_data_dict.get("Applicant Status") == "N/A" or \
               text_content.lower() != entry_data_dict.get("Decision Full Text","").lower():
                entry_data_dict["Decision Full Text"] = text_content
                status_match = re.match(r'(Accepted|Rejected|Wait listed|Admitted|Denied|Other)(?:\s+on\s+(.*))?', text_content, re.IGNORECASE)
                if status_match:
                    entry_data_dict["Applicant Status"] = status_match.group(1).strip()
                    entry_data_dict["Decision Date String"] = status_match.group(2).strip() if status_match.group(2) else "N/A"
                else: entry_data_dict["Applicant Status"] = "Other"
            parsed_this_detail = True
        if parsed_this_detail: continue

        if entry_data_dict.get("Comments Cue", "N/A") == "N/A":
            if "see more" in text_content.lower() or "report" in text_content.lower():
                entry_data_dict["Comments Cue"] = text_content; parsed_this_detail = True

def _parse_main_row_data(cells, entry_data):
    if len(cells) > 0:
        school_name_div = cells[0].find('div', class_=lambda c: c and 'tw-font-medium' in c.split() and 'tw-text-gray-900' in c.split())
        if school_name_div: entry_data["University"] = school_name_div.get_text(strip=True)
    if len(cells) > 1:
        program_cell = cells[1]
        program_name_span = program_cell.select_one('div.tw-text-gray-900 span')
        if program_name_span: entry_data["Program Field"] = program_name_span.get_text(strip=True)
        degree_level_span = program_cell.find('span', class_='tw-text-gray-500')
        if degree_level_span:
            degree_text = degree_level_span.get_text(strip=True)
            if degree_text.upper() in ["MASTERS", "PHD", "MS", "MA", "MENG", "MFA", "LLM", "MBA"]:
                entry_data["Program Degree Level"] = degree_text
        elif entry_data.get("Program Field", "N/A") == "N/A":
            entry_data["Program Field"] = program_cell.get_text(separator=" ", strip=True)
    if len(cells) > 2: entry_data["Date Added"] = cells[2].get_text(strip=True)
    if len(cells) > 3:
        decision_cell = cells[3]
        decision_text_val = ""
        decision_div = decision_cell.find('div', class_=lambda c: c and 'tw-inline-flex' in c.split())
        if decision_div: decision_text_val = decision_div.get_text(strip=True)
        else: decision_text_val = decision_cell.get_text(strip=True)
        entry_data["Decision Full Text"] = decision_text_val
        status_match = re.match(r'(Accepted|Rejected|Wait listed|Admitted|Denied|Other)(?:\s+on\s+(.*))?', decision_text_val, re.IGNORECASE)
        if status_match:
            entry_data["Applicant Status"] = status_match.group(1).strip()
            entry_data["Decision Date String"] = status_match.group(2).strip() if status_match.group(2) else "N/A"
        elif decision_text_val: entry_data["Applicant Status"] = "Other"; entry_data["Decision Full Text"] = decision_text_val

    if len(cells) >= 5:
        actions_cell = cells[4]
        link_tag = actions_cell.find('a', href=re.compile(r'^/result/\d+'))
        if link_tag:
            href = link_tag.get('href')
            if href: entry_data["URL Link"] = GRADCAFE_BASE_URL + href

def _parse_page_entries(soup):
    page_entries = []
    temp_entry = {}
    results_table = soup.find('table', class_='tw-min-w-full')
    if not results_table: return page_entries
    table_body = results_table.find('tbody')
    if not table_body: return page_entries
    html_rows = table_body.find_all('tr')

    for i, row_tag in enumerate(html_rows):
        cells = row_tag.find_all('td')
        current_row_classes = row_tag.get('class', [])
        is_main_data_row = len(cells) >= 4
        is_detail_or_comment_row = (len(cells) == 1 and 'tw-border-none' in current_row_classes and cells[0].get('colspan'))

        if is_main_data_row:
            if temp_entry.get('University') and temp_entry['University'] != "N/A":
                page_entries.append(temp_entry)
            temp_entry = _get_empty_admission_entry() # Use helper
            _parse_main_row_data(cells, temp_entry) # Use helper
        
        elif is_detail_or_comment_row:
            if temp_entry.get('University') and temp_entry['University'] != "N/A":
                detail_cell = cells[0]
                detail_divs_found = detail_cell.find_all('div', class_=DETAIL_DIV_CLASSES)
                pill_texts_in_this_cell = []
                if detail_divs_found:
                    _parse_entry_details(detail_divs_found, temp_entry) # Use helper
                    for pill_div in detail_divs_found:
                        pill_text = pill_div.get_text(strip=True)
                        if pill_text: pill_texts_in_this_cell.append(pill_text)
                
                actual_comment_segments = []
                for element in detail_cell.children:
                    current_text_from_element = ""
                    is_direct_child_a_pill_div = (element.name == 'div' and element.get('class') == DETAIL_DIV_CLASSES)
                    if is_direct_child_a_pill_div: continue

                    if isinstance(element, str): current_text_from_element = element.strip()
                    elif element.name == 'p':
                        p_text_candidate = element.get_text(separator=' ', strip=True)
                        if p_text_candidate not in pill_texts_in_this_cell: current_text_from_element = p_text_candidate
                    elif element.name is not None:
                         other_text_candidate = element.get_text(separator=' ', strip=True)
                         if other_text_candidate and other_text_candidate not in pill_texts_in_this_cell: current_text_from_element = other_text_candidate
                    if current_text_from_element: actual_comment_segments.append(current_text_from_element)
                
                full_prose_comment = "\n".join(filter(None, actual_comment_segments)).strip()
                if full_prose_comment:
                    is_just_a_parsed_value = False
                    parsed_values_for_check = [temp_entry.get(k) for k in ["GPA", "GRE Verbal", "GRE Quant", "GRE AWA", "GRE Total or General", "TOEFL", "Student Status", "Program Start Term", "Decision Full Text", "Comments Cue"]]
                    for val in parsed_values_for_check:
                        if val and val != "N/A" and str(val).strip() == full_prose_comment: is_just_a_parsed_value = True; break
                    if not is_just_a_parsed_value and len(full_prose_comment) > 15 : 
                        temp_entry["Comments"] = full_prose_comment

    if temp_entry.get('University') and temp_entry['University'] != "N/A":
        page_entries.append(temp_entry)
    return page_entries

# --- Public Scraping Function ---
def scrape_data(initial_search_url, max_pages, max_entries):
    all_entries = []
    current_page_url = initial_search_url
    print(f"Starting scrape. Max pages: {max_pages}, Max entries: {max_entries}")

    for page_num in range(1, max_pages + 1):
        if page_num > 1:
            separator = '&' if '?' in initial_search_url else '?'
            if initial_search_url.endswith('?'): current_page_url = f"{initial_search_url}p={page_num}"
            elif '?' not in initial_search_url : current_page_url = f"{initial_search_url}?p={page_num}"
            else: current_page_url = f"{initial_search_url}&p={page_num}"
        
        if not current_page_url: break
        print(f"\n--- Scraping Page {page_num} from URL: {current_page_url} ---")
        soup = _fetch_page_soup(current_page_url) # Use helper
        if not soup: print(f"Failed to fetch page {page_num}. Assuming end of results or issue."); break
        
        page_entries = _parse_page_entries(soup) # Use helper
        
        if not page_entries and page_num > 1: print(f"Found no entries on page {page_num}. Assuming end of actual results."); break
        all_entries.extend(page_entries)
        print(f"Parsed {len(page_entries)} entries from this page. Total entries so far: {len(all_entries)}")
        if len(all_entries) >= max_entries: print(f"Reached entry limit of {max_entries}. Stopping."); break
        if page_num == max_pages: print(f"Reached max_pages limit of {max_pages}. Stopping further pagination."); break
    return all_entries