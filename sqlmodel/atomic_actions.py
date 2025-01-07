from common import get_session #, get_workspace_root
from sqlmodel import select
from imageutil import scan_folder

from models import Root, ImageFile, Photo, Quality, Category, GroupType
from pathlib import Path

def root_create(path: Path, descr: str = ""):
    root = Root(path_str=path.as_posix(), descr=descr)
    with get_session() as session:
        session.add(root)
        session.commit()
        session.refresh(root)
    return root

def root_get_by_id (id:int):
    with get_session() as session:
        statement = select(Root).where(Root.id == id)
        result = session.exec(statement)
        return result.first()
    
def root_update (root:Root):
    with get_session() as session:
        session.add(root)
        session.commit()
        session.refresh(root)
        return root

def root_print_all():
    print ("root_print_all")    
    with get_session() as session:        
        statement = select(Root)
        result = session.exec(statement)
        for root in result.all():
            print (root)
    
def root_scan_imagefiles(root:Root):
    paths = scan_folder (root.get_path())
    print (f"Found {len(paths)} files in {root.path_str}")
    ZZZ="""
    with get_session() as session:
        statement = select(ImageFile).where(ImageFile.branch_id == root.id)
        result = session.exec(statement)
        root.imagefiles = result.all()
    """

def root_scan_photos(root:Root):
    paths = scan_folder (root.path)
    print (f"Found {len(paths)} files in {root.path}")
    ZZZ="""
    with get_session() as session:
        statement = select(Photo).where(Photo.root_id == root.id)
        result = session.exec(statement)
        root.photos = result.all()
    """

def imagefile_create(root:Root, branch:Path):
    imagefile = ImageFile(root=root, branch_str=branch.as_posix())
    with get_session() as session:
        session.add(imagefile)
        session.add(root)
        session.commit()
        session.refresh(imagefile)
        session.refresh(root)
        return imagefile

def imagefile_update (imagefile:ImageFile):
    with get_session() as session:
        session.add(imagefile)
        session.commit()
        session.refresh(imagefile)
        return imagefile

def photo_create():
    photo = Photo()
    with get_session() as session:
        session.add(photo)
        session.commit()
        return photo

def photo_update (photo:Photo):
    with get_session() as session:
        session.add(photo)
        session.commit()
        session.refresh(photo)
        return photo

def photo_add_imagefile_fist_attempt (photo:Photo, imagefile:ImageFile):
# I try to add an image file to the photo by appending to the photo's imagefiles
# However, this is not enough. If the image file belongs to another photo,
# it must be removed from that list.
# I don't understand why it should be possible to manipulate the photo's imagefiles
# It should be enough to set the image's photo_id to the photo's id.
# The list should be updated automatically by refreshing the photo.
    with get_session() as session:
        session.add(photo)
        photo.imagefiles.append(imagefile)
        session.refresh(photo)
        session.refresh(imagefile)
        session.commit()
        return photo

def photo_print_imagefiles(photo:Photo):
    with get_session() as session:
        txt = f"Photo {photo.id} "
        statement = select(ImageFile).where(ImageFile.photo_id == photo.id)
        result = session.exec(statement)
        session.refresh (photo)
        for imagefile in result.all():
            session.refresh (imagefile)
            txt += f"{imagefile.id} "
        print (txt)

# Second attempt:
def imagefile_set_photo (imagefile:ImageFile, photo:Photo):
    with get_session() as session:
        session.add(imagefile)
        imagefile.photo = photo        
        session.refresh(imagefile)
        session.refresh(photo)
        session.commit()        
        return imagefile


if __name__ == "__main__":
    from common import create_db_and_tables
    create_db_and_tables()

    root = root_create(Path("C:/Users/kjell/OneDrive/VOLUME/2024_PROJECT_TIMELINE/photo_organizer/tiny8/gpt_photo_organizer"))  
    
    print("rootaaa:", root)

    root.descr = "Heiiiiii"
    print("rootbbb:", root)
    root = root_update(root)
    
    print("rootccc:", root)
    
    print ("rootddd", root_get_by_id(root.id))

    
    root_print_all()

    
    imagefile = imagefile_create(root, Path("static/photos/zzz.jpg"))  #branch:Path):
    print (imagefile)

   
    photo = photo_create()
    print (photo)
    
#    photo_add_imagefile_fist_attempt(photo, imagefile)
    imagefile_set_photo(imagefile, photo)
    print (photo)
    print (imagefile)
    photo_print_imagefiles(photo)

    print ("Panic"); exit()
    
    
    
    
    
#    root_print_all()

#    root_scan_imagefiles(root)
   
  
  
  