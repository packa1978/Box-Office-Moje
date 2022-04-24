import requests
import pandas as pd
from requests_html import HTML

import datetime

url = "https://www.boxofficemojo.com/year/world/"


# to open up the page using Python
# safe text from the website into html file
def url_to_txt( url , filename='world.html', save=False):
    r = requests.get(url)
    if r.status_code == 200:  # code 200 confirms that it was successful
        html_text = r.text
        if save:
            with open(filename, 'w') as f:  # to save this page onto a local system
                f.write(html_text)
        return html_text
    return None


''''Another way to store data as a date object
import datetime 
now = datetime.datetime.now()
year = now.year
def url_to_file(url, filename = "world.html"):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        with open(f' word -{year}.html, 'w') as f:
            f.write(html_text)
        return html_text
    return ""
'''

# extracting and turning data into csv file (table only ),
# please use requests-html package for parsing

def parse_and_extract(url, name='2022'):
    html_text = url_to_txt(url)
    if html_text == None:
        return
#re-declare - this turns an HTML string into something that's managed by requests HTML
    r_html = HTML(html=html_text)
# find table class, inspect html page using view/developer/inspect elements
    table_class = ".imdb-scroll-table"
    r_table = r_html.find(table_class)  # our element
    # print(r_table)
# grabbing value inside HTML element
    table_data = []
    header_names = []
    if len(r_table) == 1:
        # print(r_table[0].text)
        parsed_table = r_table[0]
        rows = parsed_table.find("tr")  # 'tr' stands for table row inside HTML,this is list of elements
        header_row = rows[0]
        header_cols = header_row.find("th")
        header_names = [x.text for x in header_cols]
        for row in rows[1:]:
            # print(row.text)
            cols = row.find("td")
            row_data = []
            for i, col in enumerate(cols):  # enumerate is helpful when you need a count and the value form an iterable
                # print(i, col.text, '\n\n')
                row_data.append(col.text)
            table_data.append(row_data)
        # save it as csv file
        df = pd.DataFrame(table_data, columns=header_names)
        df.to_csv(f'{name}.csv', index=False)


'''parse_and_extract(url, '2022')
url = "https://www.boxofficemojo.com/year/world/2021"
parse_and_extract(url, '2021 ')
url = "https://www.boxofficemojo.com/year/world/2020"
parse_and_extract(url, '2020')
'''

# print(header_names)

# print(table_data)
def run(start_year=None, years_ago=10):
    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year
        assert isinstance(start_year, int)  # to make sure that this is an integer
        assert isinstance(years_ago, int)  # to make sure that this is an integer
        assert len(f'{start_year}') == 4  # make sure it has four digits
        for i in range(0, years_ago + 1):
            url = f"https://www.boxofficemojo.com/year/world/{start_year}/"
            parse_and_extract(url, start_year)
            print(f'Finished {start_year}')
            start_year -= 1


if __name__ == "__main__":
    run()