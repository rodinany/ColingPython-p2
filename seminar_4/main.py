from fastapi import FastAPI
from app.routers import students

app = FastAPI(
    title="Student API"
)

@app.get("/")
def root() -> dict:
    """Root GET"""
    return {"message": "Hello world!"}

app.include_router(students.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=True
    )
