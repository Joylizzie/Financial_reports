show search_path;

DROP SCHEMA IF EXISTS ocean CASCADE;

CREATE SCHEMA IF NOT EXISTS ocean
AUTHORIZATION CURRENT_USER; 

set search_path TO ocean;


drop table if exists companies CASCADE;
drop table if exists coa_categories CASCADE;
drop table if exists business_type CASCADE;

drop table if exists entry_type CASCADE;
drop table if exists general_ledger CASCADE;
drop table if exists general_ledger_item CASCADE;
drop table if exists currencies cascade;
drop table if exists tax CASCADE;
drop table if exists chart_of_accounts CASCADE;
drop table if exists profit_centres CASCADE;
drop table if exists cost_centres CASCADE;
drop table if exists wbs CASCADE;
drop table if exists area_code cascade;
drop table if exists vendors CASCADE;
drop table if exists vendors_addresses CASCADE;
drop table if exists customer_names CASCADE;
drop table if exists customer_addresses CASCADE;
drop table if exists product_categories cascade;
drop table if exists products CASCADE;
drop table if exists purchase_orders CASCADE;
drop table if exists purchase_orders_items;
drop table if exists sales_orders CASCADE;
drop table if exists sales_orders_items CASCADE;
drop table if exists sales_invoices CASCADE;
drop table if exists ap_invoice CASCADE;
drop table if exists ap_invoice_item CASCADE;
drop table if exists ap_payment CASCADE;
drop table if exists ap_payment_item CASCADE;
drop table if exists ar_invoice CASCADE;
drop table if exists ar_invoice_item CASCADE;
drop table if exists ar_receipt CASCADE;
drop table if exists ar_receipt_item CASCADE;

-- company_code should be country's name in two capital letters, plus three digits
-- company_name
create table if not exists companies (
    company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) primary key not null,
    company_name varchar(30) not null
    );

--Functional currency of Parent company is different than it's subsidaries when they run in differnet jurisdiction.
create table if not exists currencies(
    company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
    currency_id serial primary key,
    currency_name char(3) check(currency_name ~ '[A-Z]{3}') not null,
    description varchar(20),
    functional_currency boolean not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code)	
    );

--balance sheet category: assets, liabilities, equity
--profit_loss category: revenue, cost_of_goods, gross_margin, operation_expenses
create table if not exists coa_categories(
	coacat_id integer primary key, 
	coa_category_name varchar(15) not null
    );
	
create table if not exists tax(
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
	general_ledger_number integer check(general_ledger_number between 100000 and 999999) unique not null,
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
	pc_id char(6) check(pc_id ~ '[A-Z]{3}[0-9]{3}') primary key, 
	pc_name varchar(30) not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  	REFERENCES companies(company_code)
    );

--A cost is for accumulating cost for a group.
create table if not exists cost_centres(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	cc_id char(5) check(cc_id ~ '[A-Z]{3}[0-9]{2}') primary key, 
	name varchar(30) not null,
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
	vendor_id char(5) primary key check (vendor_id ~ '[A-Z]{2}[0-9]{3}' ),
	vendor_name varchar(60) not null,
    general_ledger_number integer default 200001,
	currency_id integer references currencies not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id)
	);

create table if not exists vendor_addresses(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	vendor_id char(5) not null,
	address_line1 varchar(250) not null,
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
	CONSTRAINT fk_vendorid
      FOREIGN KEY(vendor_id) 
	  REFERENCES vendors(vendor_id)
    );

create table if not exists business_type(
    company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
    business_type_id serial primary key,
    business_type_name varchar(15) check(business_type_name in ('organization', 'individual')),
    CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	   REFERENCES companies(company_code)
    );


create table if not exists area_code(
  	zip varchar(10) not null,
	zipcode_name varchar(30),
	city varchar(30),
	state char(2),
	county_name varchar(40),
	area char(2)	
	);

create table if not exists customer_names (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	customer_id char(6) primary key check (customer_id ~ '[A-Z]{3}[0-9]{3}' ),
    business_type_id integer not null,
	customer_name varchar(250),
	general_ledger_number integer default 102001,
    currency_id integer not null,    
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code)
	);

