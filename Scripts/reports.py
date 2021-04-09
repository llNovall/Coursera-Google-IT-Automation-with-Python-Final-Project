#!/usr/bin/env python3
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import logging

logging.basicConfig(level=logging.INFO)

def generate_report(fileName, title, paragraph):
    '''
    This method generates pdf file which contains the title and paragraph.
    Returns True if success otherwise returns False.
    '''

    if fileName != "":
        if title != "":
            if len(paragraph) > 0:
                report = SimpleDocTemplate(fileName)
                styles = getSampleStyleSheet()

                report_items = []
                report_items.append(Paragraph(title, styles['h1']))
                report_items.append(Paragraph(paragraph,styles ['Normal']))

                print(report_items)
                report.build(report_items)
                return True
            else:
                logging.error("Paragraph is missing.")
        else:
            logging.error("Title is missing.")
    else:
        logging.error("File name is missing.")
