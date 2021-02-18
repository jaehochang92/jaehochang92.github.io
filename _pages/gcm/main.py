import pandas as pd
import numpy as np
import os, pickle, datetime, time, urllib3, re
from urllib.parse import quote
from bs4 import BeautifulSoup, NavigableString, Tag


class StringToken:

    def __init__(self, string):
        self.string = string
        self.token = string.lower()

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def __eq__(self, other):
        return self.token == other

    def __hash__(self):
        return hash(self.token)

    def get_string(self):
        return self.string

    def get_token(self):
        return self.token


columnCorrespondence = [
    ('tcol1', 'institution'),
    ('tcol2', 'program'),
    ('tcol3', 'decision'),
    ('tcol4', 'applicant_type'),
    ('tcol5', 'date_added'),
    ('tcol6', 'notes')
]

def extract_columns(tr):
    ret = dict()
    for colStyle, dest in columnCorrespondence:
        td = tr.find('td', {'class' : colStyle})
        text = ''
        for item in td.children:
            if isinstance(item, NavigableString):
                text += item
            elif isinstance(item, Tag):
                if item.name != 'a':
                    # discard extra information
                    text += item.text

        ret[dest] = text.strip()
    return ret


def process_raw_columns(rawColumns):
    ret = dict()

    # remove all parenthesis in the institution names
    rawName = rawColumns['institution']
    rawName = re.sub(r'\(.*?\)', '' ,rawName)
    # remove all punctutaion
    rawName = re.sub(r'[.,\/#!$%\^&\*;:{}=\-_`~()–]', ' ', rawName)
    rawName = re.sub(r'\s\s+', ' ', rawName)

    ret['institution'] =  StringToken(rawName.strip())

    # determine degree level
    rawProgram = re.sub(',', ' ', rawColumns['program'].lower())
    rawProgramWords = rawProgram.strip(' ')

    if 'masters' in rawProgramWords:
        ret['degree'] = StringToken('Masters')
    elif 'phd' in rawProgramWords:
        ret['degree'] = StringToken('PhD')
    else:
        ret['degree'] = StringToken('NaN')

    # determine decision type
    matchResult = re.match('(.*?) via (.*?) on (.*)', rawColumns['decision'])
    if matchResult is None:
        raise RuntimeError('unmatchable decision string {}'.format(rawColumns['decision']))

    # determine decision date
    ret['decision'] = StringToken(matchResult.group(1))
    ret['channel'] = StringToken(matchResult.group(2))
    #print(matchResult.group(3))
    ret['date'] = np.datetime64(datetime.datetime.strptime(matchResult.group(3), '%d %b %Y'))
    ret['note'] = rawColumns['notes']

    return ret


def parse_response(response):
    soup = BeautifulSoup(response, 'html.parser')

    # locate the submissons
    submissonSection = soup.find('section', {'class' : 'submissions'})

    allItems = []

    # locate all cells
    for tr in submissonSection.find_all('tr'):
        classIds = tr.attrs.get('class', [])
        if 'row0' in classIds or 'row1' in classIds:
            # extract raw information
            rawColumns = extract_columns(tr)
            # process raw information
            allItems.append(process_raw_columns(rawColumns))

    return allItems



# HTML header
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


def crawl_data(subject, startDate):
    print('crawling data from gradcafe...')
    _subject = quote(subject)
    _startDate = np.datetime64(startDate)

    manager = urllib3.PoolManager()

    # start crawling data
    page = 1
    allResponse = []
    exitSignal = False

    while not exitSignal:
        print(f'fetching page {page}')

        # send a GET request
        r = manager.request('GET', 'https://www.thegradcafe.com/survey/index.php',
                        fields={'q' : _subject, 't' : 'a', 'o' : '', 'p' : repr(page)})
        if r.status != 200:
            raise RuntimeError(f'unable to fetch page {page} (HTTP response {r.status})')

        response = parse_response(r.data)

        # sort the results by date
        response.sort(key = lambda x : x['date'], reverse=True)

        if response[-1]['date'] < _startDate:
            exitSignal = True
            # filter out unwanted results
            validResponse = list(filter(lambda x : x['date'] >= _startDate, response))
            allResponse.extend(validResponse)
            continue

        allResponse.extend(response)

        # add a bit of interval between requests
        time.sleep(0.05)
        page += 1

    print('fetched {} records from gradcafe'.format(len(allResponse)))

    # save all response to file
    pd.to_pickle(allResponse, '_pages/gradcafe-monitor/all_response.pickle')

# from markdown_generator import *

# markdown = r'''
# **Update time: {}**

# Source code: <https://github.com/xziyue/gradcafe-monitor>

# Acronyms: A-accepted, R-rejected, I-inverviewed, W-wait listed, O-other

# <!--more-->

# '''.format(
#     datetime.now().isoformat()
# )


# degrees = ['PhD', 'Masters']

# for degree in degrees:
#     degreeToken = degree.lower()
#     markdown += f'## {degree}\n\n'
#     markdown += '### Institution Activities\n\n'
#     markdown += generate_institution_overview(degreeToken) + '\n\n'
#     markdown += '### Chronological Order\n\n'
#     markdown += generate_decision_overview(degreeToken) + '\n\n'

# with open('_pages/gradcafe-monitor/stat.md', 'w') as outfile:
#     outfile.write(markdown)

def main():
    today = datetime.datetime.now()
    startDate = today - datetime.timedelta(weeks=.5)
    subject = 'duke+biostat*'
    crawl_data(subject, startDate.strftime('%Y-%m-%d'))

    gc_pkl = pd.read_pickle('_pages/gradcafe-monitor/all_response.pickle')
    df = pd.DataFrame(gc_pkl)
    md = df.to_markdown()

    with open('_pages/gradcafe-monitor/disp.md', 'w') as f:
        f.writelines(md)
    return md

main()

if __name__ == '__main__':
    main()