create table if not exists customer_addresses (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	customer_id char(6) not null,
	address_line1 varchar(250) not null,
	city          varchar(30) not null,
	state         varchar(15),
	country       varchar(20),
	postcode       varchar(10),
    phone_number   varchar(20),
	email_address  varchar(60),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_customer_id
      FOREIGN KEY(customer_id) 
	  REFERENCES customer_names(customer_id)
	);

create table if not exists product_categories(
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	cat_id serial primary key,
	cat_name varchar(20) not null,
	subcat_id integer,
	subcat_name varchar(20),
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code)
    );

create table if not exists products (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	product_id serial primary key not null,
	cat_id integer references product_categories(cat_id) not null,
	product_name varchar(60) not null,
	product_unit_name varchar(30),
	product_units integer,
	product_unit_price numeric check (product_unit_price > 0) not null,
	currency_id integer references currencies not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_productcat
      	FOREIGN KEY(cat_id) 
	  		REFERENCES product_categories(cat_id),
	CONSTRAINT fk_currencyid
      	FOREIGN KEY(currency_id) 
	  		REFERENCES currencies(currency_id)
    );

create table if not exists purchase_orders (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	p_order_id serial primary key,
	p_order_date DATE NOT NULL DEFAULT CURRENT_DATE,
	vendor_id char(6) not null,
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
	cc_id char(5) references cost_centres(cc_id),
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
	customer_id char(6) references customer_names(customer_id) not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	 CONSTRAINT fk_customer
      	FOREIGN KEY(customer_id) 
	  		REFERENCES customer_names(customer_id)
    );

create table if not exists sales_orders_items (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	sales_order_id integer not null,
	product_id integer not null,
	unit_name varchar(6),
	units integer,
	unit_selling_price numeric not null,
   	currency_id integer references currencies not null,
   	tax_code integer references tax(tax_code) not null,
    shipped boolean not null,
	CONSTRAINT fk_companyCode
      FOREIGN KEY(company_code) 
	  REFERENCES companies(company_code),
	CONSTRAINT fk_productid
      FOREIGN KEY(product_id) 
	  REFERENCES products(product_id),
	CONSTRAINT fk_currencyid
      FOREIGN KEY(currency_id) 
	  REFERENCES currencies(currency_id),
	CONSTRAINT fk_tax
      FOREIGN KEY(tax_code) 
	    REFERENCES tax(tax_code),
    CONSTRAINT fk_salesorders
      	FOREIGN KEY(sales_order_id) 
	  		REFERENCES sales_orders(sales_order_id)
	);

-- sales invoice will be issued to customers with shipped sales order items
create table if not exists sales_invoices (
	company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
	invoice_date DATE NOT NULL DEFAULT CURRENT_DATE,
	invoice_id serial primary key not null,
    sales_order_id integer not null,
	customer_id char(6) references customer_names(customer_id) not null,
	amount numeric(12,2),
	CONSTRAINT fk_companyCode
      	FOREIGN KEY(company_code) 
	  		REFERENCES companies(company_code),
    CONSTRAINT fk_salesorders
      	FOREIGN KEY(sales_order_id) 
	  		REFERENCES sales_orders(sales_order_id),
	 CONSTRAINT fk_customer
      	FOREIGN KEY(customer_id) 
	  		REFERENCES customer_names(customer_id)
    );

create table if not exists entry_type(
    entry_type_id varchar(3) primary key,
    entry_type_name varchar(20) not null,
    description varchar(100)
    );

create table if not exists journal_entry(
        company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
        entry_type_id varchar(3) default 'JE',
        transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
        je_id serial primary key,
        CONSTRAINT fk_companyCode
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),
        CONSTRAINT fk_entrytype
            FOREIGN KEY(entry_type_id) 
	            REFERENCES entry_type(entry_type_id)
        );
 


