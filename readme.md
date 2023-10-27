# Contact API

A simple API for managing contacts, built using FastAPI.

## Features:

- CRUD operations for contacts.
- Storage of contact's birthdate.
- Automatic API documentation generation.
- Utilizes PostgreSQL as the database.
- Data validation using Pydantic.

## Getting Started

### Prerequisites:

- Python 3.8 or newer.
- PostgreSQL.

### Installation:

1. Clone the repository:
   ```
   git clone [your-repository-link]
   ```

2. Navigate to the project directory:
   ```
   cd [your-project-name]
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Update the `config.ini` with your PostgreSQL database details.

5. Run the FastAPI server:
   ```
   uvicorn main:app --reload
   ```

Visit `http://127.0.0.1:8000/docs` in your browser to access the automatically generated API documentation.

## Usage

You can perform CRUD operations on contacts through the provided endpoints:

- Create a new contact: `POST /api/contacts/`
- Retrieve all contacts: `GET /api/contacts/all`
- Retrieve a single contact by ID: `GET /api/contacts/{contact_id}`
- Update a contact by ID: `PUT /api/contacts/{contact_id}`
- Delete a contact by ID: `DELETE /api/contacts/{contact_id}`

## License

This project is licensed under the MIT License.
