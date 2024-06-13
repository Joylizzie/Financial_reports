from django.shortcuts import render
from pathlib import Path

from django.conf import settings
from django.http import HttpResponse
from bokeh.plotting import figure
from bokeh.resources import CDN
from django.views import generic
from bokeh.embed import components, file_html
from django.db import connections
from itertools import chain
from pathlib import Path
import csv

import pandas as pd
from bokeh.models import (HoverTool, ColumnDataSource,NumeralTickFormatter)
from math import pi

def index(request):
    return render(request, 'finreports/index.html')

def balancesheet(request):

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    csv_fp = open(f'{BASE_DIR}/reporting_results/4_sum_bs_03_2021.csv', 'r')
    reader = csv.DictReader(csv_fp)
    out = [row for row in reader]
    return render(request, 'finreports/balancesheet/bs.html', {'data' : out})

def pl(request):
    conn = connections['default']
    func = """select * from transaction_list('US001',500000, 999999, '2021-03-01', '2021-03-31')"""
    with conn.cursor() as curs:
        curs.execute("set search_path to ocean_stream;")
        curs.execute(func)
        pls = curs.fetchall()

        conn.commit()
        df = pd.DataFrame(pls, columns=['company_code', 'sub_name','profit_centre','currency_id','amount'])
        df['amount'] = df['amount'].astype(float)
        # a list of unique profit centres for bokeh figure
        pcs = list(df['profit_centre'].unique())
        # a list of unique sub_name for different graphs
        sub_names = list(df['sub_name'].unique())
        # dataframes filtered by sub_name 
        df_rev = df.loc[df['sub_name']== 'Revenue']
        df_exp = df.loc[df['sub_name']== 'Expenses']
        #turn above sub_name dataframe into ColumnDataSource
        source_rev = ColumnDataSource(df_rev)
        source_exp = ColumnDataSource(df_exp)
        # # save the html file to folder '/home/lizhi/projects/joylizzie/Financial_reports/reporting_results/htmls'
        # head, tail =  os.path.split(pathlib.Path(__file__).parent.absolute())
 
        # path = os.path.join(head, 'reporting_results/htmls', f'3_profit_loss_by_pc_{end_date.strftime("%m_%Y")}.html')
        # output_file(filename=path, title=f'profit and loss during {end_date.strftime("%b-%Y")}')        

        p = figure(x_range=pcs,                 
                   height=500,
                  width=550,
               title='Profit and loss by profit centre',
               x_axis_label="Profit centres",
               y_axis_label="Amount",
               toolbar_location="right")

        p.vbar(x='profit_centre',
            top='amount',
            bottom = 0,
            source = source_rev,
            width=0.8,
            color='blue',
            legend_label='Revenue')

        p.vbar(x='profit_centre',
            top='amount',
            bottom = 0,
            source = source_exp,
            width=0.9,
            color='red',
            legend_label='Expenses')

        p.add_tools(HoverTool(tooltips=[('company_code', '@company_code'),
                                        ('profit_centre', '@profit_centre'),                                    
                                    ('amount', '@amount')], mode='vline'))
                                    
        p.yaxis.formatter=NumeralTickFormatter(format="$‘0 a’")        
        p.xaxis.major_label_orientation = pi/4 
        p.xaxis.axis_label_text_font_size = "12pt"
        p.axis.axis_label_text_font_style = 'bold'                               
        p.legend.orientation = "horizontal"
        p.legend.label_text_font_size = '8pt'

        script, div = components(p)
 
        return render(request, 'finreports/pl/pl.html', {'script': script, 'div': div})


def araging(request):

    return render(request,"this is Account receivable aging")