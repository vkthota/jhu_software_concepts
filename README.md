These instructions are for Windows.

Step 1 - Open terminal

Step 2 - Clone the repository using the below command
- git clone https://github.com/vkthota/jhu_software_concepts.git

Step 3 - change directory by using the below command
- cd jhu_software_concepts

step 4 - setup environment and install dependencies
run the below command to activate a virtual environment
- python -m venv venv 

activate the virtual encironment by using the below command
.\venv\Scripts\activate

Step 5 - Install required packages using the below command
- pip install -r requirements.txt

Step 6 - Run the Application
The main application script run.py is located in the module_1 subdirectory.

Navigate to the module_1 directory using the below command
- cd module_1

Run the application using the below command
- python run.py
- You should see output indicating the Flask development server is running, typically on http://127.0.0.1:8000/ or http://0.0.0.0:8000/.

Step 7 - Access in Browser
Open your web browser and navigate to:

http://127.0.0.1:8000

To stop the server, press Ctrl+C in the terminal where it's running.
