from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello from pbmcc"}


@app.get("/health")
def health():
    return {"status": "ok"}
