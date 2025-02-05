from sqlmodel import Field, Relationship, SQLModel, create_engine, Session, select
from typing import List, Optional

class ImageFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(default="", nullable=False)  # File name with path
    stack_id: Optional[int] = Field(default=None, foreign_key="stack.id")  # Foreign key to Stack
    stack: Optional["Stack"] = Relationship(back_populates="imagefiles")  # Relationship to Stack

class Stack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    imagefiles: List[ImageFile] = Relationship(back_populates="stack")  # Relationship to ImageFiles
