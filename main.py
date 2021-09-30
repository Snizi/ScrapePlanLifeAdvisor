from bs4 import BeautifulSoup
import requests
import pdfplumber
from os import mkdir

def parse_pdf(pdf_file):
    with pdfplumber.open(pdf_file) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()
        text = text.split('\n')
        text = [text[x].strip(' ') for x in range(len(text))]
        text = [text[x] for x in range(len(text)) if text[x] != '']
        
    a = pdf_file.split('.')[1]
    name = a.split('/')[2]

    with open('./results/'+name + '.txt', 'w') as f:
        f.write(text[0] + '\n')          
        f.write(text[1] + '\n')
        f.write(text[2] + '\n')
        f.write(text[3] + '\n')
        f.write(text[4] + '\n')          


URL = 'https://planlifeadvisors.org/our_sales_team'

html = requests.get(URL).text
content = BeautifulSoup(html, 'html.parser')


# get all the urls
all_urls = content.find_all('a')
pdf_urls = set()


# remove duplicates and add only the PDF links to pdf_urls
for url in all_urls:
    try:
        if 'pdf' in url['href']:
            pdf_urls.add(url['href'])
    except:
        pass

try:
    mkdir('./results/')
    mkdir('./tmp/')
    
except:
    pass


for pdf in pdf_urls:
    pdf_content = requests.get(pdf).content
    if 'bios' in pdf:
        file_name = pdf.split('/')[8]
        with open('./tmp/'+file_name, 'wb') as f:
            f.write(pdf_content)
        parse_pdf('./tmp/'+file_name)
    else:
        file_name = pdf.split('/')[7]
        with open('./tmp/'+file_name, 'wb') as f:
            f.write(pdf_content)
        parse_pdf('./tmp/'+file_name)