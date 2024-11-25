Title of the Task
"Detecting DNS information from the website "
Index:
- [Introduction](#introduction)
- [How to Run the Program](#how-to-run-the-program)
- [Dependencies Installed](#dependencies-installed)
- [API Endpoints and Usage](#api-endpoints-and-usage)
- [Contributors and Their Contributions](#contributors-and-their-contributions)
- [File Descriptions](#file-descriptions)
- [Working Program Images](#working-program-images)

How to Run the Program:

Install Python (3.x).

Set up a virtual environment in terminal:
cd path/to/current/project/folder

python -m venv venv

venv\Scripts\activate     # For Windows

Install dependencies:
pip install -r requirements.txt

Start the Flask app:
python app.py

Use Postman or cURL to test the endpoints.
Dependencies Installed
Flask
Selenium
tldextract
pymongo
dnspython

Install microsoftedge driver :
Step 1: Download Microsoft Edge WebDriver
Visit the official Microsoft Edge WebDriver download page.
Download the version of Edge WebDriver that matches your Microsoft Edge browser version.
Check your Edge version by navigating to edge://settings/help in Edge.
Download the corresponding WebDriver for your operating system.

Step 2: Add Edge WebDriver to PATH
Extract the downloaded msedgedriver executable.
Copy the path to the folder containing msedgedriver.exe.
Add it to your system's PATH:
Windows:
Press Win + R, type sysdm.cpl, and press Enter.
Go to the Advanced tab and click Environment Variables.
Under System variables, find and edit the Path variable.
Add the folder path containing msedgedriver.exe.
Click OK to save changes.
Restart any open command prompts or terminals.

API Endpoints and Usage
use postman 



POST /search
Example:http://127.0.0.1:5000/search

Description: Searches Google for the term and stores DNS details.
Request Body:
json
Copy code
{
  "search_term": "example domain"
}
Response:
json
Copy code
{
  "message": "DNS info stored successfully",
  "data": {
    "subdomain": "",
    "domain": "example.com",
    "ip_addresses": ["93.184.216.34"]
  }
}


GET /dns-info
Example:http://127.0.0.1:5000/search

Description: Fetches all stored DNS data.
Response:
json
Copy code
[
  {
    "subdomain": "",
    "domain": "example.com",
    "ip_addresses": ["93.184.216.34"]
  }
]
Contributors:
SIBBALA CHANDANA

Contributions:
Developed the Flask API for DNS resolution.
Integrated Selenium for Google search functionality.
Designed MongoDB schema for storing DNS information.
Tested API endpoints and validated results.
Wrote detailed project documentation.

File Descriptions
app.py: Main Flask application.
msedgedriver.exe: WebDriver for Selenium.
requirements.txt: Python dependencies.
README.md: Project documentation.