from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional, List
from pydantic import BaseModel

DATABASE_URL = "sqlite:///ZZZ_main_micro.db"
engine = create_engine(DATABASE_URL, echo=True)
def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

class StorageDeviceBase(BaseModel):
    uniquename: str
    mountpoint: str
    description: str
    
class StorageDevice(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    uniquename: str = Field(unique=True, nullable=False)
    mountpoint: str = Field(nullable=False)
    description: str = Field(nullable=False)

SQLModel.metadata.create_all(engine)

@app.post("/storagedevices/create", response_model=StorageDevice)
def add_storage_device(device: StorageDeviceBase, session: Session = Depends(get_session)):
    new_device = StorageDevice(**device.model_dump())
    session.add(new_device)
    session.commit()
    session.refresh(new_device)
    return new_device

@app.get("/storagedevices/", response_model=List[StorageDevice])
def get_storage_devices(session: Session = Depends(get_session)):
    devices = session.exec(select(StorageDevice)).all()
    return devices

from fastapi import HTTPException

@app.get("/storagedevices/{device_id}", response_model=StorageDevice)
def get_storage_device(device_id: int, session: Session = Depends(get_session)):
    device = session.get(StorageDevice, device_id)
    if not device:
        raise HTTPException(status_code=404, detail=f"StorageDevice not found: {device_id}")
    return device


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)