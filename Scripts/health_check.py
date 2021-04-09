#!/usr/bin/env python3
import report_email as email
import shutil
import psutil
import socket
import logging
import time

logging.basicConfig(level=logging.INFO)

sender = "automation@example.com"
receiver = "username@example.com"
body = "Please check your system and resolve the issue as soon as possible."

def report_email(subject):
    '''
    This method creates an email based on error and sends it to receiver.
    '''
    message = email.generate_email(sender, receiver, subject, body)
    if message is not None:
        email.send_email(message)
    else:
        logging.error("Failed to send error report.")

def check_cpu_usage():
    '''
    This method checks cpu usage.
    If cpu usage is above 80 percent, then an error email is sent to the receiver.
    '''
    usage = psutil.cpu_percent(1)
    logging.info("Current CPU usage :{}".format(usage))
    if usage > 80:
        report_email("Error - CPU usage is over 80%")

def check_disk_usage():
    '''
    This method checks if free space is above 20 percent.
    If not, sends an error email to the receiver.
    '''
    total, used, free = shutil.disk_usage("/")
    logging.info("Current free space in disk : {}".format(free/total))
    if free / total < 0.2:
         report_email("Error - Available disk space is less than 20%")

def convert_bytes_to_megabytes(bytes):
    '''
    This method converts bytes to megabytes.
    '''
    return bytes * (9.537 * 10**-7)

def check_memory_usage():
    '''
    This method checks memory usage.
    If free memory is below 500 MB, then an error email is sent to the receiver.
    '''
    free_memory = psutil.virtual_memory()[4]
    free_memory_mb = convert_bytes_to_megabytes(free_memory)
    logging.info("Current free memory : {}".format(free_memory_mb))
    if free_memory_mb < 500:
        report_email("Error - Available memory is less than 500MB")

def check_if_localhost_is_resolved():
    '''
    Checks if local host is resolved to 127.0.0.1.
    If not, an error email is sent to the receiver.
    '''
    resolved = False
    try:
        if "127.0.0.1" == socket.gethostbyname("localhost"):
            resolved = True
        else:
            resolved = False
    except:
        resolved = False

    if not resolved:
        report_email("Error - localhost cannot be resolved to 127.0.0.1")

if __name__ == "__main__":

    starttime = time.time()
    while True:
        check_cpu_usage()
        check_disk_usage()
        check_memory_usage()
        check_if_localhost_is_resolved()
        time.sleep(60.0 - ((time.time() -starttime) % 60.0))
