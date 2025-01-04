from common import get_session
from sqlmodel import select
from imageutil import scan_folder

from models import Root, ImageFile, Photo, Quality, Category, GroupType

def debug_three_photos(root:Root):
    print ("debug_three_photos")
    paths = scan_folder (root.path)
    i = 0
    for path in paths:
        print (path)
        imagefile = ImageFile.create_from_file(rootpath=root.path, branchpath=path)
        imagefile_add_with_photo(imagefile)
        if i==2:
            break
        i += 1
    
def imagefile_add_with_photo (imagefile:ImageFile):
    photo = Photo(caption=imagefile.branch, grouptype=GroupType.MIXED)
    with get_session() as session:
        session.add(imagefile)
        session.add(photo)
        session.commit()
        imagefile.photo = photo
        session.refresh(imagefile)
        session.commit()
        
def imagefile_delete(imagefile:ImageFile):
    print ("  ########imagefile_delete", imagefile.id, imagefile.photo_id)
    with get_session() as session:
#        session.refresh(imagefile)
#        photo = imagefile.photo
#        if photo:
#            photo.imagefiles.remove(imagefile)
#            if len(photo.imagefiles) == 0:
#                session.delete(photo)
#            session.commit()
        session.refresh(imagefile)
        session.print(imagefile.photo)
        session.delete(imagefile)
        session.commit()

def imagefile_delete_all():
    list = []
    with get_session() as session:
        statement = select(ImageFile)
        results = session.exec(statement)
        list = []+results.all()
        #Todo: Delete photo if empty
    for imagefile in list:
        imagefile_delete(imagefile)
        
ZZZ="""
def imagefile_debug_scan_folder(root:Root):
    print ("imagefile_test_scan_folder")
    paths = scan_folder (root.path)
    i = 0
    for path in paths:
        print (path)
        with get_session() as session:
            imagefile = ImageFile.from_path(path_str=path, root=root)
            session.add(imagefile)
            session.commit()
        if i==2:
            break
        i += 1
"""
            
def imagefile_print_all():
    print ("imagefile_print_all")
    with get_session() as session:
        statement = select(ImageFile)
        result = session.exec(statement)
        for imagefile in result.all():
            print (imagefile.model_dump())
            
        
        
        
        
#    print (f"Found {len(paths)} files in {root.path}")

def root_scan_photos(root:Root):
    paths = scan_folder (root.path)
    print (f"Found {len(paths)} files in {root.path}")
    ZZZ="""
    with get_session() as session:
        statement = select(Photo).where(Photo.root_id == root.id)
        result = session.exec(statement)
        root.photos = result.all()
    """


def photo_print_list_all_overview():
    print ("print_photos")
    with get_session() as session:
        statement = select(Photo)
        result = session.exec(statement)
        for photo in result.all():
            print ("     ",photo_str_imagefiles (photo))
       
def photo_str_imagefiles(photo:Photo):
    lst = photo.imagefiles
    return f"{photo.id}: {[img.id for img in lst]}"
       
def photo_get_position (photo:Photo, imagefile:ImageFile):
    print ("photo_get_position")
    for i in range(len(photo.imagefiles)):
        if photo.imagefiles[i].id == imagefile.id:
            return i
    return -1
            
def photo_set_anchor(photo:Photo, imagefile:ImageFile):
    print ("photo_set_anchor")
    index = photo_get_position(photo, imagefile)
    if index > 0:
        photo.imagefiles.insert (0, photo.imagefiles.pop(index))
        with get_session() as session:
            session.add(photo)
            session.commit()
    return index # Original position

def ZZZ_photo_merge(src:Photo, trg:Photo):
  print ("photo_merge", src, trg)
  img_src = src.imagefiles[0]
  img_trg = trg.imagefiles[0]
  src.imagefiles.remove(img_src)
  trg.imagefiles.insert(img_trg)
  with get_session() as session:
    session.add(src)
    session.add(trg)
    session.add(img_src)
    session.add(img_trg)
    session.commit()
    if len(src.imagefiles)==0:
        session.delete(src)
        session.commit()
    
  
def photo_merge(src: Photo, trg: Photo):
    print(f"Starting photo_merge: src_id={src.id}, trg_id={trg.id}")
    
    # Ensure there are images to move
    if not src.imagefiles:
        print(f"No images in src (id={src.id}) to merge.")
        return
    
    img_src = src.imagefiles[0]
    
    # Transfer the image
    src.imagefiles.remove(img_src)
    trg.imagefiles.insert(0, img_src)
    
    try:
        with get_session() as session:
            # Add changes to the session
            session.add(src)
            session.add(trg)
            
            # Commit changes
            session.commit()
            
            # Delete `src` if it has no images left
            if not src.imagefiles:
                print(f"Deleting src (id={src.id}) as it has no more images.")
                session.delete(src)
                session.commit()
    except Exception as e:
        print(f"Error during photo_merge: {e}")
        session.rollback()
  
    
    
   
  
  
  