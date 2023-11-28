from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import selenium
import time
from urllib.parse import urlparse
import tldextract
import os
import json
import uuid
import requests
from bs4 import BeautifulSoup
import pickle 

import email
from email import message_from_file
import pdfkit
import quopri
from metadata_prompts import metadata_prompt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def save_page_text(html, subj, count, source, entry_url):
    soup = BeautifulSoup(html, 'html.parser')
    text=soup.select('p')

    if len(text)==0:
        raise Exception("Invalid html or it does not have a <p> element")

    f = list()
    def writeline(linetext):
        f.extend(linetext.split("\n"))

    text_metadata = soup.get_text()
    for i in ["\n","\t","\r", "  "]:
        text_metadata = text_metadata.replace(i, "")
    metadata = metadata_prompt(text_metadata)
    try:
        writeline(metadata+"\n")
    except:
        writeline(f'Metadata is not available'+"\n")

    writeline(F"Source: {source}\n")
    writeline(F"Article Link: {entry_url}\n")

    for t in text:
        if len(t)>0:
            writeline(t.get_text().strip())

    writeline("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    def create_pdf(texts, output_file):
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        styles = getSampleStyleSheet()
        flowables = []
        for text in texts:
            p = Paragraph(text, styles['Normal'])
            flowables.append(p)
            flowables.append(Spacer(1, 0.1*inch))
        doc.build(flowables)
    
    create_pdf(f, f'output_pdfs/{str(subj)}_{str(count)}.pdf')

"""
path = "C:\\Users\\KARAMA11\\src\\GenAI\\web_scraping_deloitte\\docker\\Pfizer_Web_Scraping 11.22_kk\\output_html\\0editors_go.fiercebiotech.com202311021620176520.eml_6.html"
with open(path, encoding="utf-8") as file:
    html = file.read()
save_page_text(html, "subj", "count", "source", "entry_url")
"""