create table if not exists journal_entry_item(
        company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
        je_id integer not null,
        transaction_date DATE NOT NULL DEFAULT CURRENT_DATE,
        general_ledger_number integer not null,
        cc_id char(6) references cost_centres(cc_id), 
        wbs_code char(5) references wbs(wbs_code),
        currency_id integer references currencies not null,
        debit_credit varchar(6) check(debit_credit in ('debit', 'credit')) NOT NULL,
        amount numeric(12,2),
        CONSTRAINT fk_companyCode
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),
        CONSTRAINT fk_journalentryid
            FOREIGN KEY(je_id) 
	            REFERENCES  journal_entry( je_id),
        CONSTRAINT coasgln
            FOREIGN KEY(general_ledger_number) 
	            REFERENCES  chart_of_accounts(general_ledger_number),
        CONSTRAINT fk_costcentre
            FOREIGN KEY(cc_id) 
	            REFERENCES cost_centres(cc_id),
	    CONSTRAINT fk_wbs
            FOREIGN KEY(wbs_code) 
	            REFERENCES wbs(wbs_code),
	    CONSTRAINT fk_currencyid
            FOREIGN KEY(currency_id) 
	            REFERENCES currencies(currency_id)	
       );

-- sales invoices booked to Financial statements via ar_invoice double entry
create table if not exists ar_invoice(
        company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
        entry_type_id varchar(3) default 'RIE',
        rie_id serial primary key not null,
		date DATE NOT NULL DEFAULT CURRENT_DATE,
		invoice_id integer not null,
        CONSTRAINT fk_companyCode
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),
         CONSTRAINT fk_salesinvoice
      	    FOREIGN KEY(invoice_id) 
	  		    REFERENCES sales_invoices(invoice_id)	
		);


create table if not exists ar_invoice_item(
        company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
        rie_id integer not null,
		description varchar(80),
        customer_id char(6) check (customer_id ~ '[A-Z]{3}[0-9]{3}' ),
        general_ledger_number integer default 102001,
	 	cc_id char(6) references cost_centres(cc_id),
        currency_id integer references currencies not null,
        debit_credit varchar(6) default 'debit',
        amount numeric(12,2),
        CONSTRAINT fk_companyCode
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),	    
         CONSTRAINT fk_arinvoice
      	    FOREIGN KEY(rie_id) 
	  		    REFERENCES ar_invoice(rie_id),
         CONSTRAINT fk_coano
      	    FOREIGN KEY(general_ledger_number) 
	  		    REFERENCES chart_of_accounts(general_ledger_number),
	     CONSTRAINT fk_customer
          	FOREIGN KEY(customer_id) 
	      		REFERENCES customer_names(customer_id),	  	
	     CONSTRAINT fk_currencyid
            FOREIGN KEY(currency_id) 
	            REFERENCES currencies(currency_id),
		 CONSTRAINT fk_costcentre
		   FOREIGN KEY(cc_id) 
			REFERENCES cost_centres(cc_id)	
       );
	   

create table if not exists ar_receipt(
        company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
        entry_type_id varchar(3) default 'RRE',
        rre_id serial primary key not null,
		date DATE NOT NULL DEFAULT CURRENT_DATE,		
		rie_id integer not null,
		customer_id char(6) check (customer_id ~ '[A-Z]{3}[0-9]{3}' ),
        CONSTRAINT fk_companyCode	
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),
	     CONSTRAINT fk_customer
          	FOREIGN KEY(customer_id) 
	      		REFERENCES customer_names(customer_id),	  		    
        CONSTRAINT fk_arinvoice
      	    FOREIGN KEY(rie_id) 
	  		    REFERENCES ar_invoice(rie_id)	
   );

