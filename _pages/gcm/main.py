from pprint import pprint
from urllib.request import urlopen
from datetime import datetime, tzinfo
import pytz
import re
import argparse
import pandas


parser = argparse.ArgumentParser(description='Type your query.')
parser.add_argument('degree', choices=['phd', 'mas'])
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
    submissions = re.compile(
        '<table class="submission-table">(.*?)</table>', re.DOTALL).findall(html)[0]
    # submissions = re.sub('(\\n|\\t)', '', submissions)
    inst = re.findall('instcol tcol1\">(.*?)</td>', submissions)
    prgm = re.findall('<td class="tcol2">(.*?)</td>', submissions)
    stus = re.findall('<td class="tcol3 (.*?)>(.*?)</td>', submissions)
    stus = [re.findall(
        '(Accepted|Rejected|Other|Interview|Wait listed).+via (.+) on (.+[0-9]{4})', tuple[1])[0] for tuple in stus]
    dgre = re.findall('<td class="tcol4">(.*?)</td>', submissions)
    sdte = re.findall('<td class="datecol tcol5">(.*?)</td>', submissions)
    cmnt = re.findall('<li>(.*?)</li>', submissions)

    if len(inst) == len(prgm) == len(stus) == len(dgre) == len(sdte) == len(cmnt):
        col_names = ['inst', 'prgrm', 'res', 'via', 'on', 's', 'date', 'cmmnts']
        rows = [(j, prgm[i], *stus[i], dgre[i], sdte[i], cmnt[i])
                for i, j in enumerate(inst)]
        df = pandas.DataFrame(rows, columns=col_names)

        # filtering
        if args.degree:
            dgr = degree_dict[args.degree]
            query += f'+{dgr}'
            df = df[[dgr in i for i in df.prgrm]]
            if '*' in dgr:
                df = df.drop(columns='prgrm')

        with open(query + '.html', 'w') as html_file:
            tz = pytz.timezone('US/Eastern')
            time_stamp = datetime.now(tz).strftime("%Y-%m-%d(%a) %I:%M %p")
            html_file.writelines('---\n'
                                 'layout: archive\n'
                                 f'permalink: /pa/{query}\n'
                                 f'title: "Gradcafe monitor: {query}"\nauthor_profile: true\n'
                                 '---\n'
                                 f'updated in {tz} time: {time_stamp}\n<br>\n<br>\n' +
                                 df.to_html(index=False).replace('<table border="1" class="dataframe">', '<table>'))
