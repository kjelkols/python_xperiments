from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from fastapi import HTTPException
from fastapi import Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models import ImageFile, Stack  # Import your models
from database import get_session  # Import the session dependency

router = APIRouter()

# Load Jinja2 templates
templates = Jinja2Templates(directory="templates")

#@router.post("/imagefiles/")
#def create_imagefile(path_str: str, session: Session = Depends(get_session)):

# Homepage: View all stacks
@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, session: Session = Depends(get_session)):
    stacks = session.exec(select(Stack)).all()
    for stack in stacks:
        stack.imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
    return templates.TemplateResponse("index.html", {"request": request, "stacks": stacks})

# Add an image with a new stack
@router.post("/add-image/")
async def add_image(request: Request, path_str: str = Form(...), session: Session = Depends(get_session)):
    stack = Stack()
    imagefile = ImageFile(path_str=path_str, stack=stack)
    session.add(stack)
    session.add(imagefile)
    session.commit()
    return RedirectResponse(url="/", status_code=303)

# Move an image from one stack to another
@router.post("/move-image/{imagefile_id}/to/{new_stack_id}")
async def move_image(imagefile_id: int, new_stack_id: int, session: Session = Depends(get_session)):
    print(f"Moving image {imagefile_id} to stack {new_stack_id}")  # Debugging
    imagefile = session.get(ImageFile, imagefile_id)
    old_stack_id = imagefile.stack_id
    if not imagefile:
        raise HTTPException(status_code=404, detail="ImageFile not found")
    new_stack = session.get(Stack, new_stack_id)
    if not new_stack:
        raise HTTPException(status_code=404, detail="New Stack not found")
    imagefile.stack_id = new_stack.id
    session.commit()
    
    old_stack = session.get(Stack, old_stack_id)
    if old_stack and not old_stack.imagefiles:
        session.delete(old_stack)
        session.commit()
    
    return RedirectResponse(url="/", status_code=303)

@router.post("/split-image/{imagefile_id}/")
async def split_image(imagefile_id: int, session: Session = Depends(get_session)):
    # Fetch the ImageFile
    imagefile = session.get(ImageFile, imagefile_id)
    if not imagefile:
        raise HTTPException(status_code=404, detail="ImageFile not found")
    
    # Create a new Stack
    new_stack = Stack()
    session.add(new_stack)
    session.commit()
    session.refresh(new_stack)

    # Move the ImageFile to the new Stack
    imagefile.stack_id = new_stack.id
    session.commit()
    return RedirectResponse(url="/", status_code=303)

# View a specific stack
@router.get("/stack/{stack_id}", response_class=HTMLResponse)
async def view_stack(request: Request, stack_id: int, session: Session = Depends(get_session)):
    stack = session.get(Stack, stack_id)
    if not stack:
        raise HTTPException(status_code=404, detail="Stack not found")
    
    stack.imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
    return templates.TemplateResponse("stack.html", {"request": request, "stack": stack})