from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi import HTTPException
from fastapi import Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

# database.py
from sqlmodel import create_engine, Session
DATABASE_URL = "sqlite:///zzz_main_all.db"
engine = create_engine(DATABASE_URL, echo=True)
def get_session():
    with Session(engine) as session:
        yield session

# ===== models.py =====
# Images are typically stored on external drives, which are connected to the computer for scanning.
# The drive can be any storage device, e.g. a USB drive, a network drive, or a cloud service.
# The drive can be disconnected and reconnected, so the path_str of the ScanPoint can change.
# That must be handled by the application, so the user can still access the images after reconnecting the drive.
# By now, the user must manually update the path_str of the ScanPoint, but in the future, the application can do that automatically.
class StorageDevice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uniquename: str = Field(default="", nullable=False) # A unique identifier for the drive noted on the drive itself
    mountpoint: str = Field(default="", nullable=False) # The path where the drive is mounted in the file system first time
    description: str = Field(default="", nullable=False) # Extra information about the drive, e.g. where it is stored
    scanpoints: List["ScanPoint"] = Relationship(back_populates="storagedevice")
# A subdirectory under which ImageFiles are fetched and stored in the database.
# After scanning, the ScanPoint can be detatched from the computer, e.g when located on a USB drive
# Scanning is normally done once, but the ScanPoint can be reconnected to the computer and scanned again.
# A disk name is used to identify the ScanPoint, as the path_str can change if the ScanPoint is connected to another computer.
class ScanPoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(default="", nullable=False)
    description: str = Field(default="", nullable=False)
    storagedevice_id: Optional[int] = Field(default=None, foreign_key="storagedevice.id")
    storagedevice: Optional["StorageDevice"] = Relationship(back_populates="scanpoints")
    
    imagefiles: List["ImageFile"] = Relationship(back_populates="scanpoint")
# A file in the file system, which is part of a stack of images.
# The file is first scanned, then stored in the database
# Downscale versions of the file can be created and stored on the file system of the server.
# The fullscale version is too big to be stored on the server, but can be fetched from the ScanPoint.
# The fullscale version can also be backed up to a cloud service if needed.
class ImageFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(default="", nullable=False)
    stack_id: Optional[int] = Field(default=None, foreign_key="stack.id")
    stack: Optional["Stack"] = Relationship(back_populates="imagefiles")
    scanpoint_id: Optional[int] = Field(default=None, foreign_key="scanpoint.id")
    scanpoint: Optional["ScanPoint"] = Relationship(back_populates="imagefiles")
# A stack of images, where one of them is displayed in a photo browser.
# Grouping raw and JPEG files together is important, as the raw file is the original image, and the JPEG file is the edited version.
# An algorithm must be used to handle such pairs of files, and the JPEG file must be displayed in the photo browser.
class Stack(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    imagefiles: List[ImageFile] = Relationship(back_populates="stack")
    
# Dependency to get a database session. Used by FastAPI's dependency injection system for React
app = FastAPI()
# Define allowed origins "Cross-Origin Resource Sharing (CORS)"
# Since you're building a React frontend for your FastAPI application, your frontend 
# (localhost:5173 for Vite, or localhost:3000 for Create React App) will make API requests to FastAPI (localhost:8000). 
# Without CORSMiddleware, the browser will block these requests due to CORS policy.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
      "localhost:5173",  # React app Vite running locally
      "https://yourfrontend.com",  # Your deployed frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

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