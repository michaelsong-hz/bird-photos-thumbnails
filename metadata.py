import os
import sys
import json
from pathlib import Path
from datetime import datetime
from operator import attrgetter
from PIL import Image, ExifTags


class ExifData():
    def __init__(self, url_image_path, exif_datetime=None, f_number=None, exposure_time=None, iso=None):
        self.url_image_path = url_image_path
        self.exif_datetime = exif_datetime
        self.f_number = f_number
        self.exposure_time = exposure_time
        self.iso = iso

    def to_json(self):
        if self.exif_datetime:
            return {
                "url": self.url_image_path,
                "metadata": {
                    "date": self.exif_datetime.strftime("%Y-%m-%d"),
                    "fNum": str(self.f_number.numerator),
                    "fDen": str(self.f_number.denominator),
                    "eNum": str(self.exposure_time.numerator),
                    "eDen": str(self.exposure_time.denominator),
                    "ISO": str(self.iso)
                }
            }
        else:
            return {
                "url": self.url_image_path,
                "metadata": None
            }


def main():
    input_directory = os.path.normpath(sys.argv[1])
    output_file = "{}.json".format(input_directory + " Metadata")
    print("Processing files in: \"{}\"".format(input_directory))

    exif_data_list = []
    non_exif_data_list = []
    for infile in os.listdir(input_directory):
        index_image(input_directory, infile,
                    exif_data_list, non_exif_data_list)
    exif_data_list.sort(key=attrgetter("exif_datetime"))
    non_exif_data_list.sort(key=attrgetter("url_image_path"))

    exif_data_json = []
    for exif_datum in exif_data_list:
        exif_data_json.append(exif_datum.to_json())
    for non_exif_datum in non_exif_data_list:
        exif_data_json.append(non_exif_datum.to_json())
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(exif_data_json, f, ensure_ascii=False, indent=2)
        print("Wrote to \"{}\"".format(output_file))


def index_image(album_name, image_path, exif_data_list, non_exif_data_list):
    img_path = os.path.join(album_name, image_path)

    img_path_converted = Path(img_path)
    img_path_converted.parts[len(img_path_converted.parts) - 1]
    img_path_converted.parts[len(img_path_converted.parts) - 2]

    url_img_path = "/albums/{}/{}".format(img_path_converted.parts[len(
        img_path_converted.parts) - 2], img_path_converted.parts[len(img_path_converted.parts) - 1])
    img = Image.open(img_path)
    try:
        exif = {ExifTags.TAGS[k]: v for k,
                v in img._getexif().items() if k in ExifTags.TAGS}
    except AttributeError:
        exif = None
    print(img_path)
    if exif and "DateTimeOriginal" in exif and "FNumber" in exif:
        exif_datetime = datetime.strptime(
            exif["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S")
        exif_data_list.append(ExifData(url_img_path, exif_datetime,
                                       exif["FNumber"], exif["ExposureTime"], exif["ISOSpeedRatings"]))
    else:
        non_exif_data_list.append(ExifData(url_img_path))


if __name__ == "__main__":
    main()
