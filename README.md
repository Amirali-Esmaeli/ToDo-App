# ToDo-App

This project was developed as part of the **Advanced Django course (https://maktabkhooneh.org/course/%d8%a2%d9%85%d9%88%d8%b2%d8%b4-%d8%ac%d9%86%da%af%d9%88-%d9%be%db%8c%d8%b4%d8%b1%d9%81%d8%aa%d9%87-mk1438/)**.  
It contains three main applications:  
`accounts`, `todo`, and `weather`.

---

## Features

### 1. Accounts

The **Accounts** app handles user authentication, registration, and account management.  
It supports both **web authentication (forms & views)** and **REST API endpoints** (Token & JWT).

- Custom `User` model with:
  - Email as unique identifier (instead of username)
  - Flags: `is_staff`, `is_superuser`, `is_active`, `is_verified`
- `UserManager` for creating users and superusers
- Login & Register views:
  - `CustomLoginView` → users log in with their email
  - `RegisterPage` → register new users and auto-login
  - Both implemented using **Class-Based Views (CBV)**
- Forms:
  - `CustomUserCreationForm` with CAPTCHA for extra security
  - `CustomAuthenticationForm` customized for email login

#### API Endpoints (`/accounts/api/v1/`)
The project provides a full-featured authentication API with **Django REST Framework** and **JWT**.

**Authentication**
- Token-based:
  - `POST /accounts/api/v1/token/login/` → Login and get auth token
  - `POST /accounts/api/v1/token/logout/` → Logout and delete auth token
- JWT-based:
  - `POST /accounts/api/v1/jwt/create/` → Get access & refresh tokens
  - `POST /accounts/api/v1/jwt/refresh/` → Refresh token
  - `POST /accounts/api/v1/jwt/verify/` → Verify token

**Password Management**
- `PUT /accounts/api/v1/change/password/` → Change password (requires old password)
- `POST /accounts/api/v1/password-reset/` → Request password reset (email with link is sent)
- `POST /accounts/api/v1/password-reset-confirm/<uidb64>/<token>/` → Reset password using link


#### Email Handling
- Uses `mail_templated.EmailMessage` to send activation & password reset emails.
- Emails are sent asynchronously with a custom `EmailThread` utility.


#### Tests (`tests/test_account_api.py`)
-  Successful user registration (`201 Created`)
-  Change password with valid data (`200 OK`)
-  Login attempt by a verified user (`200 OK`)

---

### 2. todo

The **Todo** app allows authenticated users to create, update, complete, and delete personal tasks.  
Each task belongs to a specific user and cannot be accessed by others. 

- **Model: `Task`**
  - `user` → ForeignKey to `User`
  - `title` → CharField
  - `complete` → BooleanField
  - `created_date`, `updated_date`
  - Ordered with respect to the `user`

- **Class-based Views**
  - `TaskList` → List all tasks for the logged-in user
  - `TaskCreate` → Create a new task
  - `TaskUpdate` → Update an existing task
  - `TaskComplete` → Toggle task completion status
  - `DeleteView` → Delete a task

- **Celery Background Task**
- `delete_completed_tasks` → Deletes all completed tasks every 10 minutes

**API Endpoints (via DRF ViewSet & Router):**
- `GET /api/v1/task/` → List user’s tasks
- `POST /api/v1/task/` → Create a new task
- `GET /api/v1/task/{id}/` → Retrieve a specific task
- `PATCH /api/v1/task/{id}/` → Update a task
- `DELETE /api/v1/task/{id}/` → Delete a task

#### Tests (`tests/test_todo_api.py`)
The Todo API is fully tested with **pytest** and **DRF APIClient**. 
-  Get task list (authenticated, `200 OK`)
-  Create task (verified user, `201 Created`)
-  Edit own task (verified user, `200 OK`)
-  Delete own task (`204 No Content`)

---
### 3. weather
The **Weather** app provides a simple API to get current weather information for a given city using OpenWeatherMap API.

- Fetch current weather data for any city
- Cached responses for 20 minutes to reduce API calls

**API Endpoint:**
- `GET /api/v1/weather/<city>/` → Get weather information for a specific city
---
### API Documentation (Swagger)
- `GET /swagger/` → View interactive Swagger UI for all endpoints


## Docker Setup (Development & Production)
To get this repository, run the following command inside your git enabled terminal
 ```bash
git clone https://github.com/Amirali-Esmaeli/ToDo-App.git
```
### services
- redis → Caching and Celery broker
- backend → Django app
- worker → Celery worker
- beat → Celery beat scheduler
- db → PostgreSQL database
- nginx → Reverse proxy
- smtp4dev → Local email testing
### Development
```bash
docker-compose up --build
```
- Backend: http://localhost:8000/
- SMTP4DEV: http://localhost:5000/

### Production / Stage
```bash
docker-compose -f docker-compose-stage.yml up --build
```
- Backend runs with Gunicorn and Nginx
- Static & media files persisted in volumes
- Celery worker & beat run with Redis





