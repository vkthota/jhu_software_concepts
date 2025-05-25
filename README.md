# Project Setup and Running Instructions

Welcome, collaborator! Follow these steps to set up and run the Personal Website project on your local machine.

# Running the Personal Website Application

1. Clone the Repository

Run the below commands in the terminal.

git clone https://github.com/vkthota/jhu_software_concepts.git
cd jhu_software_concepts



2. Set Up Environment & Install Dependencies
It's recommended to use a Python virtual environment.

From the project's root directory (jhu_software_concepts):

#Command to Create and activate a virtual environment
python -m venv venv 

#Commad to activate
source venv/bin/activate  # macOS/Linux command to activate
.\venv\Scripts\activate   # Windows command to activate

# Install required packages
pip install -r requirements.txt


3. Run the Application
The main application script run.py is located in the module_1 subdirectory.

# Navigate to the module_1 directory
cd module_1

# Run the application
python run.py
You should see output indicating the Flask development server is running, typically on http://127.0.0.1:8000/ or http://0.0.0.0:8000/.


4. Access in Browser
Open your web browser and navigate to:

http://127.0.0.1:8000

To stop the server, press Ctrl+C in the terminal where it's running.
