# py-web-hw14

  In this homework assignment, I continued to refine the REST API application from homework 13.
  Using Sphinx, I created the documentation for the homework assignment. To do this, I added basic modularizations to the required functions and methods of the docstrings classes.
  Covered the homework repository modules with unit tests using the Unittest framework. I used the example from the outline for the tests/test_unit_repository_notes.py module as a   basis
  Covered any routes/auth route with functional tests using the pytest framework.



## Contact API
A simple API for managing contacts, built using FastAPI.

Features:
CRUD operations for contacts.
Storage of contact's birthdate.
Automatic API documentation generation.
Utilizes PostgreSQL as the database.
Data validation using Pydantic.
Getting Started
Prerequisites:
Python 3.8 or newer.
PostgreSQL.
Installation:
Clone the repository:

git clone [your-repository-link]
Navigate to the project directory:

cd [your-project-name]
Install the required packages:

pip install -r requirements.txt
Update the config.ini with your PostgreSQL database details.

Run the FastAPI server:

uvicorn main:app --reload
Visit http://127.0.0.1:8000/docs in your browser to access the automatically generated API documentation.

Usage
You can perform CRUD operations on contacts through the provided endpoints:

Create a new contact: POST /api/contacts/
Retrieve all contacts: GET /api/contacts/all
Retrieve a single contact by ID: GET /api/contacts/{contact_id}
Update a contact by ID: PUT /api/contacts/{contact_id}
Delete a contact by ID: DELETE /api/contacts/{contact_id}
License
This project is licensed under the MIT License.
