import requests
from bs4 import BeautifulSoup
import io
from pypdf import PdfReader
import pandas as pd

raw_data = []

base_url = 'https://utdirect.utexas.edu'
url_list = ['https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?year=&semester=&department=A+I&course_number=&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search',
            'https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?year=&semester=&department=AED&course_number=&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search']
#url = "https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?year=&semester=&department=A+I&course_number=&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search"

for url in url_list:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    header_row = soup.find('tr', class_='tbh header')
    table = header_row.find_parent('table')
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        raw_data.append(cols)
    

data = {'Semester': [], 'Department': [], 'Course Number': [], 'Title': [], 
        'Unique': [], 'Instructor': [], 'Syllabus': [], 'Survey': []}

data['Semester'] = [row[0] for row in raw_data]
data['Department'] = [row[1] for row in raw_data]
data['Course Number'] = [row[2] for row in raw_data]
data['Title'] = [row[3] for row in raw_data]
data['Unique'] = [row[4] for row in raw_data]
data['Instructor'] = [row[5] for row in raw_data]
data['Syllabus'] = [row[6] for row in raw_data]
data['Survey'] = [row[7] for row in raw_data]

text = []

for url in url_list:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    syllabi = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if 'download' in href:
            href = base_url + href
            syllabi.append(href)

    syllabi = syllabi[1::2]

    for link in syllabi:
        response = requests.get(link)
        with io.BytesIO(response.content) as f:
            reader = PdfReader(f)
            full_text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                full_text += page_text + "\n"
            text.append(full_text)


data['Syllabus'] = text
df = pd.DataFrame(data)
print(df)