import atomic_actions
import models
import common
import pathlib

common.create_db_and_tables()

root = atomic_actions.root_create(pathlib.Path("C:/Users/kjell/OneDrive/VOLUME/2024_PROJECT_TIMELINE/photo_organizer/tiny8/gpt_photo_organizer"))  
branch = "static/photos/20240427_102030.JPG"
print(root)

#imagefile = imagefile_create(root, Path("static/photos/zzz.jpg"))  #branch:Path):
imagefile_sample = models.ImageFile.create_from_file(rootpath=root.path, branchpath=pathlib.Path(branch))
print ("imagefile_sample =", imagefile_sample)

imagefile = atomic_actions.imagefile_create(root=root, branch=root.path)
print ("imagefile =", imagefile)

# protonmail.domainkey.d43ghy6hb72yonggxc6ywpa44tajqqvafe3tc7z3uq5qg4p6bf4ea.domains.proton.ch.



