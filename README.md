Markdown

# Running the Personal Website Application

## 1. Clone the Repository

If you haven't already, clone the repository:

```bash
git clone [https://github.com/vkthota/jhu_software_concepts.git](https://github.com/vkthota/jhu_software_concepts.git)
cd jhu_software_concepts
2. Set Up Environment & Install Dependencies
It's recommended to use a Python virtual environment.

From the project's root directory (jhu_software_concepts):

Bash

# Optional: Create and activate a virtual environment
# python -m venv venv
# source venv/bin/activate  # macOS/Linux
# .\venv\Scripts\activate   # Windows

# Install required packages
pip install -r requirements.txt
3. Run the Application
The main application script run.py is located in the module_1 subdirectory.

Bash

# Navigate to the module_1 directory
cd module_1

# Run the application
python run.py
You should see output indicating the Flask development server is running, typically on http://127.0.0.1:8000/ or http://0.0.0.0:8000/.

4. Access in Browser
Open your web browser and navigate to:

http://127.0.0.1:8000

To stop the server, press Ctrl+C in the terminal where it's running.