create table if not exists ar_receipt_item(
        company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
        rre_id integer references ar_receipt(rre_id) not null,
        general_ledger_number integer default 102001,
        currency_id integer references currencies not null,
        debit_credit varchar(6) default 'credit' NOT NULL,
        amount numeric(12,2),
        CONSTRAINT fk_companyCode
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),
        CONSTRAINT fk_arreceipt
      	    FOREIGN KEY(rre_id) 
	  		    REFERENCES ar_receipt(rre_id),
         CONSTRAINT fk_coano
      	    FOREIGN KEY(general_ledger_number) 
	  		    REFERENCES chart_of_accounts(general_ledger_number),
	    CONSTRAINT fk_currencyid
            FOREIGN KEY(currency_id) 
	            REFERENCES currencies(currency_id)        
     );

create table if not exists ap_invoice(
        company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
        entry_type_id varchar(3) default 'PIE',
	    pie_id serial primary key not null,
        vendor_id char(5) check (vendor_id ~ '[A-Z]{2}[0-9]{3}' ) not null,
		date DATE NOT NULL DEFAULT CURRENT_DATE,
        p_order_id integer references purchase_orders(p_order_id),
        invoice_id varchar(10) not null,
        CONSTRAINT fk_companyCode
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),
	    CONSTRAINT fk_po
            FOREIGN KEY(p_order_id) 
	            REFERENCES purchase_orders(p_order_id),
	    CONSTRAINT fk_vendor
          FOREIGN KEY(vendor_id) 
	      REFERENCES vendors(vendor_id)
	);
		
create table if not exists ap_invoice_item(
        company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
		PIE_id integer not null,
	 	cc_id char(6) references cost_centres(cc_id),
		wbs_code char(5) references wbs(wbs_code),
        currency_id integer references currencies not null,
        general_ledger_number integer default 200001,
       	debit_credit varchar(6) default 'credit' NOT NULL,
        amount numeric(12,2),
        CONSTRAINT fk_companyCode
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),
        CONSTRAINT fk_apinvoice
      	    FOREIGN KEY(pie_id) 
	  		    REFERENCES ap_invoice(pie_id),	
		 CONSTRAINT fk_costcentre
		   FOREIGN KEY(cc_id) 
			REFERENCES cost_centres(cc_id),
	    CONSTRAINT fk_wbs
            FOREIGN KEY(wbs_code) 
	            REFERENCES wbs(wbs_code),
         CONSTRAINT fk_coano
      	    FOREIGN KEY(general_ledger_number) 
	  		    REFERENCES chart_of_accounts(general_ledger_number),	
	    CONSTRAINT fk_currencyid
            FOREIGN KEY(currency_id) 
	            REFERENCES currencies(currency_id)
      );

create table if not exists ap_payment(
		company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
        entry_type_id varchar(3) default 'PPE',
		ppe_id serial primary key,
		date DATE NOT NULL DEFAULT CURRENT_DATE,
		PIE_id integer not null,
        vendor_id char(5) check (vendor_id ~ '[A-Z]{2}[0-9]{3}' ) not null,
        CONSTRAINT fk_companyCode
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),
	    CONSTRAINT fk_vendor
          FOREIGN KEY(vendor_id) 
	      REFERENCES vendors(vendor_id),	  		    
	    CONSTRAINT fk_apinvoice
            FOREIGN KEY(pie_id) 
	            REFERENCES ap_invoice(pie_id)   
	);
	
	
create table if not exists ap_payment_item(
		company_code char(5) check (company_code ~ '[A-Z]{2}[0-9]{3}' ) not null,
		ppe_id integer not null,
        general_ledger_number integer default 200001,
        currency_id integer references currencies not null,
        debit_credit varchar(6) default 'debit' NOT NULL,
        amount numeric(12,2),
        CONSTRAINT fk_companyCode
      	    FOREIGN KEY(company_code) 
	  		    REFERENCES companies(company_code),
         CONSTRAINT fk_coano
      	    FOREIGN KEY(general_ledger_number) 
	  		    REFERENCES chart_of_accounts(general_ledger_number),
	    CONSTRAINT fk_appayment
            FOREIGN KEY(ppe_id) 
	            REFERENCES ap_payment(ppe_id)       
        );
                        
