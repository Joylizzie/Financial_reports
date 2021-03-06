drop table if exists companies CASCADE;
drop table if exists currencies cascade;
drop table if exists chart_of_accounts CASCADE;
drop table if exists coa_categories CASCADE;
drop table if exists purchase_orders CASCADE;
drop table if exists purchase_orders_items;
drop table if exists vendors CASCADE;
drop table if exists customers CASCADE;
drop table if exists products CASCADE;
drop table if exists sales_orders CASCADE;
drop table if exists sales_invoices CASCADE;

/*
create below tables: 
	companies, 
	coa_catagories,
    chart_of_accounts,
	profit_centres,
	cost_centres,
	wbs_code,
	currencies,
    vendors, 
    customers, 
	product_categoties,
    products, 
	purchase_orders, 
	purchase_orders_items,
    sales_orders,
    sales_invoices
*/


-- company_code should be country's name in two capital letters, plus three digits
-- company_name
create table if not exists companies (
company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) primary key not null,
company_name varchar(30) not null
);

create table if not exists currencies(
currency_id serial primary key,
currency_name char(3) check(currency_name ~ '[A-Z]{3}') not null
);

--balance sheet category: assets, liabilities, equity
--profit_loss category: revenue, cost_of_goods, gross_margin, operation_expenses
create table coa_categories(
	coacat_id serial primary key, 
	coa_category_name varchar(15) not null);

create table if not exists chart_of_accounts(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	general_ledger_number numeric(6) not null,
	general_ledger_name varchar(20) not null,
	coacat_id integer references coa_categories(coacat_id) not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_coacategory
      FOREIGN KEY(coacat_id) 
	  REFERENCES coa_categories(coacat_id)
	); 

	  
ALTER TABLE chart_of_accounts ALTER COLUMN general_ledger_name TYPE varchar(30);

create table if not exists profit_centres(
	pc_id char(6) check(pc_id ~ '[A-Z]{2}[0-9]{4}') primary key, 
	pc_name varchar(20));
					
create table if not exists cost_centres(
	cc_id char(6) check(cc_id ~ '[A-Z]{2}[0-9]{4}') primary key, 
	name varchar(20),
	pc_id char(6),
	constraint fk_profitcentre
		foreign key (pc_id)
			references profit_centres(pc_id)
);
					
create table if not exists wbs(
	wbs_code char(5) check(wbs_code ~ '[A-Z]{2}[0-9]{3}') primary key, 
	name varchar(20),
	pc_id char(6),
	constraint fk_profitcentre
		foreign key (pc_id)
			references profit_centres(pc_id)
);

create table if not exists vendors (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	vendor_id varchar(10) primary key,
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
	  REFERENCES companies(company_code)	
);

alter table if not exists vendors 
   add CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id);
   
create table if not exists customers (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	customer_id varchar(6) primary key check (customer_id ~ '[A-Z]{3}[0-9]{3}' ),
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
	  REFERENCES companies(company_code)
	);
	
alter table if not exists customers 
   add CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id);
	
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
	item_id integer not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_po
      FOREIGN KEY(p_order_id) 
	  REFERENCES purchase_orders(p_order_id),
	CONSTRAINT fk_products
      FOREIGN KEY(product_id) 
	  REFERENCES products(product_id),	
    );
	
create table if not exists products (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	product_id serial primary key not null,
	product_category varchar(15) not null,
	product_name varchar(60) not null,
	product_unit_name varchar(6),
	product_units integer,
	product_unit_price numeric check (product_unit_price > 0) not null,
	currency_id integer references currencies not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code)
);

alter table if not exists products 
   add CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id);

create table if not exists sales_orders (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	sales_order_id serial primary key not null,
	s_order_date DATE NOT NULL DEFAULT CURRENT_DATE,
	product_id integer not null,
	product_unit_name varchar(6),
	units integer,
	unit_selling_price numeric not null,
	currency_id integer references currencies not null,
    general_ledger_number numeric(6),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id),
	CONSTRAINT fk_productid
      FOREIGN KEY(product_id) 
	  REFERENCES products(product_id)
  );
  
alter table if not exists sales_orders 
   add CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id);

create table if not exists sales_invoices (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	invoice_date DATE NOT NULL DEFAULT CURRENT_DATE,
	invoice_id serial primary key not null,
    sales_order_id serial not null,
	customer_id varchar(10) check (customer_id ~ '[A-Z]{3}[0-9]{3}' ),
    product_id varchar(60),
	product_unit_name varchar(6),
	product_units integer,
	product_unit_selling_price numeric not null,
    general_ledger_number numeric(6) default 501001,
	  CONSTRAINT fk_invoice
      	FOREIGN KEY(sales_order_id) 
	  		REFERENCES sales_orders(sales_order_id),
	  CONSTRAINT fk_customer
      	FOREIGN KEY(customer_id) 
	  		REFERENCES customers(customer_id),
	CONSTRAINT salesorderid
      	FOREIGN KEY(sales_order_id) 
	  		REFERENCES sales_orders(sales_order_id),
	 CONSTRAINT fk_companyCode
      	FOREIGN KEY(company_code) 
	  		REFERENCES companies(company_code)
		);


/*Create conceptial values*/

insert into companies(company_code, company_name)
                values
                  ('US001', 'Company_US');
				  
select * from companies;
				  
insert into coa_categories(coa_category_name)
    values('assets'),
	('liabilities'),
	('equity');
	
select * from coa_categories;

insert into chart_of_accounts(company_code, general_ledger_number, general_ledger_name, coa_id)
 		values('US001', 100001,'checking_account',1),
	       ('US001', 101001,'inventory',1),
			('US001', 102001,'account_receivables',1),
			('US001', 103001,'prepaied_expenses',1),
			('US001', 104001,'property_plant_equipment',1),
			('US001', 104002,'depreciation',1),
			('US001', 105001,'other_assets',1),
			('US001', 200001,'accounts_paybles',2),
			('US001', 201001,'accrued_expenses',2)
		    ('US001', 202001,'unearned_revenue',2),
	        ('US001', 203001,'tax_payable',2),
			('US001', 204001,'other_payables',2),
			('US001', 205001,'long_term_debt',2),
			('US001', 206001,'other_long_term_libilities',2),
			('US001', 301001,'equity_capital',3),
			('US001', 302002,'retaining_earnings',3),
			('US001', 501001,'revenue',5),
			('US001', 502001,'cost_of_goods_sold',5),
			('US001', 600001,'research_development',6),			
			('US001', 600002,'advertising',6),
			('US001', 600003,'rent',6),
			('US001', 600004,'utilities',6),
			('US001', 600005,'wages',6),
			('US001', 600006,'office_supplies',6),
			('US001', 600007,'depreciation',6),
			('US001', 600008,'insurance',6),
			('US001', 600009,'other_expense',6),
			('US001', 600010,'interest_expense',6)
			;	
	
select * from chart_of_accounts as coa
join coa_categories ca
on coa.coa_id = ca.coa_id;

insert into customers (company_code, customer_id,customer_name, address_line1, city)
	values('US001', 'ABC001','customer_abc','1st_ave', 'seattle');

select * from customers;

insert into vendors (company_code, customer_id,customer_name, address_line1, city)
	values('US001', 'ABC001','customer_abc','1st_ave', 'seattle');

select * from customers;

insert into product_categories(category_name)
 	values('h_ware'),
	       ('s_ware'),
		   ('service');
		   
select * from product_categories;

insert into products(company_code, product_id, product_category, 
					 product_name, product_units, product_unit_price)
		  values('US001', 1,)


	





