# Database setup
from sqlmodel import SQLModel, create_engine, Session
from pathlib import Path

DATABASE_FILE = "ZZZ_image_stack.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE}"
engine = create_engine(DATABASE_URL)

# For use with FastAPI
def get_session():
    with Session(engine) as session:
        yield session

def helper_delete_database():
    file_path = Path(DATABASE_FILE)
# Check if the file exists before attempting to delete it
    if file_path.exists():
        # Delete the file
        file_path.unlink()
        print(f"    #### {file_path} has been deleted successfully.")
    else:
        print(f"    #### {file_path} does not exist.")

def create_tables():
    SQLModel.metadata.create_all(engine)
