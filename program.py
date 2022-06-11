from Tools.web_tools import Scrapping
from Tools.file_tools import File_Manager
import re

# test with french presidential elections
def main():
    scrapping = Scrapping()
    manager = File_Manager()
    url = scrapping.open_url("https://fr.wikipedia.org/wiki/%C3%89lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")
    scrapping.save_page(url)
    table = scrapping.take_tag('table', attrs={'class':'wikitable'})
    body = scrapping.take_specific_subtag(table, 'tbody')
    lines = scrapping.take_specific_subtags(body, 'tr')
    names = scrapping.take_specific_subtag(lines[1:len(lines)], 'td')
    text = scrapping.tag_text(names)
    text_formatted = [re.sub(r"\(([^()]+)\)", ",", item) for item in text]
    cols = [item.split(',')[:-1] for item in text_formatted]
    content = ''
    for col in cols:
        content += col[0] + ',' + col[1] + '\n'
    manager.create_file('results', 'election', 'csv', content)
    return

if __name__ == '__main__':
    main()