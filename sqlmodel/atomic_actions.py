from common import get_session #, get_workspace_root
from sqlmodel import select
from imageutil import scan_folder

from models import Root, ImageFile, Stack, Quality, Category, GroupType
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

def root_scan_stacks(root:Root):
    paths = scan_folder (root.path)
    print (f"Found {len(paths)} files in {root.path}")
    ZZZ="""
    with get_session() as session:
        statement = select(Stack).where(Stack.root_id == root.id)
        result = session.exec(statement)
        root.stacks = result.all()
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

def stack_create():
    stack = Stack()
    with get_session() as session:
        session.add(stack)
        session.commit()
        return stack

def stack_update (stack:Stack):
    with get_session() as session:
        session.add(stack)
        session.commit()
        session.refresh(stack)
        return stack

def stack_add_imagefile_fist_attempt (stack:Stack, imagefile:ImageFile):
# I try to add an image file to the stack by appending to the stack's imagefiles
# However, this is not enough. If the image file belongs to another stack,
# it must be removed from that list.
# I don't understand why it should be possible to manipulate the stack's imagefiles
# It should be enough to set the image's stack_id to the stack's id.
# The list should be updated automatically by refreshing the stack.
    with get_session() as session:
        session.add(stack)
        stack.imagefiles.append(imagefile)
        session.refresh(stack)
        session.refresh(imagefile)
        session.commit()
        return stack

def stack_print_imagefiles(stack:Stack):
    with get_session() as session:
        txt = f"Stack {stack.id} "
        statement = select(ImageFile).where(ImageFile.stack_id == stack.id)
        result = session.exec(statement)
        session.refresh (stack)
        for imagefile in result.all():
            session.refresh (imagefile)
            txt += f"{imagefile.id} "
        print (txt)

# Second attempt:
def imagefile_set_stack (imagefile:ImageFile, stack:Stack):
    with get_session() as session:
        session.add(imagefile)
        imagefile.stack = stack        
        session.refresh(imagefile)
        session.refresh(stack)
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

   
    stack = stack_create()
    print (stack)
    
#    stack_add_imagefile_fist_attempt(stack, imagefile)
    imagefile_set_stack(imagefile, stack)
    print (stack)
    print (imagefile)
#    stack_print_imagefiles(stack)

    print ("Panic"); exit()
    
    
    
    
    
#    root_print_all()

#    root_scan_imagefiles(root)
   
  
  
  