/*
-- Create conceptual values.

insert into companies(company_code, company_name)
                values
                  ('US001', 'OceanStream_US');

				  
insert into coa_categories(coacat_id,coa_category_name)
    values(1,'assets'),
	(2,'liabilities'),
	(3,'equity'),
	(5,'revenue'),
	(6,'expenses');

insert into currencies(company_code, currency_name, description, functional_currency)
 	values('US001','USD', 'American_dollar', 'Yes'),
	       ('US001','CNY', 'Chinese_Yuan', 'No');	   

insert into tax(company_code,tax_name, tax_rate, tax_area, tax_belongto,description)
   values('US001','sales_tax', 0.10, 'US_Seattle','state','pec_of_sales');	  

insert into chart_of_accounts(company_code, general_ledger_number, general_ledger_name,
							  coacat_id, currency_id)
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

insert into product_categories(company_code, cat_name,subcat_id,subcat_name)
 	values('US001','hard_ware',1,'server'),
	       ('US001','hard_ware',1,'computer'),
		   ('US001','soft_ware',2,'one_off_payement'),
            ('US001','soft_ware', 2,'annual_subscribe'),
            ('US001','consulting', 1, 'one_off_payment');

insert into business_type(business_type_name)
	values('organization'),
			('individual');
			
insert into customer_names (company_code, customer_id, business_type_id,customer_name, currency_id)
	values('US001', 'ABC001', 1,'customer_abc',1);

insert into vendors (company_code, vendor_id,vendor_name, currency_id)
	values('US001', 'BC001','vendor_vbc',1);  

insert into products(company_code, cat_id, 
					 product_name, product_unit_name, product_units, product_unit_price, currency_id)
		  values('US001', 1, 'server', 'piece',1, 250000,1),
                ('US001', 2, 'vizwise','piece', 1, 3000000,1),
                ('US001', 2, 'vizwise_online', 'per_user_per_year',1, 1500,1),
                ('US001', 2, 'smarteroffice_online', 'per_user_per_year',1, 100,1),
                ('US001', 2, 'smarteroffice', 'piece',1, 1200,1),
                ('US001',3, 'consulting', 'hourly',1, 500, 1);
		 
insert into profit_centres(company_code, pc_id,pc_name)
  values('US001', 'HSE001', 'hard_ware_server_SE'),
  		('US001', 'SSE001', 'vizwise_SE'),
		('US001', 'SSE002', 'vizwise_online_annual_SE'),
		('US001', 'SSE003', 'vizwise_online_monthly_SE'),
		('US001', 'SSE004', 'smarteroffice_SE'),
		('US001', 'SSE005', 'smarteroffice_online_SE'),
		('US001', 'CSE001', 'consulting'),
		('US001', 'RDS001','research_development_sl');
  
insert into cost_centres(company_code, cc_id, name, pc_id)
  values('US001', 'HSE01','server_SE', 'HSE001'),
  		('US001', 'SSE01', 'vizwise_SE', 'SSE001'),
		('US001', 'SSE02', 'vizwise_online_annual_SE', 'SSE002'),
		('US001', 'SSE03', 'vizwise_online_monthly_SE', 'SSE003');
  

insert into wbs(company_code,wbs_code, name, pc_id)
  values('US001', 'SL001','Slingshot', 'RDS001');
  
insert into entry_type(entry_type_name, description)
    values('journal_entry', 'entries for general ledger'),
           ('ar_invoice', 'invoices issued to customers'),
            ('ar_receipt', 'fund received from customers'),
           ('ap_invoice', 'invoices received from vendors'),
            ('ap_payment', 'fund payment to vendors');

insert into general_ledger(company_code)
        values('US001');


*/

/*
 insert into purchase_orders(company_code, vendor_id)
 values('US001','VBC001');
 

insert into sales_orders(company_code, customer_id)
   values('US001','ABC001');



insert into sales_orders_items(company_code, sales_order_id,
							  product_id,units,unit_selling_price, currency_id,tax_code,shipped)
	values('US001',1,1,1,520000,1,1,True);



insert into sales_invoices(company_code, sales_order_id, cc_id)
	values('US001',1,'SE0001');
*/


