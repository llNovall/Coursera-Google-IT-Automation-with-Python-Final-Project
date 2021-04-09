#!/usr/bin/env python3

import os
import requests
import re
import logging
import sys
import changeImage

logging.basicConfig(level=logging.INFO)

url = "http://ipaddress/fruits"

def get_data_from_text_file(srcpath,extention):
    '''
    This method gets data from provided file with specified extention.
    Returns list of string upon success and returns None upon failure.
    '''
    if srcpath == "": #Checks if path is empty
        logging.error("Failed to get data from text file. Source path is empty.")
        return None

    if not os.path.isfile(srcpath): #Checks if it is file
        logging.error("Source path doesnt point to a file.")
        return None

    if not srcpath.endswith(extention): #Checks if it ends with specified extention
        logging.error("{} doesnt end with {} extention".format(srcpath, extention))
        return None

    data = []
    with open(srcpath, 'r',encoding='utf8') as file: #Opens file

        logging.info("Reading from file : {}".format(srcpath))
        data = [line.strip() for line in file.readlines()] #Reads all lines from file
        return data

    return None

def get_image_name(fileName, textToSearch, textToReplace):
    '''
    This method searches for a text in file name and replaces it with another text.
    Returns replaced text upon success and returns None if failed.
    '''
    if fileName != "":
        if textToSearch != "":
            if textToReplace != "":
                result = re.sub(textToSearch, textToReplace, fileName)

                if result is not None:
                    return result
                else:
                    logging.error("Failed to replace text: {}".format(srcpath))
                    return None
            else:
                logging.error("TextToReplace is missing.")
        else:
            logging.error("TextToSearch is missing.")
    else:
        logging.error("FileName is missing.")

    return None

def format_weight(weight):
    '''
    This method get all the number from the beginning.
    Returns an integer if successful otherwise returns None.
    '''
    if weight == "": # Checks if empty
        logging.error("Weight value is missing.")
        return None

    result = re.match(r'^([0-9]+)', weight)

    if result is not None: #Checks if a match is found
        return int(result.group(1))
    else:
        logging.error("Failed to find weight in : {}".format(weight))
        return None

def format_data(data, fields):
    '''
    This method formats provided data based on provided fields.
    Returns formatted data if successful otherwise returns None.
    '''
    if len(fields) == 0: #Checks if fields is empty
        logging.error("Fields are missing.")
        return None
    if len(data) == 0: #Checks if data is empty
        logging.error("Data is missing.")
        return None
    if len(fields) != len(data): #Checks if data and fields have equal length
        logging.error("Number of fields doesn't match number of data entries.")
        return None

    formatted_data = {}
    for index in range(len(fields)):
        formatted_data[fields[index]] = data[index]

    logging.info("Formatted Data : {}".format(formatted_data))
    return formatted_data

def post_data(dataToPost):
    requests.post(url, data = dataToPost)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        src = sys.argv[1]
        if os.path.exists(src):
            file_list = changeImage.get_file_list(src)
            if len(file_list) > 0:
                for path in file_list:
                    if(path.endswith('.txt')):
                        data = get_data_from_text_file(path, ".txt")
                        if isinstance(data, list):
                            data[1] = format_weight(data[1])
                            data.append(get_image_name(os.path.basename(path),".txt", ".jpeg"))
                            fields = ("name", "weight", "description", "image_name")
                            formatted_data = format_data(data, fields)
                            if formatted_data is not None:
                                post_data(formatted_data)
                        else:
                            logging.error("Failed to properly get data from {}".format(path))
        else:
            logging.error("Invalid source path.")
    else:
        logging.error("Source path is missing.")
