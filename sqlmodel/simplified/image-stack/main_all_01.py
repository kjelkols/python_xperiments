from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from database import engine
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi import HTTPException
from fastapi import Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from database import get_session  # Import the session dependency
#from sqlalchemy.orm import relationship as sa_relationship  # Import SQLAlchemy's relationship

class Node(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(default="", nullable=False)


class ImageFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(default="", nullable=False)
    stack_id: Optional[int] = Field(default=None, foreign_key="stack.id")
    stack: Optional["Stack"] = Relationship(back_populates="imagefiles")

class Stack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
#    imagefiles: List[ImageFile] = sa_relationship("ImageFile", back_populates="stack", lazy="joined")  # Eager loading
    imagefiles: List[ImageFile] = Relationship(back_populates="stack")
    
# Dependency to get a database session
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/ZZZstacks")
def get_ZZZstacks(session: Session = Depends(get_session)):
    stacks = session.exec(select(Stack)).all()
    return [{"id": stack.id, "imagefiles": [{"id": img.id, "path": img.path_str} for img in stack.imagefiles]} for stack in stacks]

@app.get("/stacks")
async def get_stacks(session: Session = Depends(get_session)):
    # Fetch all stacks
    stacks = session.exec(select(Stack)).all()
    
    # Prepare response with the first image in each stack
    stack_data = []
    for stack in stacks:
        first_image = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id).limit(1)).first()
        stack_data.append({
            "id": stack.id,
            "first_image": first_image.path_str if first_image else None
        })

    return stack_data

@app.get("/ZZZstack/{stack_id}")
async def get_ZZZstack(stack_id: int, session: Session = Depends(get_session)):
    # Fetch the stack by ID
    stack = session.get(Stack, stack_id)
    if not stack:
        raise HTTPException(status_code=404, detail="Stack not found")
    
    # Fetch associated image files
    stack.imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
    
    session.refresh(stack)  # Refresh the stack to get the updated imagefiles

    return stack  # FastAPI will return it as JSON

@app.get("/stack/{stack_id}")
async def get_stack(stack_id: int, session: Session = Depends(get_session)):
    # Fetch the stack by ID
    stack = session.get(Stack, stack_id)
    if not stack:
        raise HTTPException(status_code=404, detail="Stack not found")
    
    # Manually fetch image files for the stack
    imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
    
    # Convert to dictionary and add image files
    return {
        "id": stack.id,
        "imagefiles": [{"id": img.id, "path_str": img.path_str} for img in imagefiles]
    }
    
@app.get("/ZZZ1stack/{stack_id}")
async def ZZZ1get_stack(stack_id: int, session: Session = Depends(get_session)):
    stack = session.get(Stack, stack_id)
    if not stack:
        raise HTTPException(status_code=404, detail="Stack not found")
    return stack  # Now it includes `imagefiles` automatically!

@app.get("/scantest/{zzz}")
async def scan_directory(zzz: str, session: Session = Depends(get_session)):
    print ("HEIZZZ=",zzz)
    path_str = "C:/temp/PHOTOS_SRC_TEST/year_2024/2024_04_27_taipei_beitou"

    base_path = Path(path_str)

    # Check if the directory exists
    if not base_path.is_dir():
        raise HTTPException(status_code=400, detail="Directory does not exist")

    # Find all JPG files
    jpg_files = list(base_path.rglob("*.jpg"))

    if not jpg_files:
        return {"message": "No images found"}

    # Create stacks and image files
    for jpg_file in jpg_files:
        stack = Stack()  # New stack for each image
        imagefile = ImageFile(path_str=str(jpg_file), stack=stack)

        session.add(stack)
        session.add(imagefile)

    session.commit()
    return {"message": f"Added {len(jpg_files)} images"}

# Create database tables (if they don't exist)
SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)