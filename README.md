# FastAPI Modular RBAC Example

This project is a modular FastAPI application demonstrating Role-Based Access Control (RBAC) using SQLModel and SQLite. It features user authentication, task management, and role-based permissions for admin, manager, and employee roles.

## Features

- User authentication with JWT tokens
- Role-based access control (admin, manager, employee)
- CRUD operations for users and tasks
- Modular structure with routers, models, and schemas
- Middleware for request timing and custom headers

## Project Structure

```
.
├── auth.py
├── database.py
├── dependencies.py
├── main.py
├── middleware.py
├── requirements.txt
├── models/
│   ├── task.py
│   └── user.py
├── routers/
│   ├── auth.py
│   ├── tasks.py
│   └── users.py
├── schemas/
│   ├── task.py
│   ├── token.py
│   └── user.py
└── db.sqlite
```

## Getting Started

### Prerequisites

- Python 3.10+
- [pip](https://pip.pypa.io/en/stable/)

### Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd <project-folder>
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```sh
   uvicorn main:app --reload
   ```

4. **API Docs:**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI.

## Usage

- **Default Admin User:**  
  On first run, a default admin user is created:
  - Username: `admin`
  - Password: `Test_123`

- **Authentication:**  
  Obtain a JWT token via `/auth/token` using username and password.

- **User Management:**  
  - Only admins can create/list users via `/users`.

- **Task Management:**  
  - Admins and managers can create tasks.
  - Employees can update only the status of their assigned tasks.

## Environment Variables

You can set environment variables in the `.env` file (currently empty).

## License

MIT License

## Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [python-jose](https://python-jose.readthedocs.io/)