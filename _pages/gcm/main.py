from pprint import pprint
from urllib.request import urlopen
from datetime import datetime, tzinfo
import pytz
import re
import argparse
import pandas


parser = argparse.ArgumentParser(description='Type your query.')
parser.add_argument('-i', '--institution')
parser.add_argument('-p', '--program')
args = parser.parse_args()

if __name__ == '__main__':
    # parsing query
    query = ''
    if args.institution:
        query += ('+' if query else '') + args.institution
    if args.program:
        query += ('+' if query else '') + args.program
    degree_dict = {'phd': 'PhD'}

    # parsing url
    with urlopen(f'https://www.thegradcafe.com/survey/index.php?q={query}&t=a&o=&pp=100') as response:
        html = response.read().decode()
    header = '<table class="submission-table">' + re.compile(
        '<table class="submission-table">(.*?)</thead>', re.DOTALL).findall(html)[0] + '</thead>'
    submissions = re.compile(
        '</thead>(.*?)</table>', re.DOTALL).findall(html)[0]

    # selecting only phds
    submissions_phd = ''
    for line in submissions.split('\n'):
        if re.search('<td class="tcol2">.+PhD.+\((F[0-9]{2})\)</td>', line):
            submissions_phd += line + '\n'

    with open(query + '.html', 'w') as html_file:
        tz = pytz.timezone('US/Eastern')
        time_stamp = datetime.now(tz).strftime("%Y-%m-%d(%a) %I:%M %p")
        html_file.writelines('---\n'
                             'layout: archive\n'
                             f'permalink: /pa/{query}\n'
                             f'title: "Gradcafe monitor: {query}"\nauthor_profile: true\n'
                             '---\n'
                             f'updated in {tz} time: {time_stamp}\n<br>\n<br>\n' +
                             header + submissions_phd + '</table>'
                             )
