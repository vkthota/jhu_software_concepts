## Module 3: Database and Analysis
This module takes the JSON data from module 2, loads it into a database, and analyzes it.

* `load_data.py`: Connects to a PostgreSQL database and loads the `applicant_data.json` file.
* `query_data.py`: Connects to the database and runs 7 analytical queries required by the assignment.
* `app.py`: Flask web application that runs the queries and displays the results on a webpage.

### How to Run
1. Install dependencies: `pip install -r module_3/requirements.txt`.
2. load_data.py will populate the replit PostgresSQL database. This is a relational database. The data is coming from the json file named applicant_data.json.
3. Run the Flask web application: `python module_3/app.py`.