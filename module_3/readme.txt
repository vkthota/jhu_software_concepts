## Module 3: Database and Analysis
This module takes the clean JSON data, loads it into a database, and analyzes it.

* `load_data.py`: Connects to a PostgreSQL database and loads the `applicant_data.json` file.
* `query_data.py`: Connects to the database and runs 7 analytical queries required by the assignment.
* `app.py`: A simple Flask web application that runs the queries and displays the results on a webpage.

### How to Run
1.  Run Module 2 (`python module_2/main.py`) to generate `applicant_data.json`.
2.  Move the generated `applicant_data.json` into the `module_3` folder.
3.  Set up the PostgreSQL database and add the `DATABASE_URL` to your environment secrets.
4.  Install Module 3 dependencies: `pip install -r module_3/requirements.txt`.
5.  Load the data into the database: `python module_3/load_data.py`.
6.  Run the Flask web application: `python module_3/app.py`.