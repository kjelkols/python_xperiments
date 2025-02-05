from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from models import ImageFile, Stack  # Import your models
from database import get_session  # Import the session dependency
from core import create_image_file_core, move_image_file_core, remove_image_file_core, show_stack_core, show_all_stacks_core

router = APIRouter()

@router.post("/imagefiles/")
def create_imagefile(path_str: str, session: Session = Depends(get_session)):
    """
    Create a new ImageFile with a new Stack.
    """
    try:
        print ("hei000", "/imagefiles/")
        imagefile = create_image_file_core(session, path_str)
        return imagefile
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/imagefiles/{imagefile_id}/move/{new_stack_id}")
def move_imagefile(imagefile_id: int, new_stack_id: int, session: Session = Depends(get_session)):
    """
    Move an ImageFile to a new Stack.
    """
    try:
        imagefile = move_image_file_core (session, imagefile_id, new_stack_id)
        return imagefile
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#@router.delete("/stacks/cleanup")
#def cleanup_stacks(session: Session = Depends(get_session)):
#    """
#    Delete all empty Stacks.
#    """
#    try:
#        delete_empty_stacks(session)
#        return {"message": "Empty stacks deleted."}
#    except Exception as e:
#        raise HTTPException(status_code=400, detail=str(e))
