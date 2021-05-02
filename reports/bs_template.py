import os
import datetime
import csv

# write balance sheet template
   
def blank_bs(end_date):
    
    with open(os.path.join('in_progress', f'bs_template.csv'), 'w') as bbs:
        # Equation: Assets = shareholder's equity + Liabilities
        # Head part of balance sheet
        name = 'Ocean Stream' 
        bbs_writer = csv.writer(bbs)   
        bbs_writer.writerow([f'{name}','', ''])
        bbs_writer.writerow(['Balance Sheet', '', ''])
        bbs_writer.writerow(['USD $', '', ''])
        bbs_writer.writerow(['','','',f'as of {end_date}'.rjust(15)])  
        
        # Body of balance sheet
        # Assets    
        bbs_writer.writerow(['Assets','',''])
        bbs_writer.writerow(['','Current assets',''])
        bbs_writer.writerow(['','','Cash and cash equivalent'])
        bbs_writer.writerow(['','','Inventory'])
        bbs_writer.writerow(['','','Account receivables'])
        bbs_writer.writerow(['','','Prepaid expenses',''])        
        bbs_writer.writerow(['','','',''])        
        bbs_writer.writerow(['', 'Total current assets',''])
        bbs_writer.writerow(['','','',''])
        bbs_writer.writerow(['','','Property and Equipment'])
        bbs_writer.writerow(['', '', '- Accumulated depreciation'])
        bbs_writer.writerow(['','','Other assets'])        
        bbs_writer.writerow(['Total Assets','',''])
        bbs_writer.writerow(['','','',''])
        # Liabilities
        bbs_writer.writerow(['Liabilities','',''])
        bbs_writer.writerow(['','Current liabilities',''])
        bbs_writer.writerow(['','','Account payables'])
        bbs_writer.writerow(['','','Tax payable'])        
        bbs_writer.writerow(['','','Accrued expenses'])
        bbs_writer.writerow(['','','Unearned revenue'])       
        bbs_writer.writerow(['','Total current liabilities',''])
        bbs_writer.writerow(['','','',''])
        bbs_writer.writerow(['Total Liabilities','','',])
        bbs_writer.writerow(['','','',''])
        # shareholders equity
        bbs_writer.writerow(['Shareholder\'s Equity','','']) 
        bbs_writer.writerow(['','','Tax payable']) 
        bbs_writer.writerow(['','','Retained Earnings'])
        bbs_writer.writerow(['Total Shareholder\'s Equity','',''])
        bbs_writer.writerow(['','','',''])
        bbs_writer.writerow(['Total Liabilities & Total Shareholder\'s Equity','',''])     
 
        print('blank balance sheet csv done writing')
        
if __name__ == '__main__':
    end_date = datetime.date(2021,3,31)
    blank_bs(end_date)
