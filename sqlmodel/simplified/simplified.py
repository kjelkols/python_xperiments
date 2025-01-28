from sqlmodel import Field, Relationship, SQLModel, create_engine, Session, select
from typing import List, Optional
import simplified_models


# Database setup
DATABASE_URL = "sqlite:///ZZZ_image_stack.db"
engine = create_engine(DATABASE_URL)


def create_tables():
    SQLModel.metadata.create_all(engine)


# Atomic Actions
def create_image_file(path: str):
    """Add a new ImageFile and create a Stack for it."""
    with Session(engine) as session:
        new_stack = simplified_models.Stack()
        session.add(new_stack)
        session.commit()  # Commit to get the stack ID

        new_image_file = simplified_models.ImageFile(path_str=path, stack_id=new_stack.id)
        session.add(new_image_file)
        session.commit()
        print(f"Created ImageFile with ID {new_image_file.id} in Stack {new_stack.id}")


def move_image_file(imagefile_id: int, target_stack_id: int):
    """Move an ImageFile from one stack to another."""
    with Session(engine) as session:
        # Fetch the ImageFile and its current stack
        imagefile = session.get(simplified_models.ImageFile, imagefile_id)
        if not imagefile:
            print("ImageFile not found!")
            return

        current_stack_id = imagefile.stack_id
        imagefile.stack_id = target_stack_id
        session.add(imagefile)
        session.commit()
        print(f"Moved ImageFile {imagefile_id} to Stack {target_stack_id}")

        # Check if the source stack is empty
        if current_stack_id:
            stack = session.get(simplified_models.Stack, current_stack_id)
            if stack and not stack.imagefiles:  # If no images remain
                session.delete(stack)
                session.commit()
                print(f"Deleted empty Stack {current_stack_id}")

def remove_image_file(imagefile_id: int):
    """Remove an ImageFile from its current Stack and place it in a new Stack."""
    with Session(engine) as session:
        # Fetch the ImageFile
        imagefile = session.get(simplified_models.ImageFile, imagefile_id)
        if not imagefile:
            print("ImageFile not found!")
            return

        # Create a new Stack
        new_stack = simplified_models.Stack()
        session.add(new_stack)
        session.commit()  # Commit to get the stack ID

        # Update the ImageFile to reference the new Stack
        current_stack_id = imagefile.stack_id
        imagefile.stack_id = new_stack.id
        session.add(imagefile)
        session.commit()
        print(f"Removed ImageFile {imagefile_id} from Stack {current_stack_id} to new Stack {new_stack.id}")

        # Check if the source stack is empty
        if current_stack_id:
            stack = session.get(simplified_models.Stack, current_stack_id)
            if stack and not stack.imagefiles:  # If no images remain
                session.delete(stack)
                session.commit()
                print(f"Deleted empty Stack {current_stack_id}")


def show_stack(stack_id: int):
    """Print the stack ID and all its ImageFiles."""
    with Session(engine) as session:
        stack = session.get(simplified_models.Stack, stack_id)
        if not stack:
            print("Stack not found!")
            return

        print(f"Stack ID: {stack.id}")
        for imagefile in stack.imagefiles:
            print(f" - ImageFile ID: {imagefile.id}, Path: {imagefile.path_str}")


def show_all_stacks():
    """Perform show_stack on all stacks in the database."""
    with Session(engine) as session:
        stacks = session.exec(select(simplified_models.Stack)).all()
        if not stacks:
            print("No stacks found!")
            return

        for stack in stacks:
            show_stack(stack.id)


# Example Usage
if __name__ == "__main__":
    create_tables()

    # Create ImageFiles
    create_image_file("image1.jpg")
    create_image_file("image2.jpg")

    # Show all stacks
    show_all_stacks()

    # Move ImageFile and handle empty stacks
    move_image_file(imagefile_id=1, target_stack_id=2)

    # Remove an ImageFile into a new Stack
    remove_image_file(imagefile_id=1)

    # Show all stacks after move
    show_all_stacks()
