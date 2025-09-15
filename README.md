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

> [!WARNING]
> Ensure [uv](https://github.com/astral-sh/uv) and Postgres is installed

1. **Clone the repository**:

```bash
git clone <repo-url>
cd <repo>
```

2. **Create a `.env` file** in the project root:

```env
DB_USERNAME=lenny
DB_PASSWORD=leonard
DB_HOSTNAME=127.0.0.1
DB_PORT=5432
DB_NAME=my_project
```

3. **Create the `users` table** in your PostgreSQL database:

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
4. Run the FastAPI server:

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

Response example:

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

> [!NOTE]
> Tested on Fedora Workstation 42
