💬 Chat App

A modern, real-time web-based chat application built with a high-performance **FastAPI** backend and a seamless asynchronous "PostgreSQL" database layer.

🚀 Features


- Asynchronous Architecture:Built on top of FastAPI and "uvicorn" for blazing-fast request handling.
- Robust Database Layer: Powered by PostgreSQL using "psycopg2-binary" for structured and reliable data persistence.
- Clean Configuration: Environment-variable-driven setup via "python-dotenv" keeping secrets secure.
- Static Frontend Integration: Serving pre-configured web layouts straight from the "public" directory.

🛠️ Tech Stack

 - Backend Framework: FastAPI (v0.111.0)
 - ASGI Server: Uvicorn (v0.30.1)
 - Database Engine: PostgreSQL
 - Database Driver:Psycopg2-binary (v2.9.9)
 - Environment Management:Python-dotenv (v1.0.1)

 📂 Project Structure

```text
Chat App/
├── .env                  # Database and system configuration variables
├── main.py               # Application entry point & API route definitions
├── requirements.txt      # Python dependencies installation manifest
├── schema.sql            # Database tables structure initialization script
└── public/
    └── index.html        # Main web interface for the chat frontend
```
