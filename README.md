# SESHIA-
Aplicación web que integra el seguimiento del ciclo menstrual con la gestión y el análisis de finanzas personales.


## Cómo se ejecuta?
```bash
docker compose up --build -d
```

si hiciste cambios
```bash
# paso 1 
docker compose down 

# paso 2
docker compose up
```

# Seshia

## About the Project

Seshia is a web application designed to help women monitor their menstrual cycle and personal finances in a single platform. The application allows users to register menstrual cycles, daily symptoms, expenses, and income, making it possible to identify relationships between hormonal phases and financial behavior through data analysis and insights.

The project follows Django's MVT architecture and is organized into domain-driven applications to improve maintainability, scalability, and collaborative development.

---

## Features

- User authentication and profile management.
- Menstrual cycle registration and tracking.
- Daily symptom logging.
- Income and expense management.
- Financial categorization.
- Dashboard with summarized information.
- Insights generated from cycle and financial data.
- AJAX-based interactions for a smoother user experience.

---

## Technologies

### Backend

- Python *(specify version)*
- Django *(specify version)*
- Django ORM

### Frontend

- HTML5
- CSS3
- Vanilla JavaScript
- AJAX (Fetch API)
- Django Templates

### Database

- PostgreSQL

### DevOps

- Docker
- Docker Compose

---

## Requirements

Before running the project, make sure you have installed:

- Docker
- Docker Compose
- Git

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project folder:

```bash
cd Seshia
```

Build the Docker containers:

```bash
docker-compose build
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your_secret_key

DEBUG=True

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Adjust the values according to your local environment.

---

## Running the Project

Start the application using Docker:

```bash
docker-compose up
```

If this is the first execution, apply the database migrations:

```bash
docker-compose exec web python manage.py migrate
```

If the project includes seed data:

```bash
docker-compose exec web python manage.py seed_categories
```

To create an administrator account:

```bash
docker-compose exec web python manage.py createsuperuser
```

The application will be available at:

```
http://localhost:8000
```

---

## Database

Seshia uses PostgreSQL as its relational database management system.

Database schema changes are managed through Django migrations.

Useful commands:

Create migrations:

```bash
docker-compose exec web python manage.py makemigrations
```

Apply migrations:

```bash
docker-compose exec web python manage.py migrate
```

---

## Project Structure

> *Architecture documentation will be added here.*

---

## Project Organization

The project follows a modular architecture where each business domain is isolated into its own Django application.

Current domains include:

- Users
- Cycles
- Finances
- Insights

Each application is responsible for a single business context, allowing independent development, easier maintenance, and future scalability.

Instead of concentrating every model inside a single `models.py` file, each model is placed in its own file within the `models/` directory. This organization improves readability, simplifies navigation, and reduces merge conflicts during collaborative development.

The project also separates responsibilities into dedicated layers such as:

- Models
- Forms
- Views
- Services
- Templates
- Static resources

This structure keeps the codebase organized and facilitates long-term maintenance.

---

## License

This project is licensed under the MIT License.
