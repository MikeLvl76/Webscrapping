from Tools.web_tools import Scrapping
from Tools.file_tools import File_Manager
import re

# test with french presidential elections
def main():
    scrapping = Scrapping()
    manager = File_Manager()
    url = scrapping.open_url("https://fr.wikipedia.org/wiki/%C3%89lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")
    scrapping.save_page(url)

    tables = scrapping.take_tags('table', attrs={'class': 'wikitable centre'})
    table = scrapping.get_one(tables, by_string="Résultats de l'élection présidentielle française de 2022")
    body = scrapping.take_specific_subtag(table, 'tbody')
    trs = scrapping.take_specific_subtags(body, 'tr')
    cols = scrapping.take_specific_subtags(trs[0], 'th')
    sub_cols = scrapping.take_specific_subtags(trs[1], 'th')

    header, lines = [], []
    for col in cols:
        if scrapping.tag_text(col) == 'Premier tour':
            header.append(f"{scrapping.tag_text(col)} ({scrapping.tag_text(sub_cols[0])})")
            header.append(f"{scrapping.tag_text(col)} ({scrapping.tag_text(sub_cols[1])})")
        elif scrapping.tag_text(col) == 'Second tour':
            header.append(f"{scrapping.tag_text(col)} ({scrapping.tag_text(sub_cols[2])})")
            header.append(f"{scrapping.tag_text(col)} ({scrapping.tag_text(sub_cols[3])})")
        else:
            header.append(scrapping.tag_text(col))
    rows = scrapping.take_specific_subtags(trs[2:14], 'td')
    for row in rows:
        if len(row) != 0:
            for i in range(1, len(row)):
                row[i] = re.sub('\[(.*?)\]', '', scrapping.tag_text(row[i]))
                if row[i].find(',') != -1:
                    row[i] = row[i].replace(',', '.')
            lines.append(row[1:])

    content = ''
    for head in header:
        content += head + ','
    content += '\n'
    for row in lines:
        for elt in row:
            content += elt + ','
        content += '\n'
    manager.create_file('results', 'election', 'csv', content)

if __name__ == '__main__':
    main()