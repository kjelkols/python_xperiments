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

#import os


# The iso format used for text representation of a time stamp
FORMAT_ISO           = "%Y-%m-%d %H:%M:%S"
FORMAT_ISO_MOTO      = "%Y:%m:%d %H:%M:%S" # My Motola phone stores dates in this format
FORMAT_PRETTY        = "%Y-%m-%d %H:%M:%S"


#class Exif: # Static methods



  # ===== DATE AND TIME OPERATIONE =====
  # Dates and times are stored as iso reprentated text
  # Some tweeks are needed to cope with the date formats found in exif data from various makers
  # The standard ISO format is used, without time zone and other specialities
def text2date (txt:str):
      if not txt:
        print ("Text is none")
        txt = "1970-01-01 00:00:00"
      #            0123456789
      example_text = "1955-05-26 16:45:50"
      if len(txt)<len(example_text):
        print ("ERROR: Text too short", txt)
        return None
      format = FORMAT_ISO
      if txt[4]==":":
        format = FORMAT_ISO_MOTO
      print ("HEIIIIII", txt)  
      date = datetime.strptime(txt, format)
      return date

  # Use this iso format format to represent the date
def date2text (date):
      return date.strftime (FORMAT_ISO)

   
def date2pretty (date):
    date.strftime (FORMAT_PRETTY)
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


def parse_metadata (fullpath:Path):
    basename = fullpath.name
    extension = fullpath.suffix
    filesize = fullpath.stat().st_size
    
    exifdata = None
    img = None
    try:
      with open(fullpath, 'rb') as file:
        img = PIL.Image.open(file)
        img.verify()  # Verify the file to ensure it is a valid image
        exifdata = img._getexif()
    except FileNotFoundError:
        print("read_dictionary The image file was not found.", fullpath)
    except PermissionError:
        print("read_dictionary You do not have permission to access this file.", fullpath)
    except IOError as e:
        print(f"read_dictionary An I/O error occurred: {e}", fullpath)
    except Exception as e:
        print(f"read_dictionary An unexpected error occurred: {e}", fullpath)
        
    if exifdata:    
      # Image size, raw data
      width = read_stripped_from_exifdata (exifdata, 40962)
      height = read_stripped_from_exifdata (exifdata, 40963)
      if not width or not height:
        width, height = img.size
      size = [width, height]
        
      # Time taken
      timestamp = read_stripped_from_exifdata (exifdata, 36867)
      
      date = text2date (timestamp)
      
      print ("date",date, type(date))
      timestamp = date2text (date)
  #    unixtime = date2unix (date)

      # Camera
      make = read_stripped_from_exifdata (exifdata, 271)
      model = read_stripped_from_exifdata (exifdata, 272)
      
      # GPS
      gps = None 
      gpsdata = read_stripped_from_exifdata (exifdata, 34853)
      if gpsdata and len (gpsdata) > 1:
        # Longitude
        tuple_longitude = gpsdata[4]
        ref_longitude = gpsdata[3]
        gps_longitude = float(tuple_longitude[0]) + float(tuple_longitude[1]/60) +  float(tuple_longitude[2])/3600 # Last tuple should be timezone. Need this also
        if ref_longitude != 'E':
          gps_longitude = -gps_longitude
        # Latitude
        tuple_latitude = gpsdata[2]
        ref_latitude = gpsdata[1]
        gps_latitude = float(tuple_latitude[0]) + float(tuple_latitude[1]/60) +  float(tuple_latitude[2])/3600
        if ref_latitude != 'N':
            gps_latitude = -gps_latitude
            
        timezone = TimezoneFinder().timezone_at(lat=gps_latitude, lng=gps_longitude)
        # Other GPS data is also retrieved
  #      gps_datum = "DUMMY" #get_dictionary_with_default (gpsdata, 18, "")
  #      gps_height = 999999 #get_dictionary_with_default (gpsdata, 6, 0.0)
        gps = {
          "longitude" : gps_longitude,
          "latitude" : gps_latitude,
          "timezone" : timezone,
        }
        
      # If active, these postedit operations shall be performed, in this sequence
      # When changed, the thumbnail and all cached images should be regenerated
      postedit_default = {
        "rotation" : 0,              # Post-rotate, degrees
        "crop" : (0, 0, 100, 100),   # Cropped corner position after rotation
        "exposure" : 0,              # Exposure correction
      }
    else:
      size = None
      timestamp = ""
      make = ""   
      model = ""  
      gps = None
      
    return {
      "basename" : basename,        # Base name of the image file
      "extension" : extension,      # Extension of the image file
      "filesize" : filesize,
      "size" : size,
      "timestamp" : timestamp,
      "make" : make,
      "model" : model,
      "gps" : gps,
      "postedit" : None,
      "aux" : None, # Reserved for later additions
    }
  
def dict_pretty (dict):
    return json.dumps(dict, indent=2, sort_keys=False)
    
def test_time_conversion ():
    print ("-----> test_time_conversion")
  #  datetime_str = "2024:05:23 22:12:14"
    text = "2024:05:23 22:12:14"
    date = text2date (text)
    print ("date",date, type(date))
    
    text1 = date2text(date)
    print ("text1",text1, type(text))
    
def test_read_exif ():
    print ("-----> test_read_exif")
    fullname = "D:/2021_BILDER/KAMERA/year_2024/2024_05_05_england/20240503_091250.JPG"
    dict = parse_metadata (Path(fullname))
    print(dict_pretty(dict))
#    print (dict)


if __name__ == "__main__":
#  fullname = "D:/2021_BILDER/KAMERA/year_2024/2024_05_05_england/20240503_091250.JPG"

  test_time_conversion ()
    
  test_read_exif()
  
  pth = Path("fide_jeans.png")
  print (dict_pretty(parse_metadata (pth)))
  print (generate_image_hash(pth))
