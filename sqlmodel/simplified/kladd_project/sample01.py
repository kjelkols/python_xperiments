from atomic import create_image_file, move_image_file, remove_image_file, show_stack, show_all_stacks

def run_example():
    # Create ImageFiles
    create_image_file("image1.jpg")
    create_image_file("image2.jpg")

    # Show all stacks
    print ("########################")
    show_all_stacks()
    print ("########################")

    # Remove an ImageFile into a new Stack
    remove_image_file(imagefile_id=1)

    # Show all stacks after removal
    print ("########################")
    show_all_stacks()
    print ("########################")
    

if __name__ == "__main__":
    from database import helper_delete_database, create_tables
    
    helper_delete_database()
    create_tables()
    
    run_example()
