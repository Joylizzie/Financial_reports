/*recreate the database if REALLY needed*/
--drop database if exists ocean_stream;
--create database ocean_stream;

--show search_path;

drop table if exists companies CASCADE;
drop table if exists coa_categories CASCADE;
drop table if exists currencies cascade;
drop table if exists tax CASCADE;
drop table if exists chart_of_accounts CASCADE;
drop table if exists profit_centres CASCADE;
drop table if exists cost_centres CASCADE;
drop table if exists wbs CASCADE;
drop table if exists vendors CASCADE;
drop table if exists customers CASCADE;
drop table if exists product_categories cascade;
drop table if exists products CASCADE;
drop table if exists purchase_orders CASCADE;
drop table if exists purchase_orders_items;
drop table if exists sales_orders CASCADE;
drop table if exists sales_orders_items CASCADE;
drop table if exists sales_invoices CASCADE;

-- company_code should be country's name in two capital letters, plus three digits
-- company_name
create table if not exists companies (
company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) primary key not null,
company_name varchar(30) not null
);

--Functional currency of Parent company is different than it's subsidaries when they run in differnet jurisdiction.
create table if not exists currencies(
currency_id serial primary key,
currency_name char(3) check(currency_name ~ '[A-Z]{3}') not null,
description varchar(20),
functional_currency boolean	
);

--balance sheet category: assets, liabilities, equity
--profit_loss category: revenue, cost_of_goods, gross_margin, operation_expenses
create table coa_categories(
	coacat_id integer primary key, 
	coa_category_name varchar(15) not null);
	
create table tax(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	tax_code serial primary key,
	tax_name varchar(15) unique,
	tax_rate numeric(4,4) not null,
	tax_area varchar(20) not null,
	tax_belongto varchar(15) check( tax_belongto in ('state','federal')),
    description varchar(30) not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code)
);

create table if not exists chart_of_accounts(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	general_ledger_number numeric(6) not null,
	general_ledger_name varchar(30) unique not null,
	coacat_id integer references coa_categories(coacat_id) not null,
	currency_id integer references currencies(currency_id),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_coacategory
      FOREIGN KEY(coacat_id) 
	  REFERENCES coa_categories(coacat_id),
	constraint fk_currency
		foreign key(currency_id)
			references currencies(currency_id)
	); 

--A profit centre is for arregating revenue and cost for a company.
--A profit centre can have mulitple cost centres and wbs codes.
create table if not exists profit_centres(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	pc_id char(6) check(pc_id ~ '[A-Z]{2}[0-9]{4}') primary key, 
	pc_name varchar(20),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  	REFERENCES companies(company_code));

--A cost is for accumulating cost for a group.
create table if not exists cost_centres(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	cc_id char(6) check(cc_id ~ '[A-Z]{2}[0-9]{4}') primary key, 
	name varchar(20),
	pc_id char(6),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	    REFERENCES companies(company_code),
	constraint fk_profitcentre
		foreign key (pc_id)
			references profit_centres(pc_id)
);

--A wbs code is for accumulating cost for a product is in developing.
create table if not exists wbs(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	wbs_code char(5) check(wbs_code ~ '[A-Z]{2}[0-9]{3}') primary key, 
	name varchar(20),
	pc_id char(6),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	    REFERENCES companies(company_code),
	constraint fk_profitcentre
		foreign key (pc_id)
			references profit_centres(pc_id)
);

--A vendor sells goods, or provides services or both to the company.
--In accounting operations, an invoice from a vendor will be booked against this vendor as accounts payable.
create table if not exists vendors (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	vendor_id char(6) primary key,
	vendor_name varchar(60) not null unique,
    general_ledger_number char(6) default 200001,
	currency_id integer references currencies not null,
	address_line1 varchar(60) not null,
	address_line2 varchar(20),
	city          varchar(30) not null,
	state         varchar(15),
	country       varchar(20),
	postcode       varchar(10),
	phone_number  varchar(20),
	email_address varchar(100),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id)
);

create table if not exists customers (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	customer_id char(6) primary key check (customer_id ~ '[A-Z]{3}[0-9]{3}' ),
	customer_name varchar(60) not null unique,
    general_ledger_number char(6) default '102001',
	currency_id integer references currencies not null,
	address_line1 varchar(60) not null,
	city          varchar(30) not null,
	state         varchar(15),
	country       varchar(20),
	postcode       varchar(10),
	phone_number  varchar(20),
	email_address varchar(100),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id)
	);
	

