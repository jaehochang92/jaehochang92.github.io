from crawler import crawl_data
import pandas as pd
import datetime

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

if __name__ == '__main__':
    main()
    