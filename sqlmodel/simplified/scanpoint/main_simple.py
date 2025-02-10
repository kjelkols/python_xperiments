from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List
from pathlib import Path

DATABASE_URL = "sqlite:///ZZZ_main_simple.db"
engine = create_engine(DATABASE_URL, echo=True)

app = FastAPI()

#class StorageDeviceBase(BaseModel):
#    uniquename: str
#    mountpoint: str
#    description: str

class StorageDevice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uniquename: str = Field(unique=True, nullable=False)
    mountpoint: str = Field(nullable=False)
    description: str = Field(nullable=False)

class ScanPoint(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(nullable=False)
    description: str = Field(nullable=False)
    storagedevice_id: Optional[int] = Field(default=None, foreign_key="storagedevice.id")

class ImageFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    path_str: str = Field(nullable=False, unique=True)
    scanpoint_id: Optional[int] = Field(default=None, foreign_key="scanpoint.id")

def get_session():
    with Session(engine) as session:
        yield session

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

@app.get("/storagedevices/new", response_class=HTMLResponse)
def new_storage_device_form(request: Request):
    return templates.TemplateResponse("new_storage_device.html", {"request": request})

@app.get("/storagedevices/list", response_class=HTMLResponse)
def list_storage_devices(request: Request, session: Session = Depends(get_session)):
    devices = session.exec(select(StorageDevice)).all()
    return templates.TemplateResponse("list_storage_devices.html", {"request": request, "devices": devices})

@app.post("/ZZZstoragedevices/")
def ZZZadd_storage_device(storagedevice: StorageDevice, session: Session = Depends(get_session)):
    session.add(storagedevice)
    session.commit()
    session.refresh(storagedevice)
    return storagedevice

from fastapi import Form
@app.post("/storagedevices/")
def add_storage_device(
    uniquename: str = Form(...),
    mountpoint: str = Form(...),
    description: str = Form(...),
    session: Session = Depends(get_session)
):
    device = StorageDevice(uniquename=uniquename, mountpoint=mountpoint, description=description)
    session.add(device)
    session.commit()
    session.refresh(device)
    return device

@app.post("/scanpoints/")
def add_scanpoint(scanpoint: ScanPoint, session: Session = Depends(get_session)):
    session.add(scanpoint)
    session.commit()
    session.refresh(scanpoint)
    return scanpoint

@app.post("/scanpoints/{scanpoint_id}/scan/")
def scan_scanpoint(scanpoint_id: int, session: Session = Depends(get_session)):
    scanpoint = session.get(ScanPoint, scanpoint_id)
    if not scanpoint:
        raise HTTPException(status_code=404, detail="ScanPoint not found")

    scan_dir = Path(scanpoint.path_str)
    if not scan_dir.exists() or not scan_dir.is_dir():
        raise HTTPException(status_code=400, detail="ScanPoint directory not found")

    existing_files = {img.path_str for img in session.exec(select(ImageFile).where(ImageFile.scanpoint_id == scanpoint_id))}
    new_files = []

    for file in scan_dir.rglob("*.jpg"):
        if file.as_posix() not in existing_files:
            image_file = ImageFile(path_str=file.as_posix(), scanpoint_id=scanpoint_id)
            session.add(image_file)
            new_files.append(image_file)

    session.commit()
    return {"message": f"Scanned {len(new_files)} new files", "new_files": new_files}

@app.get("/scanpoints/{scanpoint_id}/thumbnails/")
def get_thumbnails(scanpoint_id: int, session: Session = Depends(get_session)):
    images = session.exec(select(ImageFile).where(ImageFile.scanpoint_id == scanpoint_id)).all()
    return [{"id": img.id, "thumbnail_url": f"/thumbnails/{img.id}.jpg"} for img in images]

@app.get("/images/{image_id}/full/")
def get_full_image(image_id: int, session: Session = Depends(get_session)):
    image = session.get(ImageFile, image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return {"full_image_url": image.path_str}

SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)