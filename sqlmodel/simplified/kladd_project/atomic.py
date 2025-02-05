from sqlmodel import Session

from core import create_image_file_core, move_image_file_core, remove_image_file_core, show_stack_core, show_all_stacks_core

from database import engine

# Atomic Actions
def create_image_file(path: str):
    """Add a new ImageFile and create a Stack for it."""
    with Session(engine) as session:
        create_image_file_core(session, path)

def move_image_file(imagefile_id: int, target_stack_id: int):
    """Move an ImageFile from one stack to another."""
    with Session(engine) as session:
        move_image_file_core (session, imagefile_id, target_stack_id)


def remove_image_file(imagefile_id: int):
    """Remove an ImageFile from its current Stack and place it in a new Stack."""
    with Session(engine) as session:
        remove_image_file_core(session, imagefile_id)


def show_stack(stack_id: int):
    """Print the stack ID and all its ImageFiles."""
    with Session(engine) as session:
        show_stack_core(session, stack_id)


def show_all_stacks():
    """Perform show_stack on all stacks in the database."""
    with Session(engine) as session:
        show_all_stacks_core(session)

if __name__ == "__main__":
    print ("Hei")
