from sqlmodel import select
from common import get_session, create_db_and_tables
from models import Root, ImageFile, Photo, Quality, Category, GroupType
from actions import photo_print_list_all_overview, root_scan_photos
from actions import imagefile_delete_all, debug_three_photos, imagefile_print_all

# Return the number of roots. If 0, one should be created
def debug_check_init():
    print ("debug_check_init")
    with get_session() as session:
        statement = select(Root)
        result = session.exec(statement)
        return len(result.all())
        
def assure_one_root():
    # Found some jpg files here:
    rootpath_str="C:/Users/kjell/OneDrive/VOLUME/2024_PROJECT_TIMELINE/photo_organizer/tiny8/gpt_photo_organizer"
    branchpath="static/photos"
    with get_session() as session:
        root = Root(path_str=rootpath_str, descr="Sample root")
        print ("############### Creating root")
        session.add(root)
        session.commit()
        print ("###############Created root:",root.model_dump())

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
        assure_one_root()
       
# Retrieve the root from database
    root = None
    with get_session() as session:
        statement = select(Root)
        result = session.exec(statement) 
        root = result.first()
#        root = result.all()[0]
#        print ("Roots:", len(result.all()))
        print ("Root=", root)
        print (root.model_dump())        
        
    print ("heiii", root)
    lst = root_scan_photos(root)
    
# Try to scan the folder
    paths = scan_folder (root.path)
    for path in paths:
        print (path)

    
#    print ("Found", len(lst), "files in", root.path)
        
    print ("Photos:")
    photo_print_list_all_overview()

    debug_three_photos(root)
    photo_print_list_all_overview()
    imagefile_delete_all()
    photo_print_list_all_overview()
    print ("Panic");exit()    

