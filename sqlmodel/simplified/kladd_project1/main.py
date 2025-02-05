from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from database import engine, SQLModel
from models import ImageFile, Stack

# Opprett database-tabeller (hvis de ikke finnes)
SQLModel.metadata.create_all(engine)

app = FastAPI()

# Monter statiske filer (CSS, JavaScript, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Last inn Jinja2-maler
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Hovedside som viser en oversikt over ImageFiles og Stacks.
    """
    with Session(engine) as session:
        imagefiles = session.exec(select(ImageFile)).all()
        stacks = session.exec(select(Stack)).all()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "imagefiles": imagefiles, "stacks": stacks},
    )

@app.post("/imagefiles/")
async def create_imagefile(request: Request, path_str: str = Form(...)):
    """
    Opprett en ny ImageFile med en ny Stack.
    """
    with Session(engine) as session:
        stack = Stack()
        imagefile = ImageFile(path_str=path_str, stack=stack)
        session.add(stack)
        session.add(imagefile)
        session.commit()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "message": "ImageFile created successfully!"},
    )

@app.post("/imagefiles/{imagefile_id}/move/{new_stack_id}")
async def move_imagefile(request: Request, imagefile_id: int, new_stack_id: int):
    """
    Flytt en ImageFile til en ny Stack.
    """
    with Session(engine) as session:
        imagefile = session.get(ImageFile, imagefile_id)
        if not imagefile:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "ImageFile not found."},
            )
        new_stack = session.get(Stack, new_stack_id)
        if not new_stack:
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "error": "Stack not found."},
            )
        imagefile.stack = new_stack
        session.commit()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "message": "ImageFile moved successfully!"},
    )

@app.post("/stacks/cleanup")
async def cleanup_stacks(request: Request):
    """
    Slett alle tomme Stacks.
    """
    with Session(engine) as session:
        stacks = session.exec(select(Stack)).all()
        for stack in stacks:
            imagefiles = session.exec(select(ImageFile).where(ImageFile.stack_id == stack.id)).all()
            if not imagefiles:
                session.delete(stack)
        session.commit()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "message": "Empty stacks deleted."},
    )