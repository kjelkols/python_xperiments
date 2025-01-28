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
