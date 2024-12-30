from pathlib import Path
from typing import Optional
from pydantic import BaseModel, field_validator
from datetime import datetime
from PIL import Image, ExifTags
from timezonefinder import TimezoneFinder
import pytz


class ExifData(BaseModel):
    time_taken: Optional[datetime]
    make: Optional[str]
    model: Optional[str]
    timezone: Optional[str]

    @field_validator("time_taken", mode="before")
    def parse_time_taken(cls, value):
        if value:
            try:
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
            except ValueError as e:
                raise ValueError(f"Invalid datetime format: {value}") from e
        return None


def extract_exif(filepath: Path) -> Optional[ExifData]:
    """
    Extract EXIF data from a JPEG file and return as an ExifData object.
    """
    try:
        with Image.open(filepath) as img:
            exif = img._getexif()
            if not exif:
                print(f"No EXIF data found in {filepath}")
                return None
            
            # Map EXIF tag IDs to human-readable names
            exif_data = {ExifTags.TAGS[k]: v for k, v in exif.items() if k in ExifTags.TAGS}
            
            # Extract relevant fields
            time_taken = exif_data.get("DateTimeOriginal")
            make = exif_data.get("Make")
            model = exif_data.get("Model")
            
            # Attempt to extract GPS-based timezone
            gps_info = exif_data.get("GPSInfo")
            timezone = None
            if gps_info:
                gps_lat = gps_info.get(2)  # GPS Latitude
                gps_lon = gps_info.get(4)  # GPS Longitude
                if gps_lat and gps_lon:
                    # Convert GPS coordinates to decimal degrees
                    lat = _convert_gps_to_decimal(gps_lat)
                    lon = _convert_gps_to_decimal(gps_lon)
                    timezone = TimezoneFinder().timezone_at(lat=lat, lng=lon)

            return ExifData(
                time_taken=time_taken,
                make=make,
                model=model,
                timezone=timezone,
            )
    except Exception as e:
        print(f"Error reading EXIF data from {filepath}: {e}")
        return None


def _convert_gps_to_decimal(gps_coord):
    """
    Helper function to convert GPS coordinates from EXIF format to decimal degrees.
    """
    degrees = gps_coord[0][0] / gps_coord[0][1]
    minutes = gps_coord[1][0] / gps_coord[1][1]
    seconds = gps_coord[2][0] / gps_coord[2][1]
    return degrees + (minutes / 60.0) + (seconds / 3600.0)


# Example usage
if __name__ == "__main__":
    jpeg_path = Path("example.jpg")  # Replace with your JPEG file path
    exif_data = extract_exif(jpeg_path)
    if exif_data:
        print(exif_data.json(indent=4))
