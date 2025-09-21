# Invoice & Billing Management API

A backend-focused **Django REST Framework (DRF)** project that manages
clients, products, invoices, and payments with role-based access
control.

## Features

-   **Authentication & Authorization**
    -   JWT Authentication (Login, Refresh, Logout, Register)
    -   Role-Based Access Control (Manager, Employee)
    -   Custom permissions (e.g., Managers full access, Employees
        read-only)
-   **Core Modules**
    -   **Clients**: Manage customer records
    -   **Products**: Manage available products
    -   **Invoices**: Create invoices with items, total, and remaining
        balance
    -   **Payments**: Record full or partial payments, update invoice
        status
    -   **Activity Logs**: Track user actions (e.g., recording payments)
-   **Other Integrations**
    -   Filtering support (basic)
    -   API documentation with DRF-Spectacular
    -   GitHub-ready project with `.gitignore`

## Tech Stack

-   Python
-   Django
-   Django REST Framework (DRF)
-   PostgreSQL (configurable)
-   JWT Auth (djangorestframework-simplejwt)
-   API Docs (drf-spectacular) - UI for testing APIs

## API Documentation

This project uses **drf-spectacular** for automatic API documentation.

- **Swagger UI (Interactive Docs):** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)  
- **Redoc UI (Static Docs):** [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)  
- **OpenAPI Schema (JSON/YAML):** [http://127.0.0.1:8000/api/schema/](http://127.0.0.1:8000/api/schema/)  

## Usage

-   Access API docs at: `http://127.0.0.1:8000/api/docs/`
-   Register or log in to obtain JWT tokens.
-   Use the tokens for authenticated API requests.

## Example API Endpoints

-   `POST /api/v1/auth/register/` → Register new user
-   `POST /api/v1/auth/login/` → Obtain JWT token
-   `POST /api/v1/auth/logout/` → Logout
-   `POST /api/v1/auth/refresh/` → Refresh Token
-   `All /api/v1/billing/clients/` → CRUD Clients
-   `ALL /api/v1/billing/products/` → CRUD Products
-   `ALL /api/v1/billing/invoices/` → CRUD Invoice
-   `ALL /api/v1/billing/payments/` → CRUD Payments
-   `GET /api/v1/billing/activity-logs/` → View all Activities

## Installation

1.  Clone the repository:

    ``` bash
    git clone https://github.com/yourusername/yourrepo.git
    cd yourrepo
    ```

2.  Create and activate a virtual environment:

    ``` bash
    python -m venv venv
    venv\Scripts\activate    # Windows
    ```

3.  Install dependencies:

    ``` bash
    pip install -r requirements.txt
    ```

4.  Set up environment variables in `.env` (example):

    ``` env
    SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_URL=postgres://user:password@localhost:5432/dbname
    ```

5.  Run migrations:

    ``` bash
    python manage.py migrate
    ```

6.  Create a superuser:

    ``` bash
    python manage.py createsuperuser
    ```

7.  Start the development server:

    ``` bash
    python manage.py runserver
    ```

## Notes

-   Filtering is enabled, but pagination is not implemented (designed
    for limited dataset showcase).
-   Focus is backend logic for portfolio purposes (no frontend).

------------------------------------------------------------------------

### Author

Developed as a portfolio project to demonstrate **Django REST Framework
backend skills**.
