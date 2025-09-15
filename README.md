# FastCrud — Simple CRUD User Management App

A **FastAPI + PostgreSQL** app for managing users with async operations, nanoid IDs, hashed passwords, and email/password validation.


## Features

* Create users with **unique IDs** using `nanoid`
* Hash passwords securely with **Passlib (bcrypt)**
* Validate passwords using **regex**
* Validate emails automatically
* List all users
* Delete users
* Login with password verification
* Async PostgreSQL queries using `psycopg_pool`
* Logging via **Loguru**

## Installation

1. **Clone the repository**:

```bash
git clone <repo-url>
cd <repo>
```

2. **Create a virtual environment**:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```


## Configuration

1. **Create a `.env` file** in the project root (never commit this):

```env
DB_USERNAME=lenny
DB_PASSWORD=leonard
DB_HOSTNAME=127.0.0.1
DB_PORT=5432
DB_NAME=my_project
```

2. **Create the `users` table** in your PostgreSQL database:

```sql
CREATE TABLE users (
    id VARCHAR(14) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Usage

Run the FastAPI server:

```bash
python main.py
```

* Server runs at `http://127.0.0.1:8000`
* Visit `http://127.0.0.1:8000/docs` for **Swagger UI**.


## API Endpoints

| Method | Path         | Description                    |
| ------ | ------------ | ------------------------------ |
| POST   | /users/add   | Create a new user              |
| POST   | /users/login | Login with username + password |
| GET    | /users/list  | List all users                 |
| DELETE | /users/{email}  | Delete a user by email      |


### Example Request — Create User

```http
POST /users/add
Content-Type: application/json

{
    "username": "john",
    "email": "john@example.com",
    "password": "StrongPass1!"
}
```

Response:

```json
{
    "id": "V1StGXR8_Z5jdHi6B-myT",
    "username": "john",
    "email": "john@example.com"
}
```


### Password Requirements

* Minimum **8 characters**
* At least **1 uppercase**
* At least **1 lowercase**
* At least **1 number**
* At least **1 special character** (`@$!%*?&`)

### Notes

* Uses **nanoid** for unique IDs
* Uses **Loguru** for logging
* Fully **async operations**
* `.env` stores sensitive DB credentials (never commit)
* Compatible with **Uvicorn** by default for running FastAPI

## `requirements.txt`

```txt
fastapi
uvicorn[standard]
psycopg_pool
passlib[bcrypt]
python-dotenv
loguru
nanoid
regex
```

---

> [!NOTE]
> Tested on Fedora Workstation 42