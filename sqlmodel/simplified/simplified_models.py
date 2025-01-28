from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel
from sqlmodel import Field, SQLModel
from typing import Optional

class ImageFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(default="") # File name with eventual path
    stack_id: Optional[int] = Field(default=None, foreign_key="stack.id") #2
    stack: Optional["Stack"] = Relationship (back_populates="imagefiles") #2

class Stack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    imagefiles: List["ImageFile"] = Relationship (back_populates="stack") #2

