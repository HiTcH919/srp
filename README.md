# Service Management System

A web-based application for managing service orders, customer information, and generating reports. Built with Flask.

## Project Structure

```
/
|-- app/                    # Main Flask application directory
|   |-- __init__.py         # Initializes Flask app and registers blueprints
|   |-- static/             # Static files (CSS, JavaScript, images)
|   |   |-- css/
|   |   |   `-- style.css
|   |   `-- js/             # (empty for now)
|   |-- templates/          # HTML templates
|   |   |-- layout.html     # Base template for all pages
|   |   |-- login.html
|   |   |-- dashboard.html
|   |   |-- new_service_basic_info.html
|   |   |-- reports.html
|   |   |-- phonebook.html
|   |   `-- backup.html     # (Template for backup/restore page, to be created)
|   |-- routes/             # Flask blueprints for different modules
|   |   |-- __init__.py
|   |   |-- auth.py         # Authentication routes (login, logout)
|   |   |-- dashboard.py    # Dashboard routes
|   |   |-- service_orders.py # Service order management routes
|   |   |-- reports.py      # Reporting routes
|   |   |-- phonebook.py    # Phonebook/contact management routes
|   |   `-- backup.py       # Backup and restore routes
|   `-- models/             # Database models (e.g., User, ServiceOrder)
|       |-- __init__.py
|       |-- user.py
|       |-- service_order.py
|       `-- contact.py
|-- database/               # Database related scripts
|   `-- schema.sql          # SQL schema definition
|-- run.py                  # Script to run the Flask development server
|-- requirements.txt        # Python dependencies
`-- README.md               # This file
```

## Features (Planned)

*   User Authentication (Login/Logout)
*   Dashboard with overview and quick links
*   Service Order Management:
    *   Create, view, update, and delete service orders
    *   Track status, priority, and assignment
    *   Log parts used and labor time (Future)
*   Customer Management (linked to service orders)
*   Phonebook/Contact Management
*   Reporting (e.g., orders per status, technician performance)
*   Data Backup and Restore functionality

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the database (example for SQLite):**
    *   Ensure you have SQLite installed.
    *   From the project root directory:
        ```bash
        sqlite3 instance/app.db < database/schema.sql
        ```
        (Note: The `instance` folder will be created by Flask if it doesn't exist. You might need to adjust the database path in your Flask configuration in `app/__init__.py` or a separate config file.)

5.  **Run the application:**
    ```bash
    python run.py
    ```
    The application should be accessible at `http://127.0.0.1:5000/` or `http://0.0.0.0:5000/`.

## TODO

*   Implement database initialization and connection in `app/__init__.py`.
*   Flesh out all model classes in `app/models/`.
*   Implement actual logic in all route files in `app/routes/`.
*   Develop all HTML templates further.
*   Add user session management (e.g., Flask-Login).
*   Implement form handling and validation.
*   Create a `config.py` for application settings.
*   Add unit and integration tests.
*   Create the `app/static/js/` directory and add any necessary JavaScript files.
*   Create the `app/templates/backup.html` template.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details (though a LICENSE file hasn't been added yet).
