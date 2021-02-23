from pprint import pprint
from urllib.request import urlopen
import re
import argparse
import pandas

parser = argparse.ArgumentParser(description='Type your query.')
parser.add_argument('-i', '--institution')
parser.add_argument('-p', '--program')
parser.add_argument('-d', '--degree', choices=['phd', 'mas'])
args = parser.parse_args()


if __name__ == '__main__':
    # parsing query
    query = ''
    if args.institution:
        query += '+' if query else ''
        query += args.institution
    if args.program:
        query += '+' if query else ''
        query += args.program
    degree_dict = {'phd': 'PhD', 'mas': 'Master'}
    
    # parsing url
    with urlopen(f'https://www.thegradcafe.com/survey/index.php?q={query}&t=a&o=&pp=250') as response:
        html = response.read().decode()
    submissions = re.compile(
        '<table class="submission-table">(.*?)</table>', re.DOTALL).findall(html)[0]
    submissions = re.sub('(\\n|\\t)', '', submissions)
    inst = re.findall('instcol tcol1\">(.*?)</td>', submissions)
    prgm = re.findall('<td class="tcol2">(.*?)</td>', submissions)
    stus = re.findall('<td class="tcol3 (.*?)>(.*?)</td>', submissions)
    stus = [re.findall(
        '(Accepted|Rejected|Other|Interview|Wait listed).+via (.+) on (.+[0-9]{4})', tuple[1])[0] for tuple in stus]
    dgre = re.findall('<td class="tcol4">(.*?)</td>', submissions)
    sdte = re.findall('<td class="datecol tcol5">(.*?)</td>', submissions)
    cmnt = re.findall('<li>(.*?)</li>', submissions)

    if len(inst) == len(prgm) == len(stus) == len(dgre) == len(sdte) == len(cmnt):
        col_names = ['학교', '과정', '결과', 'via', 'on', '출신', '게시날짜', '코멘트']
        rows = [(j, prgm[i], *stus[i], dgre[i], sdte[i], cmnt[i])
                for i, j in enumerate(inst)]
        df = pandas.DataFrame(rows, columns=col_names)
        
        # filtering
        if args.degree:
            dgr = degree_dict[args.degree]
            df = df[[dgr in i for i in df.과정]]
        
        fname = f'{query}-{dgr}' + '.html'
        with open(fname, 'a') as html_file:
            html_file.writelines(f'''---
            permalink: /gcm/{query}
            title: "Gradcafe monitor"
            author_profile: false
            ---''' + df.to_html())