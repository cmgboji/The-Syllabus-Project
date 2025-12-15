import requests
from bs4 import BeautifulSoup
import io
from pypdf import PdfReader

base_url = 'https://utdirect.utexas.edu'
url = "https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?year=&semester=&department=A+I&course_number=&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

syllabi = []
for link in soup.find_all('a', href=True):
    href = link.get('href')
    if 'download' in href:
        href = base_url + href
        syllabi.append(href)

syllabi = syllabi[1::2]

text = []
for link in syllabi:
    response = requests.get(link)
    with io.BytesIO(response.content) as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text.append(page.extract_text())

print(text)