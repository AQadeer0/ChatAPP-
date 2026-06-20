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

⚙️ Installation & Setup

1. Clone & Navigate

Ensure your project files are structured as shown in the directory tree above.

3. Environment Configuration (`.env`)

Create or edit your `.env` file in the root directory to match your PostgreSQL server settings:
```ini
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ChatApp
DB_USER=Chat
DB_PASSWORD=qadeer1234
```

3. Install Dependencies

Set up your virtual environment and install the required dependencies listed in `requirements.txt`:
```bash
pip install -r requirements.txt
```

4.Database Initialization

Execute the `schema.sql` script inside your PostgreSQL instance to generate the necessary tables:
```bash
psycopg2 -h localhost -U Chat -d ChatApp -f schema.sql
```
5. Run the Application

Start the Uvicorn development server:
```bash
uvicorn main:app --reload
```
Once started, open your web browser and navigate to `http://127.0.0.1:8000` to interact with the chat interface.

                                            OUTPUT 
![Chat App Screen](https://github.com/AQadeer0/ChatAPP-/blob/82102305eeb281b5f2f6875f0e7caf92388a7aa4/APP%20INTER%20FACE.png)
