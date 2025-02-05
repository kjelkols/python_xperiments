from sqlmodel import Session, select
from models import ImageFile, Stack

def create_image_file_core(session:Session, path: str):
        """Add a new ImageFile and create a Stack for it."""
        new_stack = Stack()
        session.add(new_stack)
        session.commit()  # Commit to get the stack ID

        new_image_file = ImageFile(path_str=path, stack_id=new_stack.id)
        session.add(new_image_file)
        session.commit()
        session.refresh(new_image_file)
        print(f"Created ImageFile with ID {new_image_file.id} in Stack {new_stack.id}")

def move_image_file_core(session:Session, imagefile_id: int, target_stack_id: int):
        """Move an ImageFile from one stack to another."""
        # Fetch the ImageFile and its current stack
        imagefile = session.get(ImageFile, imagefile_id)
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
            stack = session.get(Stack, current_stack_id)
            if stack and not stack.imagefiles:  # If no images remain
                session.delete(stack)
                session.commit()
                print(f"Deleted empty Stack {current_stack_id}")

def remove_image_file_core(session:Session, imagefile_id: int):
        """Remove an ImageFile from its current Stack and place it in a new Stack."""
        # Fetch the ImageFile
        imagefile = session.get(ImageFile, imagefile_id)
        if not imagefile:
            print("ImageFile not found!")
            return

        # Create a new Stack
        new_stack = Stack()
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
            stack = session.get(Stack, current_stack_id)
            if stack and not stack.imagefiles:  # If no images remain
                session.delete(stack)
                session.commit()
                print(f"Deleted empty Stack {current_stack_id}")

def show_stack_core(session:Session, stack_id: int):
        """Print the stack ID and all its ImageFiles."""
        stack = session.get(Stack, stack_id)
        if not stack:
            print("Stack not found!")
            return

        print(f"Stack ID: {stack.id}")
        for imagefile in stack.imagefiles:
            print(f" - ImageFile ID: {imagefile.id}, Path: {imagefile.path_str}")


def show_all_stacks_core(session:Session):
    """Perform show_stack on all stacks in the database."""
    stacks = session.exec(select(Stack)).all()
    if not stacks:
        print("No stacks found!")
        return

    for stack in stacks:
        show_stack_core(session, stack.id)


