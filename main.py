import os
import extract_msg
from email.policy import default
from email.parser import BytesParser
from email import policy
from urllib.parse import urlparse
from scrape import scrape
from scrape import get_domain, get_path, scrape_content
import re
#import asynciop
import pickle
import uuid
import requests
from bs4 import BeautifulSoup
import email


# Load the pickle file
with open('websites.pkl', 'rb') as file:
    url_list = pickle.load(file)

# Extract domains from the URLs
domains = [get_domain(url) for url in url_list]

    
def get_redirect_url(link):
    try:
        # Send an HTTP GET request and allow it to follow redirects, while disabling SSL certificate verification
        response = requests.get(link, allow_redirects=True, verify=False, timeout=5)
        # Extract the final URL after following any redirects
        link = response.url
        return link
    except Exception as e:
        # Handle SSL certificate verification errors and log the error
        with open("error_links.txt", "a") as error_file:
            error_file.write(f"Error URL: {link}\n")
        print(f"SSL certificate verification error for {link}: {e}")
        return None

async def scrape_all(links):
    async def scrape(link):
        # Your scraping logic here
        print(f"Scraping {link}")
    # Create a list of tasks to scrape each link asynchronously
    tasks = [scrape(link) for link in links]
    # Run the tasks concurrently
    await asyncio.gather(*tasks)


def extract_urls(text):
    #url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    url_pattern = r'http[s]?://\S+\$'
    urls =  re.findall(url_pattern, text)
    # Noticed some of URLS had at the end so remove '>' character from the end of each URL
    cleaned_urls = [url.rstrip('>') for url in urls]
    return cleaned_urls


def extract_scrape_EML(email_file):
    """
    Generate tests from an EML file.

    Args:
        email_file (str): The email file to generate tests from.
    """
    # extract the sender's email address
    domain_extensions = ['.gov', '.com', '.edu', '.org']
    for domain_extension in domain_extensions:
        if domain_extension in email_file:
            email = f'{email_file[:email_file.index(domain_extension)].replace("_","@")}{domain_extension}'
            msg_sender = re.sub(r'^\d+', '', email)

    if 'novartis' in email_file or 'globenewswire' in email_file or 'roche' in email_file:
        scrape_content(email_file)
    else:
        eml_file_path = os.path.join("emails", email_file)
        with open(eml_file_path, 'rb') as fp:
            msg = BytesParser(policy=default).parse(fp)
        text = msg.get_body(preferencelist=('plain')).get_content()
        text = text.replace('=\n','').replace('=3D','=')
                  
        carrot_links = extract_urls(text)
        links = [get_redirect_url(x) for x in carrot_links if x.startswith("http")]
        link_domains = [get_domain(link) for link in links]
        print(links)
        print(link_domains)
        print(len(links))

        clean_links =[]
        for i in range(len(link_domains)):
            if link_domains[i] in domains:
                clean_links.append(links[i])

        # print(len(clean_links))
        # print(len(set(clean_links)))
        clean_links = set(clean_links)

        scrape(clean_links, email_file, msg_sender)
  

  

# Read email files
email_files = [f for f in os.listdir("emails") if f.endswith(".eml")]
for email in email_files:
    print(email)
    # Generate tests from an email
    extract_scrape_EML(email)