create table product_categories(
	cat_id serial primary key,
	cat_name varchar(15) unique not null,
	subcat_id integer,
	subcat_name varchar(15)
    );

create table if not exists products (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	product_id serial primary key not null,
	cat_id integer references product_categories(cat_id) not null,
	product_name varchar(60) not null,
	product_unit_name varchar(6),
	product_units integer,
	product_unit_price numeric check (product_unit_price > 0) not null,
	currency_id integer references currencies not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_currencyid
      	FOREIGN KEY(currency_id) 
	  		REFERENCES currencies(currency_id),
	CONSTRAINT fk_productcat
      	FOREIGN KEY(cat_id) 
	  		REFERENCES product_categories(cat_id)
);

create table if not exists purchase_orders (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	p_order_id serial primary key,
	p_order_date DATE NOT NULL DEFAULT CURRENT_DATE,
	vendor_id varchar(10) not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_vendor
      FOREIGN KEY(vendor_id) 
	  REFERENCES vendors(vendor_id)
    );

create table if not exists purchase_orders_items (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	p_order_id integer references purchase_orders(p_order_id) not null,
	product_id integer references products(product_id),
	item_id serial not null,
	cc_id char(6) references cost_centres(cc_id),
	general_ledger_number integer check(general_ledger_number in(502001, 600001)),
	wbs_code char(5) references wbs(wbs_code), 
	tax_code integer references tax(tax_code) not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_po
      FOREIGN KEY(p_order_id) 
	  REFERENCES purchase_orders(p_order_id),
	CONSTRAINT fk_products
      FOREIGN KEY(product_id) 
	  REFERENCES products(product_id),
	CONSTRAINT fk_tax
      FOREIGN KEY(tax_code) 
	    REFERENCES tax(tax_code),
     CONSTRAINT fk_costcentre
       FOREIGN KEY(cc_id) 
	    REFERENCES cost_centres(cc_id),	
	 CONSTRAINT fk_wbs
       FOREIGN KEY(wbs_code) 
	    REFERENCES wbs(wbs_code)
	
    );

create table if not exists sales_orders(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	sales_order_id serial primary key not null,
	s_order_date DATE NOT NULL DEFAULT CURRENT_DATE,
	customer_id char(6) references customers(customer_id),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	 CONSTRAINT fk_customer
      	FOREIGN KEY(customer_id) 
	  		REFERENCES customers(customer_id)
);

create table if not exists sales_orders_items (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	sales_order_id integer not null,
	item_id serial,
	product_id integer not null,
	unit_name varchar(6),
	units integer,
	unit_selling_price numeric not null,
   	currency_id integer references currencies not null,
   	tax_code integer references tax(tax_code) not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id),
	CONSTRAINT fk_productid
      FOREIGN KEY(product_id) 
	  REFERENCES products(product_id),
	CONSTRAINT fk_tax
      FOREIGN KEY(tax_code) 
	    REFERENCES tax(tax_code)

  );
 
create table if not exists sales_invoices (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	invoice_date DATE NOT NULL DEFAULT CURRENT_DATE,
	invoice_id serial primary key not null,
    sales_order_id serial not null,
	customer_id char(6) check (customer_id ~ '[A-Z]{3}[0-9]{3}' ),
	item_id serial,
    product_id integer not null,
	product_unit_name varchar(6),
	units integer,
	unit_selling_price numeric not null,
    general_ledger_number integer default 501001,
	tax_code integer references tax(tax_code) not null,
	cc_id char(6) references cost_centres(cc_id),
    CONSTRAINT fk_salesorders
      	FOREIGN KEY(sales_order_id) 
	  		REFERENCES sales_orders(sales_order_id),
	  CONSTRAINT fk_customer
      	FOREIGN KEY(customer_id) 
	  		REFERENCES customers(customer_id),
	 CONSTRAINT fk_companyCode
      	FOREIGN KEY(company_code) 
	  		REFERENCES companies(company_code),
	 CONSTRAINT fk_tax
        FOREIGN KEY(tax_code) 
	      REFERENCES tax(tax_code),
     CONSTRAINT fk_costcentre
       FOREIGN KEY(cc_id) 
	    REFERENCES cost_centres(cc_id),	
	CONSTRAINT fk_productid
      FOREIGN KEY(product_id) 
	  REFERENCES products(product_id)	
		);


-- Create conceptual values.

insert into companies(company_code, company_name)
                values
                  ('US001', 'OceanStream_US');
				  
-- select * from companies;
				  
insert into coa_categories(coacat_id,coa_category_name)
    values(1,'assets'),
	(2,'liabilities'),
	(3,'equity'),
	(5,'revenue'),
	(6,'expenses');
	
