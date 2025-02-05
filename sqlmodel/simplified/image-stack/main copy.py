# main.py
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from database import engine, get_session
from models import ImageFile, Stack, SQLModel

# Create database tables (if they don't exist)
SQLModel.metadata.create_all(engine)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Homepage: View all stacks
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, session: Session = Depends(get_session)):
    stacks = session.exec(select(Stack)).all()
    for stack in stacks:
        stack.imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
    return templates.TemplateResponse("index.html", {"request": request, "stacks": stacks})

# Add an image with a new stack
@app.post("/add-image/")
async def add_image(request: Request, path_str: str = Form(...), session: Session = Depends(get_session)):
    stack = Stack()
    imagefile = ImageFile(path_str=path_str, stack=stack)
    session.add(stack)
    session.add(imagefile)
    session.commit()
    return RedirectResponse(url="/", status_code=303)

# Move an image from one stack to another
@app.post("/move-image/{imagefile_id}/to/{new_stack_id}")
async def move_image(imagefile_id: int, new_stack_id: int, session: Session = Depends(get_session)):
    print(f"ZZZMoving image {imagefile_id} to stack {new_stack_id}")  # Debugging    
    imagefile = session.get(ImageFile, imagefile_id)
    if not imagefile:
        raise HTTPException(status_code=404, detail="ImageFile not found")
    
    new_stack = session.get(Stack, new_stack_id)
    if not new_stack:
        raise HTTPException(status_code=404, detail="New Stack not found")
    
    imagefile.stack_id = new_stack.id
    session.commit()
    return RedirectResponse(url="/", status_code=303)

# View a specific stack
@app.get("/stack/{stack_id}", response_class=HTMLResponse)
async def view_stack(request: Request, stack_id: int, session: Session = Depends(get_session)):
    stack = session.get(Stack, stack_id)
    if not stack:
        raise HTTPException(status_code=404, detail="Stack not found")
    
    stack.imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
    return templates.TemplateResponse("stack.html", {"request": request, "stack": stack})

# View all stacks
@app.get("/stacks/", response_class=HTMLResponse)
async def view_all_stacks(request: Request, session: Session = Depends(get_session)):
    stacks = session.exec(select(Stack)).all()
    for stack in stacks:
        stack.imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
    return templates.TemplateResponse("index.html", {"request": request, "stacks": stacks})