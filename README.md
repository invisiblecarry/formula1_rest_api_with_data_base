# Formula 1 REST API with Database

## Overview
This project provides a RESTful API for accessing Formula 1 racing data stored in a database. It includes scripts for importing data into the database and a Python-based web server that serves the data through an API.

## Repository Contents
- `data`: Data files related to Formula 1.
- `database`: Scripts and files for setting up and managing the database.
- `tests`: Test scripts for the application's functionality.
- `.gitignore`: Specifies which files and directories to ignore in Git.
- `import_script.py`: Script for importing data into the database.
- `requirements.txt`: Required Python packages for the project.
- `rest_api_formula1_report.py`: The main script that runs the REST API server.

## Technology
The entire codebase is in Python, ensuring consistency and ease of use for Python developers.

## Setup and Running
1. Clone the repository:
git clone https://github.com/invisiblecarry/formula1_rest_api_with_data_base.git
2. Install the required packages:
pip install -r requirements.txt
3. Run the import script to set up the database:
python import_script.py
4. Start the server:
python rest_api_formula1_report.py

## API Usage
After starting the server, the API will be accessible at the configured port. Use the endpoints to access Formula 1 data.

## Contributing
Contributions are welcome. Please ensure to write tests for new features and run existing tests before making a pull request.

## License
[LICENSE](LICENSE)

## Contact
Baranov Viacheslav - [https://www.linkedin.com/in/viacheslav-baranov-ab2a0b290/

