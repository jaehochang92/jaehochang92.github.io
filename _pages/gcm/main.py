from pprint import pprint
from urllib.request import urlopen
import re
import pandas


with urlopen('https://www.thegradcafe.com/survey/index.php?'
             'q=duke+biostat*&t=a&o=&pp=50') as response:
    html = response.read().decode()
submissions = re.compile('<table class="submission-table">(.*?)</table>', re.DOTALL).findall(html)[0]
submissions = re.sub('(\\n|\\t)', '', submissions)
inst = re.findall('instcol tcol1\">(.*?)</td>', submissions)
prgm = re.findall('<td class="tcol2">(.*?)</td>', submissions)
stus = re.findall('<td class="tcol3 (.*?)>(.*?)</td>', submissions)
dgre = re.findall('<td class="tcol4">(.*?)</td>', submissions)
sdte = re.findall('<td class="datecol tcol5">(.*?)</td>', submissions)
cmnt = re.findall('<li>(.*?)</li>', submissions)
if len(inst) == len(prgm) == len(stus) == len(dgre) == len(sdte) == len(cmnt):
    pprint(pandas.DataFrame([*zip(inst, prgm, stus, dgre, sdte, cmnt)]))
