import os
import psycopg2
import datetime
import csv
import pandas as pd
from bokeh.io import output_notebook, output_file, save
from bokeh.plotting import figure, show
from bokeh.models import (HoverTool, ColumnDataSource)


# connect to Postgres
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn

def get_sub_graph(conn, start_date, end_date):
    func = """select * from transaction_list('US001',500000, 999999, '2021-03-01', '2021-03-31')"""
    with conn.cursor() as curs:
        curs.execute(func)
        pls = curs.fetchall()

        conn.commit()
        df = pd.DataFrame(pls, columns=['company_code', 'sub_name','profit_centre','currency_id','amount'])
        # a list of unique profit centre for bokeh figure
        pcs = list(df['profit_centre'].unique())
        # a list of unique sub_name for different graphs
        sub_names = list(df['sub_name'].unique())
        # dataframes filtered by sub_name 
        df_rev = df.loc[df['sub_name']== 'Revenue']
        df_exp = df.loc[df['sub_name']== 'Expenses']
        #turn above sub_name dataframe into ColumnDataSource
        source_rev = ColumnDataSource(df_rev)
        source_exp = ColumnDataSource(df_exp)
        
        filename = f'profit_loss_by_pc_{end_date.strftime("%m_%Y")}.html'
        filepath = 'reporting_results/htmls'
        
        output_file(filename=filename, title=f'profit and loss during {end_date.strftime("%b-%Y")}')
        p = figure(x_range=pcs,                 
                   plot_height=500,
                  plot_width=500,
               title='Profit and loss by profit centre',
               x_axis_label="profit centre",
               y_axis_label="Amount",
               toolbar_location="below")

        p.vbar(x='profit_centre',
            top='amount',
            bottom = 0,
            source = source_rev,
            width=0.9,
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
        p.legend.orientation = "horizontal"
        p.legend.label_text_font_size = '8pt'
        show(p)
        save(p)
        #return p

if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    start_date = datetime.date(2021,3,1)
    end_date = datetime.date(2021,3,31)
    col_names = ['company_code', 'sub_name','profit_centre', 'currency_id','amount']
    df=get_sub_graph(conn, start_date, end_date)

