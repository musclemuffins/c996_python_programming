from bs4 import BeautifulSoup
import requests, csv, re, urllib.parse, os

WEB_LINK = "http://www.census.gov/programs-surveys/popest.html"
HTML_FILE_PATH = os.path.join(os.getcwd(), 'CurrentEstimates.html')
# use 'os' module for file path for compatibility between linux and windows

# download html file if not found locally
if not os.path.isfile(HTML_FILE_PATH):
    try:
        res = requests.get(WEB_LINK)
        res.raise_for_status()
    except Exception as exc:
            print('There was a problem retrieving the page: %s' % (exc))
    else:
        html_document = open('CurrentEstimates.html', 'wb')
        for chunk in res.iter_content(100_000):
            html_document.write(chunk)
        html_document.close()

# create beautifulsoup object from local html document
try:
    html_soup = BeautifulSoup(open(HTML_FILE_PATH), 'html.parser')
except Exception as exc:
    print('There was a problem createing the BeautifulSoup object: %s' % (exc))

# get all links and add them to a list
list_of_links = []
for link in html_soup.find_all('a'):
    link = link.get('href')
    link = urllib.parse.urljoin(WEB_LINK, link)
    # ^convert relative to absolute URL's
    list_of_links.append(link)

html_regex = re.compile(r'(#.*$)')      # Search for links ending with '#anycharacters'
filtered_links = []
for link in list_of_links:
    match_object = html_regex.search(link)
    if match_object is None:            # If link doesn't end with '#something', then append
        filtered_links.append(link)

filtered_links = set(filtered_links)        # Remove duplicates
filtered_links = sorted(filtered_links)     # Sort values

output_file = open('output.csv', 'w', newline='')
output_writer = csv.writer(output_file)
for link in filtered_links:
    # iterates over list to write each value in list to a new row instead of new column
    output_writer.writerow([link])
output_file.close()