import PIL.Image
from datetime import datetime
#import time
import calendar
# from zoneinfo import ZoneInfo # Requires python 3.9
import json
import locale
import platform
from pathlib import Path
from timezonefinder import TimezoneFinder
import hashlib

DATE_FORMAT_ISO           = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT_ISO_MOTO      = "%Y:%m:%d %H:%M:%S" # My Motola phone stores dates in this format

def text2date (txt:str):
# The iso format used for text representation of a time stamp
    if not txt:
        print ("Text is none")
        txt = "1970-01-01 00:00:00"
    #            0123456789
    example_text = "1955-05-26 16:45:50"
    if len(txt)<len(example_text):
        print ("ERROR: Text too short", txt)
        return None
    format = DATE_FORMAT_ISO
    if txt[4]==":":
        format = DATE_FORMAT_ISO_MOTO
    print ("HEIIIIII", txt)  
    date = datetime.strptime(txt, format)
    return date

def date2text (date):
      return date.strftime (DATE_FORMAT_ISO)

def date2pretty (date):
    os_name = platform.system()
    if os_name == 'Windows':
      locale.setlocale(locale.LC_TIME, 'no_NO')
    else:
      locale.setlocale(locale.LC_TIME, 'no_NO.UTF-8')
    format = "%A, %B %d, %Y %I:%M %p"
    return date.strftime(format)

def read_stripped_from_exifdata (exifdata, index):
    found = exifdata.get(index)
    if type(found)==str:
      found = found.rstrip('\x00') # Text may have been padded with null
    return found

def generate_image_hash(file_path: Path, hash_function="sha256") -> str:
    """
    Generate a unique hash for an image file.

    :param file_path: Path to the image file.
    :param hash_function: Hash function to use (e.g., 'md5', 'sha1', 'sha256').
    :return: Hexadecimal hash of the image file.
    """
    hash_func = getattr(hashlib, hash_function)()  # Get the desired hash function
    with file_path.open("rb") as file:  # Open file in binary mode
        while chunk := file.read(8192):  # Read in chunks
            hash_func.update(chunk)
    return hash_func.hexdigest()

def retrieve_rawexif_if_exists (fullpath:Path):
    result = None
    try:
      with open(fullpath, 'rb') as file:
        img = PIL.Image.open(file)
        img.verify()  # Verify the file to ensure it is a valid image
        result = img._getexif()
    except FileNotFoundError:
        print("retrieve_rawexif_if_exists: read_dictionary The image file was not found.", fullpath)
    except PermissionError:
        print("retrieve_rawexif_if_exists: read_dictionary You do not have permission to access this file.", fullpath)
    except IOError as e:
        print(f"retrieve_rawexif_if_exists: read_dictionary An I/O error occurred: {e}", fullpath)
    except Exception as e:
        print(f"retrieve_rawexif_if_exists: read_dictionary An unexpected error occurred: {e}", fullpath)
    return result

def scan_folder (root_path:Path): # Recursively, add all image files
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    IMAGE_RAW_EXTENSIONS = (".nef", ".dng") # Raw files can also be added. Some logic can add matching filenames to the same photo
    if not root_path.is_dir():
        print ( ValueError(f"{root_path} is not a valid directory."))
        return
    # Use rglob to search for files with specified extensions
    filepath_list = []
    for ext in IMAGE_EXTENSIONS:
        filepath_list.extend(root_path.rglob(f'*{ext}'))
    result = []
    for filepath in filepath_list:
#      filename = filepath.as_posix()
      result.append(filepath.relative_to(root_path))
    return result

    

class MyFileData:
    def __init__ (self, fullpath:Path):
        self.fullname = fullpath.as_posix()
        self.basename = fullpath.name
        self.extension = fullpath.suffix
        if fullpath.is_file():
            self.filesize = fullpath.stat().st_size
            self.hash = generate_image_hash(fullpath)
        else:
            self.filesize = -1
            self.hash = None
        self.width = None
        self.height = None
        self.timestamp = None
        self.make = None
        self.model = None
        self.latitude = None
        self.longitude = None 
        self.altitude = None  
        self.timezone = None
            
            
           
        rawexif = retrieve_rawexif_if_exists (fullpath)
        if rawexif:
            self.width = rawexif[40962]
            self.height = rawexif[40963]
            self.timestamp = rawexif[36867]
            self.make = rawexif[271]
            self.model = rawexif[272]
            gpsdata = read_stripped_from_exifdata (rawexif, 34853)
            if gpsdata and len (gpsdata) > 1:
              # Longitude
              tuple_longitude = gpsdata[4]
              ref_longitude = gpsdata[3]
              self.longitude = float(tuple_longitude[0]) + float(tuple_longitude[1]/60) +  float(tuple_longitude[2])/3600 # Last tuple should be timezone. Need this also
              if ref_longitude != 'E':
                self.longitude = -self.longitude
              # Latitude
              tuple_latitude = gpsdata[2]
              ref_latitude = gpsdata[1]
              self.latitude = float(tuple_latitude[0]) + float(tuple_latitude[1]/60) +  float(tuple_latitude[2])/3600
              if ref_latitude != 'N':
                  self.latitude = -self.latitude
              self.timezone = TimezoneFinder().timezone_at(lat=self.latitude, lng=self.longitude)

if __name__ == "__main__":
    fullname = "D:/2021_BILDER/KAMERA/year_2024/2024_05_05_england/20240503_091250z.JPG"

    myfiledata = MyFileData (Path(fullname))
    print (myfiledata.__dict__)
