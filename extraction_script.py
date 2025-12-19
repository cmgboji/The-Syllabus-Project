import requests
from bs4 import BeautifulSoup
import io
import pdfplumber
import logging
# Reduce noise from pdfminer
logging.getLogger("pdfminer").setLevel(logging.ERROR)
import re
from nltk.corpus import stopwords
import pandas as pd
from concurrent.futures import ThreadPoolExecutor


def fetch_listing(dept_list, year, sem, headers, session):
    base_list_url = "https://utdirect.utexas.edu/apps/student/coursedocs/nlogon/"
    url_list = []

    for dept in dept_list:
        params = {
            "year": year,
            "semester": sem,
            "department": dept,
            "course_number": "",
            "course_title": "",
            "unique": "",
            "instructor_first": "",
            "instructor_last": "",
            "course_type": "In Residence",
            "search": "Search",
        }
        response = session.get(base_list_url, headers=headers, params=params, timeout=30)
        response.raise_for_status()
        url_list.append(response.url)

    return url_list


def extract_data(url_list, session, headers):
    base_url = 'https://utdirect.utexas.edu'

    raw_data = []
    raw_syllabi = []

    for url in url_list:
        response = session.get(url, headers=headers, timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Constructing data table from extracted HTML
        header_row = soup.find('tr', class_='tbh header')
        if header_row:
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

def extract_syllabi(url, session, headers):
    response = session.get(url, headers=headers, timeout=30)
    with pdfplumber.open(io.BytesIO(response.content)) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

    
def clean_text(text, stop_words, clean_re):
    # Lowercasing and removing punctuation/numbers
    text = clean_re.sub('', text.lower())
    # Tokenization and stopword removal
    tokens = [word for word in text.split() if word not in stop_words]
    cleaned_text = ' '.join(tokens)
    return cleaned_text

def fetch_and_clean_syllabus(url, session, headers, stop_words, clean_re):
    text = extract_syllabi(url, session, headers)
    return clean_text(text, stop_words, clean_re)

def syllabi_dataframe(raw_data, text):
    data = pd.DataFrame(raw_data, columns = ['Semester', 'Department', 'Course Number', 
                                            'Title', 'Unique', 'Instructor', 'Syllabus', 
                                            'Survey'])
    data['Syllabus'] = text
    data['Instructor'] = data['Instructor'].str.replace(' CV (opens new window)', '')
    data['Course Code'] = data['Department'] + ' ' + data['Course Number']
    data.drop(columns=['Unique', 'Survey'], inplace=True)
    return data

def main(dept_list, year, sem):
    HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/pdf,application/xhtml+xml",
    }

    session = requests.Session()

    adapter = requests.adapters.HTTPAdapter(
        max_retries=3,
        pool_connections=20,
        pool_maxsize=20
    )
    session.mount("https://", adapter)
    clean_re = re.compile(r'[^a-z\s]')
    stop_words = set(stopwords.words('english'))

    url_list = fetch_listing(dept_list, year, sem, HEADERS, session)
    raw_data, raw_syllabi = extract_data(url_list, session, HEADERS)

    with ThreadPoolExecutor(max_workers=8) as executor:
        full_text = list(
            executor.map(
                lambda url: fetch_and_clean_syllabus(url, session, HEADERS, stop_words, clean_re),
                raw_syllabi
            )
        )
    data = syllabi_dataframe(raw_data, full_text)
    return data


if __name__ == "__main__":
    data = main(dept_list, year, sem)
