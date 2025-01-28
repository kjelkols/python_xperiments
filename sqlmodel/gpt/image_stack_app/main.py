from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import SQLModel, Session, create_engine, select
from fastapi.staticfiles import StaticFiles
from database import engine, Stack, ImageFile
from sqlalchemy.orm import joinedload

# Create tables if they don't exist
SQLModel.metadata.create_all(engine)

# FastAPI setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

ZZZ='''
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Display all stacks and their image files."""
    with Session(engine) as session:
        stacks = session.exec(select(Stack)).all()
    return templates.TemplateResponse("index.html", {"request": request, "stacks": stacks})
'''

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Display all stacks and their image files."""
    with Session(engine) as session:
        stacks = session.exec(select(Stack).options(joinedload(Stack.imagefiles))).all()
    return templates.TemplateResponse("index.html", {"request": request, "stacks": stacks})

@app.post("/create/")
async def create_image_file(path: str = Form(...)):
    """Create a new ImageFile in a new Stack."""
    with Session(engine) as session:
        new_stack = Stack()
        session.add(new_stack)
        session.commit()

        new_image = ImageFile(path_str=path, stack_id=new_stack.id)
        session.add(new_image)
        session.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/move/")
async def move_image_file(imagefile_id: int = Form(...), target_stack_id: int = Form(...)):
    """Move an ImageFile to another Stack."""
    with Session(engine) as session:
        imagefile = session.get(ImageFile, imagefile_id)
        if imagefile:
            old_stack_id = imagefile.stack_id
            imagefile.stack_id = target_stack_id
            session.add(imagefile)
            session.commit()

            # Delete the old stack if it becomes empty
            if old_stack_id:
                old_stack = session.get(Stack, old_stack_id)
                if old_stack and not old_stack.imagefiles:
                    session.delete(old_stack)
                    session.commit()
    return RedirectResponse(url="/", status_code=303)

@app.post("/remove/")
async def remove_image_file(imagefile_id: int = Form(...)):
    """Remove an ImageFile from its Stack into a new Stack."""
    with Session(engine) as session:
        imagefile = session.get(ImageFile, imagefile_id)
        if imagefile:
            old_stack_id = imagefile.stack_id
            new_stack = Stack()
            session.add(new_stack)
            session.commit()

            imagefile.stack_id = new_stack.id
            session.add(imagefile)
            session.commit()

            # Delete the old stack if it becomes empty
            if old_stack_id:
                old_stack = session.get(Stack, old_stack_id)
                if old_stack and not old_stack.imagefiles:
                    session.delete(old_stack)
                    session.commit()
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
#    uvicorn main:app --reload
    print ("hei")
