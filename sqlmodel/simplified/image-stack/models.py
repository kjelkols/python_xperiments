# models.py
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class ImageFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(default="", nullable=False)
    stack_id: Optional[int] = Field(default=None, foreign_key="stack.id")
    stack: Optional["Stack"] = Relationship(back_populates="imagefiles")

class Stack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    imagefiles: List[ImageFile] = Relationship(back_populates="stack")