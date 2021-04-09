#!/usr/bin/env python3

import os
from datetime import date
import reports
import email.message
import smtplib
import mimetypes
import run
import sys
import changeImage
import logging

def generate_attachment(attachment_path):
    '''
    This method generates attachment pdf required for email message.
    Return True if success otherwise returns False.
    '''
    if len(sys.argv) == 2: #Checks if path for data is provided
        src = sys.argv[1]
        if os.path.exists(src): #Checks if path exists
            file_list = changeImage.get_file_list(src)
            if len(file_list) > 0: #Checks if file list is empty
                logging.info("Creating paragraph.")
                paragraph = ["<br/>"]

                #This loop will generate required paragraph based on data read from txt files
                for path in file_list:
                    if(path.endswith('.txt')):
                        data = run.get_data_from_text_file(path, ".txt")
                        if data is not None:
                            if len(data) == 3:
                                paragraph.append("name :{}".format(data[0]))
                                paragraph.append("<br/>")
                                paragraph.append("weight:{}".format(data[1]))
                                paragraph.append("<br/><br/>")
                            else:
                                logging.error("Missing fields.")
                        else:
                            logging.error("Missing data.")

                if len(paragraph) > 0: #Checks if paragraph is created successfully
                    paragraph = "".join(paragraph)
                    today = date.today()
                    title = "Processed Update on {}".format(today.strftime("%B %d, %Y"))
                    reports.generate_report(attachment_path, title, paragraph)
                    return True
                else:
                    logging.error("Failed to create paragraph.")
        else:
            logging.error("Failed to find path : {}".format(src))
    else:
        logging.error("Missing path for data.")

        return False

def generate_email(sender, receiver, subject, body, attachment_path = ""):
    '''
    This method generates an email message.
    '''
    message = email.message.EmailMessage()

    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject
    message.set_content(body)

    #Creates an attachment if attachment_path is provided
    if len(attachment_path) > 0:
        attachment_filename = os.path.basename(attachment_path)

        mime_type, _ = mimetypes.guess_type(attachment_path)
        mime_type, mime_subtype = mime_type.split('/',1)

        with open(attachment_path,'rb') as ap:
            message.add_attachment( ap.read(),
                                    maintype=mime_type,
                                    subtype=mime_subtype,
                                    filename=attachment_filename)

    return message

def send_email(message):
    mail_server = smtplib.SMTP("localhost")
    mail_server.send_message(message)
    mail_server.quit()


if __name__ == "__main__":
    sender = "automation@example.com"
    receiver = "username@example.com"
    subject = "Upload Completed - Online Fruit Store"
    body = "All fruits are uploaded to our website successfully. A detailed list is attached to this email."
    attachment_path = "/tmp/processed.pdf"

    if generate_attachment(attachment_path):
        message = generate_email(sender, receiver, subject, body, attachment_path)
        if message is not None:
            send_email(message)
        else:
            logging.error("Failed to send email.")
