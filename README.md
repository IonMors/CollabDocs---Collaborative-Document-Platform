# CollabDocs - Collaborative Document Platform

CollabDocs is a Django REST Framework backend application that allows users to create collaborative workspaces, manage version-controlled documents, collaborate through comments, organize documents using tags, and track activities using audit logs.

This project was developed as part of a Backend Engineering assessment and demonstrates Django REST Framework, PostgreSQL, JWT Authentication, transactions, middleware, signals, and query optimization.

---

# Features

- User Registration & JWT Authentication
- Workspace Management
- Workspace Member Management
- Document Versioning
- Threaded Comments
- Tag Management
- Audit Logging
- Request Logging Middleware
- PostgreSQL Database
- UUID Primary Keys
- Swagger API Documentation

---

# Tech Stack

- Python 3.x
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- drf-spectacular
- python-dotenv

---

# Project Structure

```
CollabDocs/
│
├── audit/
├── comments/
├── config/
├── documents/
├── tags/
├── users/
├── workspace/
│
├── .env.example
├── manage.py
├── requirements.txt
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
```

```bash
cd CollabDocs
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure PostgreSQL

Create a PostgreSQL database.

Example:

```
Database Name : collabdocs
```

---

## Configure Environment Variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your-secret-key

DEBUG=True

DB_NAME=collabdocs

DB_USER=postgres

DB_PASSWORD=postgres

DB_HOST=localhost

DB_PORT=5432
```

---

## Apply Migrations

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

---

## Create Superuser

```bash
python manage.py createsuperuser
```

---

## Run Development Server

```bash
python manage.py runserver
```

Application URL

```
http://127.0.0.1:8000/
```

---

# Authentication

JWT Authentication is used.

## Register User

```
POST /api/users/register/
```

## Login

```
POST /api/users/login/
```

Returns

- Access Token
- Refresh Token

Use the Access Token for all protected APIs.

Example:

```
Authorization: Bearer <access_token>
```

---

# API Endpoints

## Users

| Method | Endpoint |
|----------|-----------------------------|
| POST | /api/users/register/ |
| POST | /api/users/login/ |
| GET | /api/users/me/ |
| GET | /api/users/ |

---

## Workspaces

| Method | Endpoint |
|----------|--------------------------------|
| GET | /api/workspaces/ |
| POST | /api/workspaces/ |
| GET | /api/workspaces/{id}/ |
| PUT | /api/workspaces/{id}/ |
| DELETE | /api/workspaces/{id}/ |
| GET | /api/workspaces/{id}/members/ |
| POST | /api/workspaces/{id}/invite/ |
| GET | /api/workspaces/{id}/stats/ |

---

## Documents

| Method | Endpoint |
|----------|--------------------------------|
| GET | /api/documents/ |
| POST | /api/documents/ |
| GET | /api/documents/{id}/ |
| PUT | /api/documents/{id}/ |
| DELETE | /api/documents/{id}/ |
| GET | /api/documents/{id}/versions/ |
| GET | /api/documents/summary/ |

---

## Comments

| Method | Endpoint |
|----------|--------------------------------|
| GET | /api/comments/ |
| POST | /api/comments/ |
| GET | /api/comments/{id}/ |
| PUT | /api/comments/{id}/ |
| DELETE | /api/comments/{id}/ |
| POST | /api/comments/{id}/reply/ |

---

## Tags

| Method | Endpoint |
|----------|--------------------------------|
| GET | /api/tags/ |
| POST | /api/tags/ |
| GET | /api/tags/{id}/ |
| PUT | /api/tags/{id}/ |
| DELETE | /api/tags/{id}/ |
| GET | /api/tags/{id}/documents/ |

---

## Audit Logs

| Method | Endpoint |
|----------|--------------------------------|
| GET | /api/audit-logs/ |
| GET | /api/audit-logs/{id}/ |

---

# Database Models

The project consists of the following models:

- User (Django Built-in)
- Workspace
- WorkspaceMember
- Document
- DocumentVersion
- Comment
- Tag
- AuditLog

---

# Assignment Requirements Implemented

- UUID Primary Keys
- PostgreSQL Database
- Django REST Framework
- ModelViewSet
- SerializerMethodField
- Custom Serializer Validation
- Transaction Management (`transaction.atomic()`)
- Django Signals
- Request Logging Middleware
- JWT Authentication
- TextChoices
- UniqueConstraint
- Many-to-Many Relationship
- Self-Referencing ForeignKey
- Query Optimization using `select_related()`
- Filtering using `Q` Objects
- Aggregation using `Count`
- Custom Endpoints using `@action`

---

# Middleware

A custom middleware logs every request with:

- HTTP Method
- Endpoint Path
- Response Status Code
- Request Processing Time

Example:

```
============================================================
Method        : POST
Endpoint      : /api/documents/
Status Code   : 201
Time Taken    : 24.37 ms
============================================================
```

---

# Signals

A Django `post_save` signal automatically creates an AuditLog whenever a Document is created or updated.

The following information is stored:

- Actor
- Action
- Model Name
- Object ID

---

# Document Versioning

Whenever a document is created or updated:

- A new `DocumentVersion` is automatically created.
- Version numbers are maintained per document.
- Version creation occurs inside a `transaction.atomic()` block.

---

# Swagger API Documentation

Swagger UI

```
http://127.0.0.1:8000/api/docs/
```

OpenAPI Schema

```
http://127.0.0.1:8000/api/schema/
```

---

# Testing

All APIs were tested using Postman.

The project includes:

- User Registration
- User Login
- Workspace CRUD
- Document CRUD
- Comment CRUD
- Tag CRUD
- Audit Log APIs
- Workspace Statistics
- Document Summary
- Document Version History

---

# Future Improvements

- Role-Based Authorization
- Pagination
- Search & Advanced Filtering
- Email Invitations
- Docker Support
- CI/CD Pipeline
- Unit & Integration Tests

---

# Author

**Ayan Dey, Subhadeep Mondal, Aashish Poojari, Pranish N**

Backend Engineering Assessment Project

Built using Django REST Framework and PostgreSQL.
