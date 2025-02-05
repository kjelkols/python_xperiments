from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import engine
from models import SQLModel
from routes import router

# Create database tables (if they don't exist)
SQLModel.metadata.create_all(engine)

# Dependency to get a database session
app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)