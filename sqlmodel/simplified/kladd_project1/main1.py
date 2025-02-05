from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from database import engine, SQLModel
from models import ImageFile, Stack

# Create database tables (if they don't exist)
SQLModel.metadata.create_all(engine)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Homepage that lists all Stacks and their ImageFiles.
    """
    with Session(engine) as session:
        stacks = session.exec(select(Stack)).all()
        for stack in stacks:
            stack.imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
    return templates.TemplateResponse(
        "index1.html",
        {"request": request, "stacks": stacks},
    )

@app.post("/stacks/")
async def create_stack_with_imagefiles(request: Request, paths: list[str]):
    """
    Create a new Stack with multiple ImageFiles.
    """
    with Session(engine) as session:
        # Create a new Stack
        stack = Stack()
        session.add(stack)
        session.commit()
        session.refresh(stack)

        # Create ImageFiles and associate them with the Stack
        for path in paths:
            imagefile = ImageFile(path_str=path, stack_id=stack.id)
            session.add(imagefile)
        session.commit()

    return {"message": "Stack created successfully!", "stack_id": stack.id}

@app.get("/stacks/", response_class=HTMLResponse)
async def list_stacks_with_imagefiles(request: Request):
    """
    List all Stacks along with their associated ImageFiles.
    """
    with Session(engine) as session:
        stacks = session.exec(select(Stack)).all()
        for stack in stacks:
            stack.imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
    return templates.TemplateResponse(
        "stacks.html",
        {"request": request, "stacks": stacks},
    )