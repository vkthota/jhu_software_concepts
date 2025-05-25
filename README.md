Markdown

# Running the Personal Website Application

These instructions are for instructors grading this project. It's assumed you have Python 3, pip, and Git installed and are familiar with cloning repositories and virtual environments.

## 1. Clone the Repository

If you haven't already, clone the repository and navigate into its root directory:

```bash
git clone [https://github.com/vkthota/jhu_software_concepts.git](https://github.com/vkthota/jhu_software_concepts.git)
cd jhu_software_concepts
2. Set Up Environment & Install Dependencies
It's recommended to use a Python virtual environment to manage project dependencies.

A. Create and Activate Virtual Environment (Optional but Recommended)

From the project's root directory (jhu_software_concepts):

Create the virtual environment (e.g., named venv):

Bash

python -m venv venv
Activate it:

Windows (PowerShell/CMD):
PowerShell

.\venv\Scripts\activate
macOS/Linux (bash/zsh):
Bash

source venv/bin/activate
B. Install Required Packages

Once your virtual environment is activated (or if you're proceeding without one), install the dependencies.
From the project's root directory (jhu_software_concepts):

Bash

pip install -r module_1/requirements.txt
(Note: This command assumes your requirements.txt file is located in the jhu_software_concepts/module_1/ directory. If it's directly in the root jhu_software_concepts/ directory, change the command above to pip install -r requirements.txt.)

3. Run the Application
The main application script run.py is located in the module_1 subdirectory.

Navigate to the module_1 directory (if you are still in the project root):

Bash

cd module_1
Run the application:

Bash

python run.py
You should see output indicating the Flask development server is running, typically on http://127.0.0.1:8000/ or http://0.0.0.0:8000/.

4. Access in Browser
Open your web browser and navigate to:

http://127.0.0.1:8000

To stop the server, press Ctrl+C in the terminal where it's running.
