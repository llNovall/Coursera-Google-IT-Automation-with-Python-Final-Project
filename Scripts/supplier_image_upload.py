#!/usr/bin/env python3

import requests
import os
import changeImage
import logging
import sys

logging.basicConfig(level=logging.INFO)

url = "http://localhost/upload/"

def get_valid_image_paths(srcpath):
    '''
    This method returns all valid images at srcpath. Return None if nothing found.
    '''
    if srcpath == "": #Checks if dirpath is empty
        logging.error("Provided source path is empty")
        return None
    if not os.path.isdir(srcpath):#Checks if directory exists at dirpath
        logging.error("Provided source path is not a directory")
        return None

    file_list = changeImage.get_file_list(srcpath)#Gets all file paths
    image_paths = set()

    if len(file_list) > 0:
        #The loop will add paths of all valid images to image_paths before returning the list.
        for file in file_list:
            if changeImage.validate_image(file) is not None:
                image_paths.add(file)
        return image_paths
    else:
        logging.warning("No files found at source path : {}".format(srcpath))

    return None

def post_image(imagepath):
    '''
    This method will post the image at provided path to the url.
    '''
    with open(imagepath, 'rb') as opened:
        r = requests.post(url, files={'file':opened})
        logging.info(r)

if __name__ == "__main__":

    if len(sys.argv) == 2:
        src = sys.argv[1]
        if os.path.exists(src):
            image_paths_list = get_valid_image_paths(src)
            if len(image_paths_list) > 0:
                for path in image_paths_list:
                    post_image(path)
        else:
            logging.error("Invalid source path.")
    else:
        logging.error("Source path is missing.")