-- select * from coa_categories;

insert into currencies(currency_name, description)
 	values('USD', 'American_dollar'),
	       ('CNY', 'Chines_Yuan');
		   
-- select * from currencies;

insert into tax(company_code,tax_name, tax_rate, tax_area, tax_belongto,description)
   values('US001','sales_tax', 0.10, 'US_Seattle','state','pec_of_sales');
		  
-- select * from tax;

insert into chart_of_accounts(company_code, general_ledger_number, general_ledger_name,
							  coacat_id,currency_id)
 		values('US001', 100001,'checking_account',1,1),
	       ('US001', 101001,'inventory',1,1),
			('US001', 102001,'account_receivables',1,1),
			('US001', 103001,'prepaied_expenses',1,1),
			('US001', 104001,'property_plant_equipment',1,1),
			('US001', 104002,'accum_depreciation',1,1),
			('US001', 105001,'other_assets',1,1),
			('US001', 200001,'accounts_paybles',2,1),
			('US001', 201001,'accrued_expenses',2,1),
		    ('US001', 202001,'unearned_revenue',2,1),
	        ('US001', 203001,'tax_payable',2,1),
			('US001', 204001,'other_payables',2,1),
			('US001', 205001,'long_term_debt',2,1),
			('US001', 206001,'other_long_term_libilities',2,1),
			('US001', 301001,'equity_capital',3,1),
			('US001', 302002,'retaining_earnings',3,1),
			('US001', 501001,'revenue',5,1),
			('US001', 502001,'cost_of_goods_sold',5,1),
			('US001', 600001,'research_development',6,1),			
			('US001', 600002,'advertising',6,1),
			('US001', 600003,'rent',6,1),
			('US001', 600004,'utilities',6,1),
			('US001', 600005,'wages',6,1),
			('US001', 600006,'office_supplies',6,1),
			('US001', 600007,'depreciation',6,1),
			('US001', 600008,'insurance',6,1),
			('US001', 600009,'other_expense',6,1),
			('US001', 600010,'interest_expense',6,1)
			;	
/*	
select * from chart_of_accounts as coa
join coa_categories ca
on coa.coacat_id = ca.coacat_id;
*/

insert into customers (company_code, customer_id,customer_name, currency_id, address_line1, city)
	values('US001', 'ABC001','customer_abc',1,'1st_ave', 'seattle');

/*
select * from customers as cus
join currencies cur
on cus.currency_id = cur.currency_id;
*/

insert into vendors (company_code, vendor_id,vendor_name, currency_id,address_line1, city)
	values('US001', 'VBC001','vendor_vbc',1,'1st_street', 'seattle');

/*
select * from vendors as v
join currencies cur
on v.currency_id = cur.currency_id;
*/

insert into product_categories(cat_name)
 	values('h_ware'),
	       ('s_ware'),
		   ('service');
		   
-- select * from product_categories;

insert into products(company_code, cat_id, 
					 product_name, product_units, product_unit_price, currency_id)
		  values('US001', 1, 'server', 1, 250000,1);
		  
-- select * from products;

insert into profit_centres(company_code, pc_id,pc_name)
  values('US001', 'SE0001','hard_ware_SE');
  
-- select * from profit_centres;

insert into cost_centres(company_code, cc_id, name,pc_id)
  values('US001', 'SE0001','hard_ware_SE_server', 'SE0001');
  
-- select * from cost_centres;


insert into wbs(company_code,wbs_code, name, pc_id)
  values('US001', 'LS001','livestream_1', 'SE0001');
  
-- select * from wbs;
 
 insert into purchase_orders(company_code, vendor_id)
 values('US001','VBC001');
 
-- select * from purchase_orders;
 
/* 
select * from purchase_orders_items pt
join purchase_orders po
on pt.p_order_id = po.p_order_id;
*/
	
insert into sales_orders(company_code, customer_id)
   values('US001','ABC001');

-- select * from sales_orders;

insert into sales_orders_items(company_code, sales_order_id,
							  product_id,units,unit_selling_price, currency_id,tax_code)
	values('US001',1,1,1,520000,1,1);

/*
select * from sales_orders_items st
join sales_orders so
on st.sales_order_id = so.sales_order_id;
*/

insert into sales_invoices(company_code, sales_order_id, customer_id,product_id, 
						   units, unit_selling_price,tax_code, cc_id)
	values('US001',1,'ABC001',1,1,520000,1,'SE0001');
	
-- select * from sales_invoices;




