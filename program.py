import math
from math import pi
from Tools.web_tools import Scrapping
from Tools.file_tools import File_Manager
import re
from bokeh.plotting import figure, output_file, show
from bokeh.models import Legend, LabelSet, ColumnDataSource
from bokeh.transform import cumsum
import pandas as pd

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
            header.append(f"{scrapping.tag_text(col).lower()} ({scrapping.tag_text(sub_cols[0]).lower()})")
            header.append(f"{scrapping.tag_text(col).lower()} ({scrapping.tag_text(sub_cols[1]).lower()})")
        elif scrapping.tag_text(col) == 'Second tour':
            header.append(f"{scrapping.tag_text(col).lower()} ({scrapping.tag_text(sub_cols[2]).lower()})")
            header.append(f"{scrapping.tag_text(col).lower()} ({scrapping.tag_text(sub_cols[3]).lower()})")
        else:
            header.append(scrapping.tag_text(col).lower())
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
        content += head
        if header.index(head) < len(header) - 1:
            content += ','
    content += '\n'
    for row in lines:
        for elt in row:
            content += elt
            if row.index(elt) < len(row) - 1:
                content += ','
        content += '\n'
    manager.create_file('results', 'election', 'csv', content)

    output_file("election.html") 

    graph = figure(title = "French Presidential Elections in 2022")
    x, y, radius = 0, 0, 1

    df = pd.read_csv(manager.get_file_path())
    votes = df['premier tour (%)']
    radians = [math.radians((percent / 100) * 360) for percent in votes]
    start = [math.radians(0)]
    prev = start[0]
    for i in radians[:-1]:
        start.append(i + prev)
        prev = i + prev
    end = start[1:] + [math.radians(0)]

    color = ['#ffeb00', '#0D378A', '#cc2443', '#404040', '#0066CC', '#00c000', '#26c4ec', '#dd0000', '#0082C4', '#FF8080', '#bb0000', '#bb0001']
    df['couleurs'] = color
    df['angle'] = df['premier tour (%)'] / df['premier tour (%)'].sum() * 2 * pi
    source = ColumnDataSource(df)
    graph.wedge(x=0, y=1, radius=radius,
    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
    line_color="white", fill_color='couleurs', source=source)

    # legend = Legend(items=candidates)
    # graph.addLayout(legend, 'right')

    
    labels = labels = LabelSet(x=0, y=1, text_color='white', text='candidats', angle=cumsum('angle', include_zero=True), source=source, render_mode='canvas')
    graph.add_layout(labels)

    graph.axis.axis_label = None
    graph.axis.visible = False
    graph.grid.grid_line_color = None
    show(graph)

if __name__ == '__main__':
    main()