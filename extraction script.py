import requests
from bs4 import BeautifulSoup
import io
import pdfplumber
import re
from nltk.corpus import stopwords
import pandas as pd

def extract_data(url_list, session):
    base_url = 'https://utdirect.utexas.edu'

    raw_data = []
    raw_syllabi = []

    for url in url_list:
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Constructing data table from extracted HTML
        header_row = soup.find('tr', class_='tbh header')
        table = header_row.find_parent('table')
        for row in table.find_all('tr')[1:]:
            cols = row.find_all('td')
            link = cols[6].find('a', href=True) # Syllabus link
            if link:
                href = link['href']
                if 'download' in href:
                    href = base_url + href # full URL of syllabus PDF
                    raw_syllabi.append(href)
            cols = [ele.text.strip() for ele in cols]
            raw_data.append(cols)

    return raw_data, raw_syllabi

def extract_syllabi(url, session):
    response = session.get(url)
    with pdfplumber.open(io.BytesIO(response.content)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

    
def clean_text(text):
    stop_words = set(stopwords.words('english'))
    # Lowercasing and removing punctuation/numbers
    text = re.sub(r'[^a-z\s]', '', text.lower())
    # Tokenization and stopword removal
    tokens = [word for word in text.split() if word not in stop_words]
    cleaned_text = ' '.join(tokens)
    return cleaned_text

def syllabi_dataframe(raw_data, text):
    data = pd.DataFrame(raw_data, columns = ['Semester', 'Department', 'Course Number', 
                                            'Title', 'Unique', 'Instructor', 'Syllabus', 
                                            'Survey'])
    data['Syllabus'] = text
    data['Instructor'] = data['Instructor'].str.replace(' CV (opens new window)', '')
    data['Course Code'] = data['Department'] + ' ' + data['Course Number']
    data.drop(columns=['Unique', 'Survey'], inplace=True)
    return data

def main(url_list):
    session = requests.Session()
    raw_data, raw_syllabi = extract_data(url_list, session)
    full_text = []
    for syllabus_url in raw_syllabi:
        syllabus_text = extract_syllabi(syllabus_url, session)
        cleaned_text = clean_text(syllabus_text)
        full_text.append(cleaned_text)
    data = syllabi_dataframe(raw_data, full_text)
    return data


if __name__ == "__main__":
    url_list = ['https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?year=&semester=&department=A+I&course_number=&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search', 
                'https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/?year=&semester=&department=AED&course_number=&course_title=&unique=&instructor_first=&instructor_last=&course_type=In+Residence&search=Search']
    data = main(url_list)
    print(data)