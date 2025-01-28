from sqlmodel import Field, Relationship, SQLModel, create_engine
from typing import List, Optional

DATABASE_URL = "sqlite:///image_stack.db"
engine = create_engine(DATABASE_URL)

class ImageFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(default="", nullable=False)
    stack_id: Optional[int] = Field(default=None, foreign_key="stack.id")
    stack: Optional["Stack"] = Relationship(back_populates="imagefiles")

class Stack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    imagefiles: List[ImageFile] = Relationship(back_populates="stack")
from sqlmodel import Session, select

# Create the database tables
SQLModel.metadata.create_all(engine)

# Create a new stack
stack = Stack()

# Create some image files
image1 = ImageFile(path_str="/path/to/image1.png", stack=stack)
image2 = ImageFile(path_str="/path/to/image2.png", stack=stack)

# Add to the database
with Session(engine) as session:
    session.add(stack)
    session.add(image1)
    session.add(image2)
    session.commit()

# Query the database
with Session(engine) as session:
    statement = select(Stack).where(Stack.id == 1)
    stack = session.exec(statement).first()
    print(f"Stack ID: {stack.id}")
    for image in stack.imagefiles:
        print(f"Image ID: {image.id}, Path: {image.path_str}")