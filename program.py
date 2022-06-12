import math
from math import pi
from Tools.web_tools import Scrapping
from Tools.file_tools import File_Manager
from bokeh.plotting import figure, output_file, show
from bokeh.models import Legend, LegendItem, LabelSet, ColumnDataSource
from bokeh.transform import cumsum
import pandas as pd

# test with french presidential elections
def main():
    scrapping = Scrapping()
    manager = File_Manager()
    url = scrapping.open_url("https://fr.wikipedia.org/wiki/%C3%89lection_pr%C3%A9sidentielle_fran%C3%A7aise_de_2022")
    scrapping.save_page(url)

    tables = scrapping.take_tags('table', attrs={'class': 'wikitable centre'}) # get all tables with wikitable centre class
    table = scrapping.get_one(tables, by_string="Résultats de l'élection présidentielle française de 2022") # find this string inside table and return first table having it
    body = scrapping.take_specific_subtag(table, 'tbody') # get body table
    trs = scrapping.take_specific_subtags(body, 'tr') # get rows
    cols = scrapping.take_specific_subtags(trs[0], 'th') # get the headers in the first row
    sub_cols = scrapping.take_specific_subtags(trs[1], 'th') # get other rows

    header, lines = [], []
    # create header for csv
    for col in cols:
        if scrapping.tag_text(col) == 'Premier tour':
            header.append(f"{scrapping.tag_text(col).lower()} ({scrapping.tag_text(sub_cols[0]).lower()})")
            header.append(f"{scrapping.tag_text(col).lower()} (pourcentage)")
        elif scrapping.tag_text(col) == 'Second tour':
            header.append(f"{scrapping.tag_text(col).lower()} ({scrapping.tag_text(sub_cols[2]).lower()})")
            header.append(f"{scrapping.tag_text(col).lower()} (pourcentage)")
        else:
            header.append(scrapping.tag_text(col).lower())
    # get necessary rows : just candidates
    # data is formatted for better use
    rows = scrapping.take_specific_subtags(trs[2:14], 'td')
    for row in rows:
        if len(row) != 0:
            for i in range(1, len(row)):
                row[i] = scrapping.tag_text(row[i])
                if row[i].find(',') != -1:
                    row[i] = row[i].replace(',', '.')
            lines.append(row[1:])

    # creating content of csv
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
    
    # creating csv file with content
    manager.create_file('results', 'election', 'csv', content)

    # output result for bokeh
    output_file("election.html") 

    # initializing pie chart
    graph = figure(title = "French Presidential Elections in 2022", plot_width = 1200, plot_height=700)
    x, y, radius = 0, 0, 0.7

    # need to read csv file created before
    df = pd.read_csv(manager.get_file_path())

    # inserting new columns to DataFrame enables automatic creation of each part of the pie chart
    color = ['#ffeb00', '#0D378A', '#cc2443', '#404040', '#0066CC', '#00c000', '#26c4ec', '#dd0000', '#0082C4', '#FF8080', '#bb0000', '#bb0001']
    df['couleurs'] = color
    df['angle'] = df['premier tour (pourcentage)'] / df['premier tour (pourcentage)'].sum() * 2 * pi
    df['premier tour (pourcentage)'] = df['premier tour (pourcentage)'].astype(str) # change from float to str (labels only in string type)
    df['premier tour (pourcentage)'] = df['premier tour (pourcentage)'].str.pad(75, side = "left")

    # transform DataFrame to ColmunDataSource to match data with part
    # setting pie chart position and radius, call cumsum for each part angle
    # colors are matched also with data
    source = ColumnDataSource(df)
    graph.wedge(x=0, y=1, radius=radius,
    start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
    line_color="white", legend_group='candidats', fill_color='couleurs', source=source)

    # label for each part 
    # the column called with 'text' has its data used for labels
    labels = labels = LabelSet(x=0, y=1, text_color='white', text='premier tour (pourcentage)', text_font_size='10pt', angle=cumsum('angle', include_zero=True), source=source, render_mode='canvas')

    # options for layout
    graph.add_layout(labels)
    graph.axis.axis_label = None
    graph.axis.visible = False
    graph.grid.grid_line_color = None
    graph.add_layout(graph.legend[0], 'right')

    # execute
    show(graph)

if __name__ == '__main__':
    main()