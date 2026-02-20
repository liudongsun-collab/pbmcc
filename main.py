from fastapi import FastAPI

app = FastAPI()

fake_users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"},
]


@app.get("/")
def root():
    return {"message": "Hello from pbmcc"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/users")
def get_users():
    return {"users": fake_users}
