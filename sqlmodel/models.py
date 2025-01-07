from pathlib import Path

from typing import List, Optional
from enum import Enum

from sqlmodel import Field, Relationship, SQLModel
#from sqlalchemy.orm import joinedload

from datetime import datetime, timedelta, timezone

from pathlib import Path
from sqlmodel import Field, SQLModel
from typing import Optional
from imageutil import MyFileData

class Quality(int, Enum):
    TRASH = 1
    POOR = 2
    ACCEPTABLE = 3
    GOOD = 4
    EXCELLENT = 5
    MAGNIFICENT = 6

class Category(int, Enum):
    GENERAL = 1 # The most common type, suited for a public photo album
    DOCUMENTATION = 2 # Something interesting to document
    CLIP = 3 # Some text or image from written material for memory
    ITEM = 4 # Some item, e.g. for sale or a collector's item
    EXPERIMENTAL = 5 # Experimental stuff, e.g testing of camera equipment
    
class GroupType(int, Enum):
    MIXED = 1 # A general mix of related photos
    SEQUENCE = 2 # A sequence of images, e.g. for animation
    PANORAMA = 3 # A panoramic view to be stitched together
    
class Root(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descr: str = Field(default="")
    path_str: str = Field(max_length=255)  # Store as string in the database

    imagefiles: List["ImageFile"] = Relationship(back_populates="root")
  
    def __str__ (self) -> str:
        txt = "..."+self.path_str[-30:]
        imagefile_count = -1 #len(self.imagefiles) if self.imagefiles else 0        
        return f"Root({self.id}) {txt} ({self.descr[:30]}) ({imagefile_count})"
#        return f"Root({self.id}) {txt} ({self.descr[:30]}) ()"
    
    def get_path(self) -> Path:
        return Path(self.path_str)
    
    @property
    def path(self) -> Path:
        """Returns the file_path as a pathlib.Path object."""
        return Path(self.path_str)
    @path.setter
    def path(self, value: Path) -> None:
        """Sets the file_path from a pathlib.Path object."""
        self.path_str = str(value)

class ImageFile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    branch_str: str = Field(default="") # File name with eventual path
    basename: str = Field(default="") # File name without path
    extension: str = Field(default="") # File extension
    hash: str = Field(default="") # sha256 hash
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))  # Store as a datetime object
    quality: Quality = Field(default=Quality.ACCEPTABLE)  # Use the enum for quality
    category: Category = Field(default=Category.GENERAL)
    make: str = Field(default="") # Camera make
    model: str = Field(default="") # Camera model
    longitude: float = Field(default=0, nullable=True) # GPS longitude
    latitude: float = Field(default=0, nullable=True) # GPS latitude 
    altitude: float = Field(default=0, nullable=True) # GPS altitude
    timezone: str = Field(default="") # Timezone

    root_id: Optional[int] = Field(default=None, foreign_key="root.id")
    root: Optional[Root] = Relationship(back_populates="imagefiles")
    
    photo_id: Optional[int] = Field(default=None, foreign_key="photo.id") #2
    photo: Optional["Photo"] = Relationship (back_populates="imagefiles") #2

    @staticmethod
    def create_from_file (rootpath:Path, branchpath:Path) -> "ImageFile":
        # Create a new ImageFile object from a file
        fullpath = rootpath / branchpath
        filedata = MyFileData(fullpath)
        return ImageFile(
            branch_str=branchpath.as_posix(),    
            basename=branchpath.name,
            extension=branchpath.suffix,
            timestamp = filedata.timestamp, 
            quality=Quality.ACCEPTABLE, 
            category=Category.GENERAL, 
            latitude=filedata.latitude, 
            longitude=filedata.longitude, 
            altitude=filedata.altitude, 
            timezone=filedata.timezone,
            make=filedata.make,
            model=filedata.model,
            hash=filedata.hash)
        
       
    def debug_print(self):
        print (self.model_dump())
        
    def __repr__(self):
        # Show basic details about the ImageFile and its associated Batch
        return (
            f"ImageFile(id={self.id}, branch='{self.branch_str}', "
            f""
        )
    def myrepr(self):
        # Show basic details about the ImageFile and its associated Batch
        return (
            f"ImageFile(id={self.id}, branch='{self.branch_str}', "
            f"batch_id={self.batch_id}, batch_descr='{self.batch.descr if self.batch else None}')"
        )
        
class Photo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    caption: str = Field(default="")
    grouptype: GroupType = Field (default=GroupType.MIXED)
   
    imagefiles: List["ImageFile"] = Relationship (back_populates="photo") #2
#    album_list: List["Album"] = Relationship(back_populates="photo_list", link_model=PhotoAlbumLink) #3


    def debug_print(self):
        print (self.model_dump())

    
    
if __name__ == "__main__":
    print ("Trying to load some images")
    print ("Panic");exit()    
