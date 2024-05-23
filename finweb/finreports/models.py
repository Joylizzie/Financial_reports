# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApInvoice(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    entry_type_id = models.CharField(max_length=3, blank=True, null=True)
    pie_id = models.AutoField(primary_key=True)
    vendor = models.ForeignKey('Vendors', on_delete=models.CASCADE)
    date = models.DateField()
    p_order = models.ForeignKey('PurchaseOrders', on_delete=models.CASCADE, blank=True, null=True)
    invoice_id = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'ap_invoice'


class ApInvoiceItem(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    pie = models.ForeignKey(ApInvoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=80, blank=True, null=True)
    general_ledger_number = models.ForeignKey('ChartOfAccounts', on_delete=models.CASCADE, db_column='general_ledger_number', blank=True, null=True)
    cc = models.ForeignKey('CostCentres', on_delete=models.CASCADE, blank=True, null=True)
    wbs_code = models.ForeignKey('Wbs', on_delete=models.CASCADE, db_column='wbs_code', blank=True, null=True)
    currency = models.ForeignKey('Currencies', on_delete=models.CASCADE)
    debit_credit = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ap_invoice_item'


class ApPayment(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    entry_type_id = models.CharField(max_length=3, blank=True, null=True)
    ppe_id = models.AutoField(primary_key=True)
    date = models.DateField()
    pie = models.ForeignKey(ApInvoice, on_delete=models.CASCADE)
    vendor = models.ForeignKey('Vendors', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'ap_payment'


class ApPaymentItem(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    ppe = models.ForeignKey(ApPayment, on_delete=models.CASCADE)
    description = models.CharField(max_length=80, blank=True, null=True)
    general_ledger_number = models.ForeignKey('ChartOfAccounts', on_delete=models.CASCADE, db_column='general_ledger_number', blank=True, null=True)
    currency = models.ForeignKey('Currencies', on_delete=models.CASCADE)
    debit_credit = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ap_payment_item'


class ArInvoice(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    entry_type_id = models.CharField(max_length=3, blank=True, null=True)
    rie_id = models.AutoField(primary_key=True)
    date = models.DateField()
    invoice = models.ForeignKey('SalesInvoices', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'ar_invoice'


class ArInvoiceItem(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    rie = models.ForeignKey(ArInvoice, on_delete=models.CASCADE)
    description = models.CharField(max_length=80, blank=True, null=True)
    customer = models.ForeignKey('CustomerNames', on_delete=models.CASCADE, blank=True, null=True)
    general_ledger_number = models.ForeignKey('ChartOfAccounts', on_delete=models.CASCADE, db_column='general_ledger_number', blank=True, null=True)
    cc = models.ForeignKey('CostCentres', on_delete=models.CASCADE, blank=True, null=True)
    currency = models.ForeignKey('Currencies', on_delete=models.CASCADE)
    debit_credit = models.CharField(max_length=6, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_invoice_item'


class ArReceipt(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    entry_type_id = models.CharField(max_length=3, blank=True, null=True)
    rre_id = models.AutoField(primary_key=True)
    date = models.DateField()
    rie = models.ForeignKey(ArInvoice, on_delete=models.CASCADE)
    customer = models.ForeignKey('CustomerNames', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_receipt'


class ArReceiptItem(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    rre = models.ForeignKey(ArReceipt, on_delete=models.CASCADE)
    description = models.CharField(max_length=80, blank=True, null=True)
    general_ledger_number = models.ForeignKey('ChartOfAccounts', on_delete=models.CASCADE, db_column='general_ledger_number', blank=True, null=True)
    currency = models.ForeignKey('Currencies', on_delete=models.CASCADE)
    debit_credit = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ar_receipt_item'


class AreaCode(models.Model):
    zip = models.CharField(max_length=10)
    zipcode_name = models.CharField(max_length=30, blank=True, null=True)
    city = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    county_name = models.CharField(max_length=40, blank=True, null=True)
    area = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'area_code'


class BsPlIdx(models.Model):
    bs_pl_index = models.IntegerField(primary_key=True)
    bs_pl_cat_name = models.CharField(max_length=40, blank=True, null=True)
    coacat = models.ForeignKey('CoaCategories', on_delete=models.CASCADE)
    sub_coacat = models.ForeignKey('SubCoaCategories', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'bs_pl_idx'


class BusinessType(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    business_type_id = models.AutoField(primary_key=True)
    business_type_name = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'business_type'


class ChartOfAccounts(models.Model):
    company_code = models.ForeignKey('Companies', on_delete=models.CASCADE, db_column='company_code')
    general_ledger_number = models.IntegerField(unique=True)
    general_ledger_name = models.CharField(unique=True, max_length=30)
    coacat = models.ForeignKey('CoaCategories', on_delete=models.CASCADE)
    sub_coacat = models.ForeignKey('SubCoaCategories', on_delete=models.CASCADE)
    bs_pl_index = models.ForeignKey(BsPlIdx, on_delete=models.CASCADE, db_column='bs_pl_index')
    currency = models.ForeignKey('Currencies', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chart_of_accounts'


class CoaCategories(models.Model):
    coacat_id = models.IntegerField(primary_key=True)
    coa_category_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'coa_categories'


class Companies(models.Model):
    company_code = models.CharField(primary_key=True, max_length=5)
    company_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'companies'


class CostCentres(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    cc_id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=30)
    pc = models.ForeignKey('ProfitCentres', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cost_centres'


class Currencies(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    currency_id = models.AutoField(primary_key=True)
    currency_name = models.CharField(max_length=3)
    description = models.CharField(max_length=20, blank=True, null=True)
    functional_currency = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'currencies'


class CustomerAddresses(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    customer = models.ForeignKey('CustomerNames', on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=250)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.CharField(max_length=60, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_addresses'


class CustomerNames(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    customer_id = models.CharField(primary_key=True, max_length=6)
    business_type_id = models.IntegerField()
    customer_name = models.CharField(max_length=250, blank=True, null=True)
    general_ledger_number = models.IntegerField(blank=True, null=True)
    currency_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'customer_names'


class EmployeeCostCentres(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    employee = models.OneToOneField('EmployeeNames', on_delete=models.CASCADE, primary_key=True)
    cc = models.ForeignKey(CostCentres, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_cost_centres'


class EmployeeNames(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    employee_id = models.CharField(primary_key=True, max_length=5)
    employee_name = models.CharField(max_length=50)
    grade_code = models.ForeignKey('Grades', on_delete=models.CASCADE, db_column='grade_code')

    class Meta:
        managed = False
        db_table = 'employee_names'


class EmployeeSalaries(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    employee = models.OneToOneField(EmployeeNames, on_delete=models.CASCADE, primary_key=True)
    grade_code = models.ForeignKey('Grades', on_delete=models.CASCADE, db_column='grade_code')
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employee_salaries'


class EntryType(models.Model):
    entry_type_id = models.CharField(primary_key=True, max_length=3)
    entry_type_name = models.CharField(max_length=20)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entry_type'


class FiscalMonths(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    start_date = models.DateField(unique=True)
    end_date = models.DateField(unique=True)

    class Meta:
        managed = False
        db_table = 'fiscal_months'


class Grades(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    grade_code = models.IntegerField(primary_key=True)
    grade_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'grades'


class JournalEntry(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    entry_type = models.ForeignKey(EntryType, on_delete=models.CASCADE, blank=True, null=True)
    je_id = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'journal_entry'


class JournalEntryItem(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    je = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    description = models.CharField(max_length=80, blank=True, null=True)
    general_ledger_number = models.ForeignKey(ChartOfAccounts, on_delete=models.CASCADE, db_column='general_ledger_number')
    cc = models.ForeignKey(CostCentres, on_delete=models.CASCADE, blank=True, null=True)
    wbs_code = models.ForeignKey('Wbs', on_delete=models.CASCADE, db_column='wbs_code', blank=True, null=True)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    debit_credit = models.CharField(max_length=6)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'journal_entry_item'


class ProductCategories(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    cat_id = models.CharField(primary_key=True, max_length=1)
    cat_name = models.CharField(max_length=20)
    subcat_id = models.IntegerField(blank=True, null=True)
    subcat_name = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_categories'


class Products(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    product_id = models.AutoField(primary_key=True)
    cat = models.ForeignKey(ProductCategories, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=60)
    product_unit_name = models.CharField(max_length=30, blank=True, null=True)
    product_units = models.IntegerField(blank=True, null=True)
    product_unit_price = models.DecimalField(max_digits=65535, decimal_places=65535)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'products'


class ProfitCentres(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    pc_id = models.CharField(primary_key=True, max_length=6)
    pc_name = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'profit_centres'


class PurchaseOrders(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    p_order_id = models.AutoField(primary_key=True)
    p_order_date = models.DateField()
    vendor = models.ForeignKey('Vendors', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'purchase_orders'


class PurchaseOrdersItems(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    p_order = models.ForeignKey(PurchaseOrders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, blank=True, null=True)
    # item_id = models.AutoField()
    cc = models.ForeignKey(CostCentres, on_delete=models.CASCADE, blank=True, null=True)
    general_ledger_number = models.IntegerField(blank=True, null=True)
    wbs_code = models.ForeignKey('Wbs', on_delete=models.CASCADE, db_column='wbs_code', blank=True, null=True)
    tax_code = models.ForeignKey('Tax', on_delete=models.CASCADE, db_column='tax_code')

    class Meta:
        managed = False
        db_table = 'purchase_orders_items'


class SalesInvoices(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    invoice_date = models.DateField()
    invoice_id = models.AutoField(primary_key=True)
    sales_order = models.ForeignKey('SalesOrders', on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerNames, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sales_invoices'


class SalesOrders(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    sales_order_id = models.AutoField(primary_key=True)
    s_order_date = models.DateField()
    customer = models.ForeignKey(CustomerNames, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'sales_orders'


class SalesOrdersItems(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    sales_order = models.ForeignKey(SalesOrders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    unit_name = models.CharField(max_length=6, blank=True, null=True)
    units = models.IntegerField(blank=True, null=True)
    unit_selling_price = models.DecimalField(max_digits=65535, decimal_places=65535)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)
    tax_code = models.ForeignKey('Tax', on_delete=models.CASCADE, db_column='tax_code')
    shipped = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'sales_orders_items'


class SubCoaCategories(models.Model):
    sub_coacat_id = models.AutoField(primary_key=True)
    sub_coacat_name = models.CharField(max_length=40, blank=True, null=True)
    coacat = models.ForeignKey(CoaCategories, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'sub_coa_categories'


class Tax(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    tax_code = models.AutoField(primary_key=True)
    tax_name = models.CharField(unique=True, max_length=15, blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=4, decimal_places=4)
    tax_area = models.CharField(max_length=20)
    tax_belongto = models.CharField(max_length=15, blank=True, null=True)
    description = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tax'


class VendorAddresses(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    vendor = models.ForeignKey('Vendors', on_delete=models.CASCADE)
    address_line1 = models.CharField(max_length=250)
    address_line2 = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email_address = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vendor_addresses'


class Vendors(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    vendor_id = models.CharField(primary_key=True, max_length=5)
    vendor_name = models.CharField(max_length=60)
    general_ledger_number = models.IntegerField(blank=True, null=True)
    currency = models.ForeignKey(Currencies, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'vendors'


class Wbs(models.Model):
    company_code = models.ForeignKey(Companies, on_delete=models.CASCADE, db_column='company_code')
    wbs_code = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=20, blank=True, null=True)
    pc = models.ForeignKey(ProfitCentres, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wbs'
