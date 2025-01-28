from common import get_session
from sqlmodel import select
from imageutil import scan_folder

from models import Root, ImageFile, Stack, Quality, Category, GroupType

def debug_three_stacks(root:Root):
    print ("debug_three_stacks")
    paths = scan_folder (root.path)
    i = 0
    for path in paths:
        print (path)
        imagefile = ImageFile.create_from_file(rootpath=root.path, branchpath=path)
        imagefile_add_with_stack(imagefile)
        if i==2:
            break
        i += 1
    
def imagefile_add_with_stack (imagefile:ImageFile):
    stack = Stack(caption=imagefile.branch_str, grouptype=GroupType.MIXED)
    with get_session() as session:
        session.add(imagefile)
        session.add(stack)
        session.commit()
        imagefile.stack = stack
        session.refresh(imagefile)
        session.commit()
        
def imagefile_delete(imagefile:ImageFile):
    print ("  ########imagefile_delete", imagefile.id, imagefile.stack_id)
    with get_session() as session:
#        session.refresh(imagefile)
#        stack = imagefile.stack
#        if stack:
#            stack.imagefiles.remove(imagefile)
#            if len(stack.imagefiles) == 0:
#                session.delete(stack)
#            session.commit()
        session.refresh(imagefile)
        session.print(imagefile.stack)
        session.delete(imagefile)
        session.commit()

def imagefile_delete_all():
    list = []
    with get_session() as session:
        statement = select(ImageFile)
        results = session.exec(statement)
        list = []+results.all()
        #Todo: Delete stack if empty
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

def root_scan_stacks(root:Root):
    paths = scan_folder (root.path)
    print (f"Found {len(paths)} files in {root.path}")
    ZZZ="""
    with get_session() as session:
        statement = select(Stack).where(Stack.root_id == root.id)
        result = session.exec(statement)
        root.stacks = result.all()
    """


def stack_print_list_all_overview():
    print ("print_stacks")
    with get_session() as session:
        statement = select(Stack)
        result = session.exec(statement)
        for stack in result.all():
            print ("     ",stack_str_imagefiles (stack))
       
def stack_str_imagefiles(stack:Stack):
    lst = stack.imagefiles
    return f"{stack.id}: {[img.id for img in lst]}"
       
def stack_get_position (stack:Stack, imagefile:ImageFile):
    print ("stack_get_position")
    for i in range(len(stack.imagefiles)):
        if stack.imagefiles[i].id == imagefile.id:
            return i
    return -1
            
def stack_set_anchor(stack:Stack, imagefile:ImageFile):
    print ("stack_set_anchor")
    index = stack_get_position(stack, imagefile)
    if index > 0:
        stack.imagefiles.insert (0, stack.imagefiles.pop(index))
        with get_session() as session:
            session.add(stack)
            session.commit()
    return index # Original position

def ZZZ_stack_merge(src:Stack, trg:Stack):
  print ("stack_merge", src, trg)
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
    
  
def stack_merge(src: Stack, trg: Stack):
    print(f"Starting stack_merge: src_id={src.id}, trg_id={trg.id}")
    
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
        print(f"Error during stack_merge: {e}")
        session.rollback()
  
    
    
   
  
  
  