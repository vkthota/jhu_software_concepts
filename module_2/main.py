# main.py
from scrape import scrape_data # scrape.py contains scrape_data
from clean import clean_data     # Aclean.py contains clean_data
from file_ops import save_data, load_data # file_ops.py for these

# --- Configuration for the main run ---
BASE_SEARCH_URL = "https://www.thegradcafe.com/survey/?q=Computer+Science"
OUTPUT_FILENAME = "applicant_data.json"
MAX_PAGES_TO_SCRAPE = 3  # Adjust as needed
MAX_ENTRIES_TO_SCRAPE = 10000 # Assignment limit

def main_process():
    print("Starting GradCafe Scraper...")
    
    # Call scrape_data from scrape.py
    raw_data = scrape_data(BASE_SEARCH_URL, max_pages=MAX_PAGES_TO_SCRAPE, max_entries=MAX_ENTRIES_TO_SCRAPE)
    
    if raw_data:
        # print(f"Raw data contains {len(raw_data)} entries.") # Optional debug
        
        # Call clean_data from clean.py
        cleaned_entries = clean_data(raw_data)
        # print(f"Cleaned data contains {len(cleaned_entries)} entries.") # Optional debug
        
        # Call save_data from file_ops.py
        save_data(cleaned_entries, OUTPUT_FILENAME)
        
        
    else: 
        print("No data was scraped.")
    
    print("\nScraping process finished.")

if __name__ == '__main__':
    main_process()