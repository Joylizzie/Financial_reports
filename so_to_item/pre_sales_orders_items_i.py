import os
import psycopg2
import random
import csv
import itertools

# if rerun the below code, the results of pre_sales_orders_items will be different because of random values were chosen.
# fetch existing sales_order_ids and product_ids in database where the company_code is 'US001'
# generate sale_orders_items tuples.
def _get_conn(pw, user_str):
    conn = psycopg2.connect(host="localhost",
                            database = db,
                            user= user_str,
                            password=pw)
    conn.autocommit = False
    return conn

# get sales order ids placed by individuals
def get_so_ids(conn):

    sql_so = """ select sales_order_id from sales_orders as so
            inner join customer_names as cn
            on so.customer_id = cn.customer_id
            where cn.business_type_id = 2  
			      and cn.company_code='US001' 
			      and so.s_order_date between '2021-03-01' and '2021-03-31';             
         """
    with conn.cursor() as curs:
        curs.execute(sql_so)  #cursor closed after the execute action
        (sales_order_id) = curs.fetchall()
    conn.commit()
    return sales_order_id


def get_product_ids(conn):
    sql_pi = """ select product_id from products as pi 
                where company_code='US001' and product_id between 3 and 5        
             """
    with conn.cursor() as curs:
        curs.execute(sql_pi)  #cursor closed after the execute action
        (product_id) = curs.fetchall()
    conn.commit() 

    return product_id # a list of tupples, but only one item in each tuple
    
    
def weight_pro():
    pro_ids_tups = get_product_ids(conn)  
    pro_ids_lst = [x[0] for x in pro_ids_tups]# get the first item in the tuples then put them in a list
    product_weights = [35, 30, 35] 
    num_items_to_ship = random.choice(list(range(1,len(pro_ids_lst)+1)))
    # get product_id without repeating
    set_pro_ids = set()
    while len(set_pro_ids) < num_items_to_ship:        
        products_to_ship = random.choices(pro_ids_lst, weights = product_weights)
        set_pro_ids.add(products_to_ship[0])

    return set_pro_ids   

# generate item(s) for a single sales order
def so_items(so_id):
    units_sold_lst = list(range(1, 22))
    selling_prices = {3:1500, 4:100, 5:1200}
    shipped_lst = ['yes', 'no']
    shipped_lst_weights = [98,2] # assuming there are 2% of orders were not shipped
    weight_pro_res = weight_pro()   
    return [('US001', #company_code
              so_id,
              product_id,
              random.choice(units_sold_lst),
              selling_prices[product_id], #unit_selling_price 
              1,# currency_id
              1, # tax
              random.choices(shipped_lst, weights=shipped_lst_weights)[0] #shipped?
                ) 
             for product_id in weight_pro_res]  
          
# generate all sales orders with the items generated above
def generate_value_tuples(conn):
    so_ids = get_so_ids(conn)
    lol = (so_items(so_id[0]) for so_id in so_ids)

    return list(itertools.chain(*lol))
    
# generate values and save in csv file, then upload to db from psql which is quicker comparing to below way.
def _to_csv(conn, outfile):
    tups = generate_value_tuples(conn)
    with open(os.path.join('intermediate_csv', outfile), 'w') as write_obj:
        csv_writer = csv.writer(write_obj)
        csv_writer.writerow(['company_code','sales_order_id', 'product_id', 'units', 'unit_selling_price', 'currency_id', 'tax_code', 'shipped'])
        for tup in tups:
            csv_writer.writerow(tup)
        print('Done writing')


if __name__ == '__main__':
    db = 'ocean_stream'
    pw = os.environ['POSTGRES_PW']
    user_str = os.environ['POSTGRES_USER']
    conn = _get_conn(pw, user_str)
    #get_product_ids(conn)
    #weight_pro()
    generate_value_tuples(conn)
    _to_csv(conn, outfile='pre_sales_orders_items_i.csv')
 
