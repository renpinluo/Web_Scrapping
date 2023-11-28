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


def get_login_python(domain):
    """
    Retrieve login code for a given domain from the logins file.

    Parameters:
    domain (str): The domain to retrieve the login code for.

    Returns:
    str: The login code if found, otherwise None.
    """
    with open(os.path.join("test_templates", "logins.json"), "r") as f:
        logins = dict(json.load(f))
        if domain in logins.keys():
            return logins[domain]
    return None

def get_domain(link):
    """
    Extract the domain from a URL.

    Parameters:
    link (str): The URL to extract the domain from.

    Returns:
    str: The extracted domain.
    """
    try:
        extracted = tldextract.extract(link)
        domain = extracted.domain
        return domain
    except Exception as e:
        return 'UNKNOW'
    
def get_path():
    with open(os.path.join("test_templates", "path.json"), "r") as f:
        return dict(json.load(f))

def save_page_html(driver, output_dir):
    """
    Save the HTML source of the current page to a file.

    Parameters:
    driver (webdriver): The Selenium WebDriver.
    output_dir (str): The directory where the HTML file will be saved.
    """
    html = driver.page_source
    time.sleep(2)
    file_path = os.path.join(output_dir, str(uuid.uuid4()) + ".html")
    with open(file_path, "w") as f:
        f.write(html)


def scrape(entry_url, subj, source):
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    
    while True:
        driver = None
        capabilities = DesiredCapabilities.FIREFOX
        print(capabilities)
        try:
            driver = webdriver.Remote(command_executor='http://grid:4444/wd/hub', options=options, desired_capabilities=capabilities)
        except Exception as e:
            print(f"Got an error, waiting 5s: {e}")
            time.sleep(5)
        if driver:
            break

    print("Login handling code goes here")


    driver.set_page_load_timeout(300)
    count = 0
    scraped_list = []
    with open('websites.pkl', 'rb') as file:
        url_list = pickle.load(file)

    # Extract domains from the URLs
    domains = [get_domain(url) for url in url_list]

    for url in entry_url:

        try:
            driver.get(url)
            time.sleep(5)
            
            domain = get_domain(driver.current_url)
            path = urlparse(driver.current_url).path
            if path == '/' or domain not in domains or driver.current_url in scraped_list:
                continue
            
            dic = get_path()

            if domain in dic.keys():
                trigger = True
                for z in dic[domain]:
                    if path.startswith(z):
                        trigger = False
                        break
                if trigger:
                    continue
                
            print(domain)   
            with open(os.path.join("../debug", domain), "w") as f:
                f.write(domain)

            login_code = get_login_python(domain)
            print('login_code: ',login_code)

            if login_code:
                with open(os.path.join("test_templates", "logins", login_code), "r") as f:
                    exec(f.read())

            driver.get(url)
            #driver.refresh()

            def save_page():
                print("Saving page")
                with open(os.path.join("debug", "saved_pages.txt"), "a") as f:
                    if get_domain(driver.current_url) == domain:
                        f.write(str(driver.current_url) + "\n")

            def save_page_html():
                save_page_html(driver, "output_html")

            def save_page_text(html, subj, count, source, url_element):
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

                writeline("Source: "+source+"\n")
                writeline("Article Link: "+url_element+"\n")

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

            # def save_page_text(html, count):

            #     soup = BeautifulSoup(html, 'html.parser')
            #     text=soup.select('p')

            #     if len(text)>0:

            #         f = list()
            #         def writeline(linetext):
            #             f.extend(linetext.split("\n"))

            #         text_metadata = soup.get_text()
            #         for i in ["\n","\t","\r", "  "]:
            #             text_metadata = text_metadata.replace(i, "")
            #         metadata = metadata_prompt(text_metadata)
            #         try:
            #             writeline(metadata+"\n")
            #         except:
            #             writeline(f'Metadata is not available'+"\n")
                
            #         writeline("Source: "+source+"\n")
            #         writeline("Article Link: "+entry_url+"\n")

            #         for t in text:
            #             if len(t)>0:
            #                 # writeline(t.get_text()+"\n")
            #                 # writeline(t.get_text().encode('latin-1', 'replace').decode('latin-1').strip())
            #                 writeline(t.get_text().strip())

            #         writeline("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

            #         def create_pdf(texts, output_file):
            #             doc = SimpleDocTemplate(output_file, pagesize=letter)
            #             styles = getSampleStyleSheet()
            #             flowables = []
            #             for text in texts:
            #                 p = Paragraph(text, styles['Normal'])
            #                 flowables.append(p)
            #                 flowables.append(Spacer(1, 0.1*inch))
            #             doc.build(flowables)
                    
            #         create_pdf(f, f'output_pdfs/{str(subj)}_{str(count)}.pdf')

            save_page()

            print("Starting initial link")

            # elems = driver.find_elements_by_xpath("//a[@href]")
            # print("Links")
            # page_links = [elem.get_attribute("href") for elem in elems]
            
            denied_list=[]

            # for page_link in page_links:
            #     try:
            #         driver.get(page_link)
            #         save_page()
            #         html = driver.page_source
            #         time.sleep(2)
            #         file_path = os.path.join("output_html", str(uuid.uuid4()) + ".html")
            #         with open(file_path, "w") as f:
            #             f.write(html)
            #         save_page_text(page_link, count)
            #         count += 1
            #     except Exception as e:
            #         print(f"Failed to get linked page: {e}")
            #         denied_list.append(page_link)
            

            try:
                html = driver.page_source
                time.sleep(2)
                file_path = os.path.join("output_html", str(subj) + '_'+ str(count) + ".html")
                with open(file_path, "w") as f:
                    f.write(html)
                save_page_text(html, subj, count, source, url)
            except Exception as e:
                print(f"Failed to get linked page: {e}")
                denied_list.append(driver.current_url)

            #save denied url in a pickle file under debug folder
            with open(os.path.join('debug', 'denied_urls.pkl'), 'wb') as f:
                pickle.dump(denied_list, f)

            print("Done with initial link")
            count += 1
            scraped_list.append(driver.current_url)

        except selenium.common.exceptions.WebDriverException as e:
            with open(os.path.join("debug", "timeout_urls.txt"), "a") as f:
                f.write(url + "\n")
            print(f"TimeoutError: {e}")

    try:
        driver.quit()
    except:
        pass



def scrape_content(email_file):
    
    def encode(text):
        '''
        1. encodes a given text into bytes by trying each encoding one by one until it finds one that does not throw a UnicodeEncodeError
        2. decodes the bytes back into a string using the 'ascii' encoding and ignores any errors that occur during this decoding process.
        the asci encoding is needed as input in the quopri library
        '''
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

    
    def remove_attrs(soup, whitelist=tuple()):
        '''
        cleans up the HTML document
        removes all attributes from all tags in a BeautifulSoup object, except for those attributes whose names are listed in the whitelist.
        '''
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
            return
            # raise Exception("No html content in file: "+eml_path)
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
        pdfkit.from_string(message, pdf_path, options={
            'encoding': 'UTF-8',
            'enable-local-file-access': True
        })

    eml_path = os.path.join("emails", email_file)
    pdf_path = os.path.join("output_pdfs", str(email_file) + '_'+ str(0) + '.pdf')
    html_path = os.path.join("output_html", str(email_file) + '_'+ str(0) + ".html")

    # save_email_as_pdf(eml_path, html_path)
    save_email_as_pdf(eml_path, pdf_path, html_path)

