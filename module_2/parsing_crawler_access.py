from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

# the base URL for the site
site_url = "https://www.thegradcafe.com/"

# Define agent string 
user_agent = "agentvt" # 

# Paths to check (
paths_to_check = [
    "/",  # Root of the site
    "/cgi-bin/",
    "/admin/",
    "/survey/", # Main survey/results path
    "/survey/index.php",
    "/survey/index.php?q=Computer+Science", # A specific search result page
    "/result/986065" # An example individual result page
]

# Construct the full URL for robots.txt
robots_txt_url = urljoin(site_url, "robots.txt")

# Initialize the RobotFileParser
parser = RobotFileParser()
parser.set_url(robots_txt_url)

try:
    print(f"Attempting to fetch and read: {robots_txt_url}")
    parser.read()
    print("Successfully read robots.txt\n")

    print(f"Checking access for user agent: '{user_agent}'\n")
    for path in paths_to_check:
        # Construct the full path URL to check (can_fetch expects a full URL or absolute path)
        # checking against the absolute path on the site
        full_path_to_check_on_site = urljoin(site_url, path.lstrip('/')) # Ensure path is relative to root

        can_fetch_status = parser.can_fetch(user_agent, full_path_to_check_on_site)
        print(f"Can fetch '{path}'? : {can_fetch_status}")

except Exception as e:
    print(f"An error occurred: {e}")
    print("Could not fetch or parse robots.txt. It's advisable to assume restricted access or manually check.")