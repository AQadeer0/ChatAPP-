import os
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


load_dotenv()

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "chatapp_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "")
    )

@app.on_event("startup")
def startup_db():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        with open("schema.sql", "r") as f:
            cur.execute(f.read())
        conn.commit()
        print("--- Database Tables Initialized Successfully ---", flush=True)
    except Exception as e:
        print(f"--- Database Initialization Failed: {e} ---", flush=True)
        print("Make sure PostgreSQL is running and you have created the database specified in .env", flush=True)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

def get_chat_history():
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT sender, content, TO_CHAR(timestamp, 'HH24:MI') as time FROM messages ORDER BY id DESC LIMIT 50"
        )
        rows = cur.fetchall()
        return list(reversed(rows))
    except Exception as e:
        print(f"Error fetching history: {e}", flush=True)
        return []
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def save_chat_message(sender: str, content: str):
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO messages (sender, content) VALUES (%s, %s) RETURNING TO_CHAR(timestamp, 'HH24:MI')",
            (sender, content)
        )
        time_str = cur.fetchone()[0]
        conn.commit()
        return time_str
    except Exception as e:
        print(f"Error saving message: {e}", flush=True)
        return ""
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        print(f"Broadcasting message to {len(self.active_connections)} connection(s): {message}", flush=True)
        for connection in list(self.active_connections):
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                print(f"Error broadcasting to connection, disconnecting: {e}", flush=True)
                self.disconnect(connection)

manager = ConnectionManager()

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    print(f"WebSocket connecting for user: {username}", flush=True)
    await manager.connect(websocket)
    print(f"WebSocket connected for user: {username}. Total active connections: {len(manager.active_connections)}", flush=True)
    try:
        history = get_chat_history()
        print(f"Sending chat history of size {len(history)} to {username}", flush=True)
        await websocket.send_text(json.dumps({
            "type": "history",
            "messages": history
        }))

        await manager.broadcast({
            "type": "system",
            "content": f"{username} joined the chat",
            "time": ""
        })

        while True:
            data = await websocket.receive_text()
            print(f"Received text data from {username}: {data}", flush=True)
            message_data = json.loads(data)
            content = message_data.get("content", "")

            if content:
                time_str = save_chat_message(username, content)
                if not time_str:
                    time_str = "Now"

                await manager.broadcast({
                    "type": "chat",
                    "sender": username,
                    "content": content,
                    "time": time_str
                })

    except WebSocketDisconnect:
        print(f"WebSocket disconnected for user: {username}", flush=True)
        manager.disconnect(websocket)
        await manager.broadcast({
            "type": "system",
            "content": f"{username} left the chat",
            "time": ""
        })
    except Exception as e:
        print(f"WebSocket error for {username}: {e}", flush=True)
        manager.disconnect(websocket)


os.makedirs("public", exist_ok=True)
app.mount("/", StaticFiles(directory="public", html=True), name="public")