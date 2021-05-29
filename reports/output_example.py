import os
import datetime
import csv
from bokeh.io import output_notebook, output_file, save
from bokeh.plotting import figure, show
from bokeh.models import (HoverTool, ColumnDataSource)
import pathlib


def graph():
    end_date = datetime.date(2021,3,31)
    head, tail =  os.path.split(pathlib.Path(__file__).parent.absolute())
    path = os.path.join(head, 'reporting_results', 
            f'profit_loss_by_pc_{end_date.strftime("%m_%Y")}.html')
    output_file(filename=path, title=f'profit and loss during {end_date.strftime("%b-%Y")}')
    p = figure()
    p.line(x = [1,2,3], y = [1, 2, 3])

    #show(p)
    save(p)

if __name__ == '__main__':
    graph()

