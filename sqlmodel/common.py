from sqlmodel import SQLModel, create_engine
from sqlmodel import Session

# Set up the database
#sqlite_file_name = "zzz_main_all.db"
sqlite_file_name = ":memory:"
sqlite_url = f"sqlite:///{sqlite_file_name}"
my_engine = create_engine(sqlite_url, echo=False) #True)
print ("COMMON my_engine CREATED", my_engine)

def get_session():
    return Session(my_engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(my_engine)

