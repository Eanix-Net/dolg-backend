# LawnMate Backend

The backend API for the LawnMate application - an open source lawn care management system for landscaping professionals from solo operators to small/medium teams.


![App Login Screen](https://lawnbuddy.net/static/images/app-screenshot.png)
![Website Landing Page](https://lawnbuddy.net/static/images/website-screenshot.png)

## Features

* Customer Management
* Location Management 
* Appointment Scheduling
* Invoice Generation
* Quote Creation
* Equipment Tracking
* Reviews System
* Time Tracking
* Customer Portal
* Photo Management

## Tech Stack

* Python 3.12
* Flask 2.2.3
* PostgreSQL
* Docker
* SQLAlchemy ORM
* JWT Authentication

## Prerequisites

* Docker and Docker Compose
* PostgreSQL (or use the Docker container)
* Python 3.12+ (for local development)

## Environment Setup

Create a `.env` file in the backend directory with the following variables:

```
FLASK_APP=app.py
FLASK_ENV=development
JWT_SECRET_KEY=your_secret_key_here
POSTGRES_USER=lawnmate
POSTGRES_PASSWORD=your_password_here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=lawnmate
```

## Installation

### Using Docker

1. Clone the repository
2. Navigate to the backend directory
3. Modify the `docker-compose.yml` file to set your preferred database volume location:

```yaml
services:
  backend:
    # ... existing config ...
    volumes:
      - .:/app
      # For database persistence, add a volume that points to a directory outside the container:
      - ../data:/var/lib/postgresql/data  # Store data one level up from current directory
```

4. Build and start the Docker containers:

```bash
sudo docker compose up -d
```

5. Initialize the database with the default admin user:

```bash
sudo docker compose exec backend python init_db.py
```

### Manual Setup

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Set up the database (PostgreSQL):

```bash
flask db upgrade
```

6. Initialize the database with the default admin user:

```bash
python init_db.py
```

7. Start the application:

```bash
flask run
```

## Default Admin User

After initializing the database, you can log in with the following credentials:

- Email: admin@example.com
- Password: admin

**IMPORTANT:** Change the default admin password immediately after first login.

## API Documentation

The API is structured around the following resources:

- `/api/auth` - Authentication endpoints
- `/api/employees` - Employee management
- `/api/customers` - Customer information
- `/api/locations` - Customer locations
- `/api/appointments` - Scheduling
- `/api/invoices` - Billing
- `/api/quotes` - Service quotes
- `/api/equipment` - Equipment tracking
- `/api/reviews` - Customer reviews
- `/api/photos` - Job photos
- `/api/timelogs` - Employee time tracking
- `/api/customer-portal` - Customer-facing endpoints
- `/api/integrations` - External service integrations

## Development

To run the development server with hot reloading:

```bash
flask run --debug
```

## License

This project is licensed under the terms specified in the LICENSE file.
