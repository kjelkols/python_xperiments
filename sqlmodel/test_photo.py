from sqlmodel import select
from common import get_session, create_db_and_tables
from models import Root, ImageFile, Photo, Quality, Category, GroupType
from actions import photo_print_list_all_overview

# Return the number of roots. If 0, one should be created
def debug_check_init():
    print ("debug_check_init")
    with get_session() as session:
        statement = select(Root)
        result = session.exec(statement)
        return len(result.all())
        
def debug_two_photos():
    print ("debug_two_photos")
def debug_print():
    
    print ("debug_print")
    with get_session() as session:
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
    with get_session() as session:
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
    with get_session() as session:
        statement = select(Batch).where(Batch.id == 1) #.options(joinedload(Batch.imagefiles))
        result = session.exec(statement).first()
        print (result)
        if not result:
            raise HTTPException(status_code=404, detail="Batch not found")
        return result
        """

def ZZZ_photo_print_list_all_overview():
    print ("print_photos")
    with get_session() as session:
        statement = select(Photo)
        result = session.exec(statement)
        for photo in result.all():
            lst = photo.imagefiles
            print (photo.id, ":",[img.id for img in lst])
#            print (photo, lst)

def print_photo():
    print ("print_photo")
    

    
if __name__ == "__main__":
    from imageutil import scan_folder
    
    
    print ("Trying to load some images")
    create_db_and_tables()
    if (debug_check_init() == 0):
        print ("No roots, creating one")    
        debug_populate()
        
    print ("Photos:")
    photo_print_list_all_overview()
   
    print ("Panic");exit()    


    ZZZ1="""

    with get_session() as session:
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

    with get_session() as session:
        statement = select(ImageFile)
        result = session.exec(statement) 
        for imagefile in result.all():           
            print ("ImageFile=", imagefile.basename)
 
    with get_session() as session:
        statement = select(Photo)
        result = session.exec(statement) 
        print (len(result.all()))
        
    with get_session() as session:
        statement = select(Photo)
        result = session.exec(statement) 
        photo = result.first()
        session.refresh(photo)
        print (photo)
        print (photo.imagefiles)
    """
        
        
