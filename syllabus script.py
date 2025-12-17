import requests
from bs4 import BeautifulSoup
import io
import logging
logging.getLogger("pypdf").setLevel(logging.ERROR) # silencing pypdf warnings
from pypdf import PdfReader
import re
import nltk
from nltk.corpus import stopwords
import pandas as pd

raw_data = []
text = []
stop_words = set(stopwords.words('english'))

base_url = 'https://utdirect.utexas.edu'
url_list = ['https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?year=&semester=&department=A+I&course_number=&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search',
            'https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?year=&semester=&department=AED&course_number=&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search']
#url = "https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?year=&semester=&department=A+I&course_number=&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search"

for url in url_list:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Constructing data table from extracted HTML
    header_row = soup.find('tr', class_='tbh header')
    table = header_row.find_parent('table')
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        raw_data.append(cols)

    syllabi = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if 'download' in href:
            href = base_url + href # full URL of syllabus PDF
            syllabi.append(href)

    syllabi = syllabi[1::2] # filtering for syllabi and removing cover letters

    for link in syllabi:
        response = requests.get(link)
        with io.BytesIO(response.content) as f:
            reader = PdfReader(f)
            full_text = ""
            for page in reader.pages:
                page_text = page.extract_text().strip()
                full_text += page_text + "\n"
            text.append(full_text)
    
def clean_text(text):
    text = re.sub(r'[^a-z\s]', '', text.lower())
    tokens = [word for word in text.split() if word not in stop_words]
    cleaned_text = ' '.join(tokens)
    return cleaned_text

text = [clean_text(t) for t in text]

data = pd.DataFrame(raw_data, columns = ['Semester', 'Department', 'Course Number', 
                                         'Title', 'Unique', 'Instructor', 'Syllabus', 
                                         'Survey'])
data['Syllabus'] = text
data['Course Code'] = data['Department'] + ' ' + data['Course Number']
data.drop(columns=['Unique', 'Survey'], inplace=True)
print(data)