import os
import extract_msg
from email.policy import default
from email.parser import BytesParser
from email import policy
from urllib.parse import urlparse
from scrape import scrape
from scrape import get_domain, get_path
import re
#import asynciop
import pickle
import uuid
import requests
from bs4 import BeautifulSoup
import email
import pdfkit

import fitz
import email
from email import policy
from email.parser import BytesParser
from email import message_from_file
import quopri, codecs

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


'''
1. encodes a given text into bytes by trying each encoding one by one until it finds one that does not throw a UnicodeEncodeError
2. decodes the bytes back into a string using the 'ascii' encoding and ignores any errors that occur during this decoding process.
   the asci encoding is needed as input in the quopri library
'''
def encode(text):
    encodings = ['utf-8', 'latin-1', 'ascii']
    unicode_bytes = None
    for encoding in encodings:
        try:
            unicode_bytes = text.encode(encoding)
            break
        except UnicodeEncodeError:
            continue
    if unicode_bytes is not None:
        print("Unicode encoding bytes:", unicode_bytes)
    else:
        print("Unable to determine encoding")
    return unicode_bytes.decode("ascii", 'ignore')

'''
cleans up the HTML document
removes all attributes from all tags in a BeautifulSoup object, except for those attributes whose names are listed in the whitelist.
'''
def remove_attrs(soup, whitelist=tuple()):
    for tag in soup.findAll(True):
        for attr in [attr for attr in tag.attrs if attr not in whitelist]:
            del tag[attr]
    return soup

def save_email_as_pdf(eml_path, pdf_path, html_path):
# def save_email_as_pdf(eml_path, html_path):
    with open(eml_path) as file:
        #message = file.read()
        message = message_from_file(file)
    message = str(message)
    # extract the html part
    message_start = message.find("<!DOCTYPE html")
    if message_start == -1:
        raise Exception("No html content in file: "+eml_path)
    message = message[message_start:]
    # remove =\n which is how the html is artificially split into lines
    message = message.replace("=\n", "")
    # fix encoding
    encoded = encode(message)
    message = quopri.decodestring(encoded)
    message = message.decode('utf-8', 'ignore')
    # remove html attributes
    soup = BeautifulSoup(message, 'html.parser')
    soup =  remove_attrs(soup)
    message = str(soup)
    # save the message as html
    with open(html_path, "w", encoding="utf-8") as file:
        file.write(message)
    # save the message as pdf
    # HTML(string=message).write_pdf(pdf_path)
    pdfkit.from_file(html_path, pdf_path)

    # # save the message as pdf
    # text = soup #.select('span')   
    # if len(text)>0:
    #     f = list()
    #     def writeline(linetext):
    #         f.extend(linetext.split("\n"))
    #     for t in text:
    #         if len(t)>0:
    #             writeline(t.get_text().strip())        
    #     def create_pdf(texts, output_file):
    #         doc = SimpleDocTemplate(output_file, pagesize=letter)
    #         styles = getSampleStyleSheet()
    #         flowables = []
    #         for text in texts:
    #             p = Paragraph(text, styles['Normal'])
    #             flowables.append(p)
    #             flowables.append(Spacer(1, 0.1*inch))
    #         doc.build(flowables)            
    #     create_pdf(f, pdf_path)
    # return

email_files = ['0media.relations_novartis.com202310311705167386.eml']
# email_files = ['0media.relations_novartis.com202310311705167386.eml',
#               '0media.relations_novartis.com202310300300158747.eml' ,
#               'donotreply_globenewswire.com2023111108503326300.eml',
#               'donotreply_globenewswire.com2023111307203820372.eml',
#               'EXTERNAL Communiqué de presse  Sanofi entame un nouveau chapitre de sa stratégie Play to Win.msg',
#               'EXTERNAL Communiqué de presse  Un troisième trimestre solide marqué par la performance de la Médecine de Spécialités et le fort démarrage des lancements de Beyfortus et ALTUVIIIO             .msg'
#               ]

# email_files = ['0global.news_roche.com202310301605141499.eml',
#               '0global.news_roche.com202310310850155292.eml' ,
#               ]

for email_file in email_files:
    eml_path = os.path.join("emails", email_file)
    pdf_path = os.path.join("output_pdfs", str(email_file) + '_'+ str(0) + '.pdf')
    html_path = os.path.join("output_html", str(email_file) + '_'+ str(0) + ".html")
    # save_email_as_pdf(eml_path, html_path)
    save_email_as_pdf(eml_path, pdf_path, html_path)



################################################################################################################ 1st attempt no html content
# def convert_eml_to_pdf(eml_file, pdf_file):
#     # Read the .eml file
#     with open(eml_file, 'r') as file:
#         eml_content = file.read()
#     # Parse the .eml content
#     msg = email.message_from_string(eml_content)
#     # Extract the HTML content from the .eml file
#     html_content = None
#     for part in msg.walk():
#         if part.get_content_type() == "text/html":
#             html_content = part.get_payload(decode=True).decode()
#             break
#     if html_content:
#         # Convert HTML to PDF
#         pdfkit.from_string(html_content, pdf_file)
#         print(f"Converted {eml_file} to pdf successfully.")
#     else:
#         print("No HTML content found in the .eml file.")

# email_file = '0media.relations_novartis.com202310311705167386.eml'              
# eml_file_path = os.path.join("emails", email_file)
# pdf_file = os.path.join("output_pdfs", str(email_file) + '_'+ str(0) + '.pdf')

# convert_eml_to_pdf(eml_file_path, pdf_file)

################################################################################################################ original working
# # email_file = '0media.relations_novartis.com202310300300158747.eml'  
# email_file = '0media.relations_novartis.com202310311705167386.eml' 

# eml_file_path = os.path.join("emails", email_file)
# with open(eml_file_path, 'rb') as fp:
#     msg = BytesParser(policy=default).parse(fp)
# text = msg.get_body(preferencelist=('plain')).get_content()
# text = text.replace('=\n','').replace('=3D','=')

# file_path = os.path.join("output_html", str(email_file) + '_'+ str(0) + ".html")
# with open(file_path, "w", encoding="utf-8") as f:
#         f.write(text)
# soup = BeautifulSoup(text, 'html.parser')
# text=soup.select('span')
# if len(text)>0:
#         f = open(os.path.join("output_pdfs", str(email_file) + '_'+ str(0) + '.txt'), 'w', encoding="utf-8")
#         for t in text:
#             if len(t)>0:
#                 f.writelines(t.get_text()+"\n")
#         f.close()