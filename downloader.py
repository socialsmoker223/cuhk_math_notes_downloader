import re
import os
import sys
import requests
from bs4 import BeautifulSoup

def download_note(note_element, out_dir):
    # Get the title of the note from the HTML element
    note_title = note_element.text.strip().replace('/', '-')
    download_url = note_element['href']
    file_name = '{}/{}.pdf'.format(out_dir,note_title)

    # Download the note
    r = requests.get(download_url, allow_redirects=True)
    with open(file_name, 'wb') as f:
        f.write(r.content)

    # Print to the console to keep note of how the scraping is coming along.
    print('Downloaded: {}'.format(note_title, download_url))
    # print(download_url)
    pass

math_url = str(sys.argv[1])
html_text = requests.get(math_url).text
soup = BeautifulSoup(html_text, 'html.parser')
course = re.findall(r'(\d+)/(\w+)', math_url)[0]
year, name = course[0], course[1].upper()
out_dir = '{}({})'.format(name,year)
if not os.path.exists(out_dir):
    os.mkdir(out_dir)
if __name__ == '__main__':

    attrs = {
        'href': re.compile(r'\.pdf$')
    }

    notes = soup.find_all('a', attrs=attrs, string=re.compile(r'^((?!\().)*$'))

    for note in notes:
        download_note(note,out_dir)
    print('{} files downloaded'.format(len(notes)))
