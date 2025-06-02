1. Name: Vijay Thota
   JHED ID: vthota1

2. Module Info
   ------------
   Module 2
   Assignment: Web Scraper for GradCafe Data
   Due Date: Due Jun 1 at 11:59pm

3. Approach
   ---------
   This project implements a web scraper in Python to extract graduate school admission results from The GradCafe (thegradcafe.com) for a specified query (defaulting to "Computer Science"). The process is broken down into several key modules and steps:

   a. Project Structure:
      - `main.py`: Orchestrates the entire scraping, cleaning, and saving process. Defines global constants like the base URL and output filename.
      - `scrape.py`: Contains the core scraping logic. This includes:
          - `_fetch_page_soup(url)`: Fetches the HTML content of a given URL using the `requests` library and parses it into a BeautifulSoup object. It handles HTTP errors and timeouts.
          - `_parse_main_row_data(cells, entry_data)`: Extracts data from the main cells of a table row (University, Program, Date Added, Decision, URL Link to entry).
          - `_parse_entry_details(elements_to_search, entry_data_dict)`: Parses "pill-style" detail `divs` (containing GPA, GRE scores, Term, Status, etc.) found within detail/comment rows. Uses regular expressions to extract specific values.
          - `_parse_page_entries(soup)`: Identifies main data rows and subsequent detail/comment rows within a single HTML page (soup object). It manages the association of details and comments with their corresponding main entry. It calls `_parse_main_row_data` and `_parse_entry_details`.
          - `scrape_data(initial_search_url, max_pages, max_entries)`: The main public scraping function. It handles pagination by constructing URLs for subsequent pages (e.g., appending "&p=PAGENUMBER") and calls `_parse_page_entries` for each page, up to the defined limits.
      - `clean.py`: Contains the `clean_data(entries_list)` function. Currently, this function performs minimal cleaning, such as removing the "Other Misc Details" field if it was populated (though recent versions aim to prevent its population with redundant data) and ensuring the "Comments" field is a string.
      - `file_ops.py`: Contains utility functions:
          - `save_data(entries_list, filename)`: Saves the provided list of dictionaries to a JSON file with indentation for readability.
          - `load_data(filename)`: Loads data from a specified JSON file.
      - `robot_checker.py`: A separate utility script to check `robots.txt` compliance for given paths using `urllib.robotparser`.
      - `applicant_data.json`: The default output file where scraped data is stored.

   b. Scraping Process:
      - The scraper starts with a base search URL on The GradCafe.
      - It fetches the first page and parses it. Main admission entries are identified (typically rows with >= 4 cells).
      - It then looks for an immediately following row with a specific structure (class 'tw-border-none' and a single cell, often with a colspan) which contains additional details ("pills" like GPA, GRE, term, status) and potentially long-form comments.
      - Specific "pill" details are extracted using their unique shared CSS class structure (`DETAIL_DIV_CLASSES`) and then parsed using regular expressions.
      - Long-form comments are extracted by taking the text content of the detail/comment row's cell and attempting to exclude text that was already identified as part of a "pill." If no distinct prose is found, the "Comments" field defaults to "N/A".
      - The "URL Link" to the individual GradCafe result page is extracted from an icon (usually a comment icon) in the 5th cell of main data rows.
      - The process iterates through pages by constructing page URLs (e.g., adding `&p=2`, `&p=3`, etc.) up to a configurable maximum number of pages or entries.

   c. Data Storage:
      - All extracted data for each admission entry is stored in a Python dictionary.
      - The collection of all entries (a list of these dictionaries) is then saved as a JSON array to a file (default: `gradcafe_admissions_data.json`).

   d. Key Libraries Used:
      - `requests`: For making HTTP requests to fetch web page content.
      - `BeautifulSoup4` (from `bs4`): For parsing HTML content.
      - `re`: For regular expression matching to extract specific data patterns (e.g., scores, dates).
      - `json`: For saving the extracted data to a JSON file and loading it.
      - `urllib.robotparser` and `urllib.parse`: Used in `robot_checker.py`.

4. Setup and Execution
   --------------------
   To run this web scraper after cloning it from GitHub:

   a. Prerequisites:
      - Ensure you have Python 3.9 or newer installed on your system.
      - Ensure `pip` (Python package installer) is available.

   b. Instructions:
      1. **Clone the Repository:**
         Open your terminal or command prompt and run:
         ```
         git clone https://github.com/vkthota/jhu_software_concepts.git
         ```

      2. **Navigate to the Project Directory:**
         Change into the project folder 
         ```
         cd module_2
         ```

      3. **(Recommended) Create and Activate a Virtual Environment:**
         
         - To create a virtual environment (e.g., named `venv`):
           ```
           python -m venv venv
           ```
         - To activate it:
           - On macOS and Linux:
             ```
             source venv/bin/activate
             ```
           - On Windows:
             ```
             venv\Scripts\activate
             ```

      4. **Install Dependencies:**
         Install the required Python packages using the `requirements.txt` file:
         ```
         pip install -r requirements.txt
         ```

      5. **Run the Scraper:**
         Execute the `main.py` script to start the scraping process:
         ```
         python main.py
         ```

      6. **Output:**
         - The script will print progress to the console.
         - Upon completion, a JSON file (default name: `applicant_data.json`, but configurable in `main.py`) will be created in the project directory containing the scraped admission data. In main.p, MAX_PAGES_TO_SCRAPE should be set to 500 to get 10000 applicant data.
         - The `robot_checker.py` script can be run separately (`python robot_checker.py`) to verify `robots.txt` permissions for specific paths on The GradCafe.


5. Known Bugs 
   --------------------------
	N/A