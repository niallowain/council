#PDF Processinig
import PyPDF2

# Get pdf files or url
import requests

# BeautifulSoup for processing HTML
from bs4 import BeautifulSoup

# for input and output operations
import io

# Attempt to read without download
from urllib.request import urlopen

Years = ['2014','2015','2016','2017','2018','2019','2020','2021']

#created an empty list for putting the pdfs
list_of_pdf = set()

for year in Years:

    # website to scrape
    url = "https://www.corkcity.ie/en/council-services/councillors-and-democracy/meetings-of-the-city-council/full-council-meetings/full-council-meetings-minutes/" + str(year) + ".html"

    # get the url from requests get method
    read = requests.get(url)

    # full html content
    html_content = read.content

    # Parse the html content
    soup = BeautifulSoup(html_content, "html.parser")

    #Get the files in tag form
    files_raw = soup.find_all(class_ = "file-name")

    for file in files_raw:

        p = file.find_all('a')

        # iterate through p for getting all the href links
        for link in p:

            # converting the extention from .html to .pdf
            pdf_link = "https://corkcity.ie" + (link.get('href')[:-4]) + ".pdf"

            # added all the pdf links to set
            list_of_pdf.add(pdf_link)


# Prepare empty list to store pdf text as elements
pages_text = list()
for pdf in list_of_pdf:

    read = requests.get(pdf, allow_redirects=True)

    open('minutes.pdf','wb').write(read.content)
    
    pdfFileObj = open('minutes.pdf', 'rb')

    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pages = pdfReader.numPages
    
    for i in range(pages):
        pageObj = pdfReader.getPage(i)
        pages_text.append(pageObj.extractText())
    
    # remove content from pdf
    open('minutes.pdf','wb').flush
