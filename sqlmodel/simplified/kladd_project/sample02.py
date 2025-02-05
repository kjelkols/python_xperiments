from fastapi import Depends, FastAPI
from fastapi import HTTPException
from sqlmodel import Session, create_engine
from core import create_image_file_core, move_image_file_core, remove_image_file_core, show_stack_core, show_all_stacks_core

from database import helper_delete_database, create_tables, get_session
from database import engine, SQLModel  # Import database setup

from routes import router

create_tables()

# Dependency to get a database session
app = FastAPI()

# Include the router
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    #uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="localhost", port=8000)