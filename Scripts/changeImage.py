#!/usr/bin/env python3
import PIL
from PIL import Image
import sys
import os
import logging

logging.basicConfig(level=logging.INFO)

def get_file_list(dirpath):
    if len(dirpath) == 0:
        logging.error("Provided source path is empty")
        return None
    if not os.path.isdir(dirpath):
        logging.error("Provided source path is not a directory")
        return None

    file_list = set()

    for file in os.scandir(dirpath):
        logging.info("File path added : {}".format(file.path))
        file_list.add(file.path)

    return file_list

def validate_image(srcpath):
    try:
        logging.info("Attempting to open image at : {}".format(srcpath))
        image = Image.open(srcpath)
        logging.info("Successfully opened image at : {}".format(srcpath))
        return image
    except FileNotFoundError:
        logging.error("Image is missing at source path :" + srcpath)
    except PIL.UnidentifiedImageError:
        logging.error("Failed to identify image at source path :" + srcpath)

    return None

def image_formatting(image, srcpath, destpath, width, height, conversion, format):
        file_name = os.path.basename(srcpath)
        image.resize((width, height)).convert(conversion).save(destpath + file_name, format)
        logging.info("Saved file as : {}".format(file_name))

if __name__ == "__main__":
    if len(sys.argv) > 1 and len(sys.argv) < 4:
        src = sys.argv[1]
        if not os.path.exists(src):
            logging.error("Invalid source path.")
        if len(sys.argv) == 3:
            dest = sys.argv[2]
            if not os.path.exists(dest):
                logging.error("Invalid destination path.")
        else:
            dest = src
            logging.warning("Destination path is set to source path.")

        if os.path.exists(src) and os.path.exists(dest):
            file_list = get_file_list(src)
            if len(file_list) > 0:
                for filepath in file_list:
                    image = validate_image(filepath)
                    if image is not None:
                        image_formatting(image,filepath,dest, 600, 400, "RGB", "JPEG")
                        image.close()
            else:
                logging.warning("No files found at source path : {}".format(src))

    else:
        logging.error("Missing parameters for source and destination paths")
