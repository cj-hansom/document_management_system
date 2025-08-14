# FastAPI Document Connector

A simplified Document Connector service built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**. This application allows users to manage documents, process them for AI context (text chunking and embeddings), and access them securely.

---

##  Key Features

- **Document CRUD REST API**
- **JWT-based Authentication & Authorization**
- **PostgreSQL Database** with proper migrations via Alembic
- **In-Memory Vector Embeddings** for AI document context (simulated)
- **Text Chunking for AI Processing**
- **Structured Logging & Error Handling**
- **Unit Tests** using `pytest`
- **Interactive API Documentation** via OpenAPI/Swagger

---

##  Tech Stack

| Component      | Stack                  |
|----------------|------------------------|
| Framework      | FastAPI (Python 3.13)  |
| Database       | PostgreSQL             |
| ORM            | SQLAlchemy             |
| Migrations     | Alembic                |
| Auth           | JWT (HS256)            |
| Testing        | pytest                 |
| Embeddings     | In-memory mock         |

---

##  Setup & Installation

1. **Clone the repository**
    ```bash
    git clone https://github.com/cj-hansom/document_management_system.git
    cd document_management_system
    ```

2. **Create and activate virtual environment**
    ```bash
    python -m venv venv
    # Linux/macOS:
    source venv/bin/activate
    # Windows:
    venv\Scripts\activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure environment variables**  
   Create a `.env` file:
    ```
    DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/fastapidb
    SECRET_KEY=your_jwt_secret
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

---

##  Database Migrations with Alembic

1. Ensure your models are defined in `app/models.py` and `Base = declarative_base()` in `app/database.py`.
2. In your Alembic `env.py`, `target_metadata = Base.metadata` must be set (you’ve done this).
3. Create and apply migrations:
    ```bash
    alembic revision --autogenerate -m "Initial schema"
    alembic upgrade head
    ```

---

##  Running the Application

```bash
uvicorn app.main:app --reload


##   Running Authumated Test

pytest -v
