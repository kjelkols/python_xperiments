from pathlib import Path

from contextlib import asynccontextmanager
from typing import List, Optional
from enum import Enum

from sqlmodel import Field, Relationship, Session, SQLModel, create_engine, select
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
    branch: str = Field(default="") # File name with eventual path
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

    photo_id: Optional[int] = Field(default=None, foreign_key="photo.id") #2
    photo: Optional["Photo"] = Relationship (back_populates="imagefiles") #2

    @staticmethod
    def create_from_file (rootpath:Path, branchpath:Path) -> "ImageFile":
        # Create a new ImageFile object from a file
        fullpath = rootpath / branchpath
        filedata = MyFileData(fullpath)
        return ImageFile(
            branch=branchpath.as_posix(),    
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
            f"ImageFile(id={self.id}, branch='{self.branch}', "
            f""
        )
    def myrepr(self):
        # Show basic details about the ImageFile and its associated Batch
        return (
            f"ImageFile(id={self.id}, branch='{self.branch}', "
            f"batch_id={self.batch_id}, batch_descr='{self.batch.descr if self.batch else None}')"
        )
        
class Photo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    caption: str = Field(default="")
    grouptype: GroupType = Field (default=GroupType.MIXED)
    anchor: int = Field (default=0) # Index of the image in imagefiles to represent the photo
   
    imagefiles: List["ImageFile"] = Relationship (back_populates="photo") #2
#    album_list: List["Album"] = Relationship(back_populates="photo_list", link_model=PhotoAlbumLink) #3


    def debug_print(self):
        print (self.model_dump())

def scan_folder (root_path:Path): # Recursively, add all image files
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    IMAGE_RAW_EXTENSIONS = (".nef", ".dng") # Raw files can also be added. Some logic can add matching filenames to the same photo
#    root = Path(path_str)
    if not root_path.is_dir():
        print ( ValueError(f"{path_str} is not a valid directory."))
        return
    # Use rglob to search for files with specified extensions
    filepath_list = []
    for ext in IMAGE_EXTENSIONS:
        filepath_list.extend(root_path.rglob(f'*{ext}'))
    result = []
    for filepath in filepath_list:
#      filename = filepath.as_posix()
      result.append(filepath.relative_to(root_path))
    return result

    

# Set up the database
sqlite_file_name = "zzz_main_all.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=False) #True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Return the number of roots. If 0, one should be created
def debug_check_init():
    print ("debug_check_init")
    with Session(engine) as session:
        statement = select(Root)
        result = session.exec(statement)
        return len(result.all())
        
        
def debug_print():
    
    print ("debug_print")
    with Session(engine) as session:
        print ("===== Root ======")
        statement = select(Root)
        result = session.exec(statement)
        for root in result.all():
#            session.refresh(photo)
            print (root.model_dump())
#        print (result.all())
        print("===== END Root =====")
    

def debug_populate():
    # Found some jpg files here:
    rootpath_str="C:/Users/kjell/OneDrive/VOLUME/2024_PROJECT_TIMELINE/photo_organizer/tiny8/gpt_photo_organizer"
    branchpath="static/photos"
    with Session(engine) as session:
        root = Root(path_str=rootpath_str, descr="Sample root")
        print ("############### Creating root")
        session.add(root)
        session.commit()
        print ("###############Created root:",root.model_dump())
        
        ZZZ="""       
        print ("############### Creating photo")
#        load_imagefile(session, batch1, branch)
        photo = Photo(caption="")
        session.add (photo)
        session.commit()
        print ("###############Created photo:",photo.model_dump())
        
        print ("############### Creating imagefile")
        #Todo: Get data from EXIF
        imagefile = ImageFile(branch=branch, timezone = datetime.now(timezone.utc), quality=3, photo=photo)
        session.add(imagefile)
        print ("###############Created imagefile:",imagefile)
        
        print ("############### Adding imagefile to photo")
        photo.imagefiles.append(imagefile)
        session.refresh(photo)
        session.refresh(imagefile)
        session.commit()
        
        print ("###############Added imagefile to photo",photo.model_dump())
        session.refresh(batch)
        session.refresh(imagefile)
        session.commit()
        print ("   ??????????", "batch=", batch.imagefiles, "imagefile=",imagefile.batch)
        
def test_load_batch():
    with Session(engine) as session:
        statement = select(Batch).where(Batch.id == 1) #.options(joinedload(Batch.imagefiles))
        result = session.exec(statement).first()
        print (result)
        if not result:
            raise HTTPException(status_code=404, detail="Batch not found")
        return result
        """


def print_photo():
    print ("print_photo")
    

    
    
    
if __name__ == "__main__":
    print ("Trying to load some images")
    
    create_db_and_tables()
    if (debug_check_init() == 0):
        print ("No roots, creating one")    
        debug_populate()

    with Session(engine) as session:
        statement = select(Root)
        result = session.exec(statement) 
#        for root in result.all():           
#            print ("Root=", root)
            
        root = result.first()
        
        paths = scan_folder (root.path)
        for path in paths:
            print (path)
            fullpath = root.path / path
            print(fullpath)
            imagefile = ImageFile.create_from_file (root.path, path)
            print (imagefile)
            session.add (imagefile)
            session.commit()
            photo = Photo(caption="")
            session.add (photo)
            session.commit()
            photo.imagefiles.append(imagefile)
            session.refresh(photo)
            session.refresh(imagefile)
            session.commit()

    with Session(engine) as session:
        statement = select(ImageFile)
        result = session.exec(statement) 
        for imagefile in result.all():           
            print ("ImageFile=", imagefile.basename)
 
    with Session(engine) as session:
        statement = select(Photo)
        result = session.exec(statement) 
        print (len(result.all()))
        
    with Session(engine) as session:
        statement = select(Photo)
        result = session.exec(statement) 
        photo = result.first()
        session.refresh(photo)
        print (photo)
        print (photo.imagefiles)
        
        
   
    print ("Panic");exit()    
