import os
import importlib.util
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

# ---------------------------------------------------------------------------------------------------------
root = 'C:\\Users\\sliu\\Documents\\GitHub\\sumo-ccp\\'
os.chdir(root)

modules = 'scripts\\modules\\'

spec = importlib.util.spec_from_file_location('paths', f'{modules}paths.py')
paths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paths)
# ---------------------------------------------------------------------------------------------------------

print('Import report template...')
df = pd.read_csv(paths.report_template, index_col = 'Index')
xmls = paths.xmls

print('Sorting XML data...')
for file in os.listdir(xmls):
    if file.endswith('.xml'):
        tree = ET.parse(xmls + file)
        root = tree.getroot()
        for cus in root.findall('Customer'):
            dis_meth = cus.find('DistributionMethod').text
            doc_type = cus.find('DocumentType').text
            if doc_type == 'Invoice':
                doc_type = cus.find('Invoices/Invoice/InvoiceType').text
                juri = cus.find('Invoices/Invoice/Jurisdiction').text
                # Invoice; Final Invoice
                if (doc_type in ['Invoice', 'Final Invoice']) & (juri == 'VIC') & (dis_meth == 'Email'):
                    df.loc['VIC_IN', 'Email'] += 1
                elif (doc_type in ['Invoice', 'Final Invoice']) & (juri == 'VIC') & (dis_meth == 'Print'):
                    df.loc['VIC_IN', 'Print'] += 1
                elif (doc_type in ['Invoice', 'Final Invoice']) & (juri == 'NSW') & (dis_meth == 'Email'):
                    df.loc['NSW_IN', 'Email'] += 1
                elif (doc_type in ['Invoice', 'Final Invoice']) & (juri == 'NSW') & (dis_meth == 'Print'):
                    df.loc['NSW_IN', 'Print'] += 1
                # Reminder Notice
                elif (doc_type == 'Reminder Notice') & (juri == 'VIC') & (dis_meth == 'Email'):
                    df.loc['VIC_RN', 'Email'] += 1
                elif (doc_type == 'Reminder Notice') & (juri == 'VIC') & (dis_meth == 'Print'):
                    df.loc['VIC_RN', 'Print'] += 1
                elif (doc_type == 'Reminder Notice') & (juri == 'NSW') & (dis_meth == 'Email'):
                    df.loc['NSW_RN', 'Email'] += 1
                elif (doc_type == 'Reminder Notice') & (juri == 'NSW') & (dis_meth == 'Print'):
                    df.loc['NSW_RN', 'Print'] += 1
                # Final Notice (Disconnection Notice)
                elif (doc_type == 'Final Notice') & (juri == 'VIC') & (dis_meth == 'Email'):
                    df.loc['VIC_DN', 'Email'] += 1
                elif (doc_type == 'Final Notice') & (juri == 'VIC') & (dis_meth == 'Print'):
                    df.loc['VIC_DN', 'Print'] += 1
                elif (doc_type == 'Final Notice') & (juri == 'NSW') & (dis_meth == 'Email'):
                    df.loc['NSW_DN', 'Email'] += 1
                elif (doc_type == 'Final Notice') & (juri == 'NSW') & (dis_meth == 'Print'):
                    df.loc['NSW_DN', 'Print'] += 1
            elif doc_type in ['WelcomePack', 'ContractNovation']:
                juri = cus.find('WelcomePack/Jurisdiction').text
                # Welcome Pack
                if (doc_type == 'WelcomePack') & (juri == 'VIC') & (dis_meth == 'Email'):
                    df.loc['VIC_WP', 'Email'] += 1
                elif (doc_type == 'WelcomePack') & (juri == 'VIC') & (dis_meth == 'Print'):
                    df.loc['VIC_WP', 'Print'] += 1
                elif (doc_type == 'WelcomePack') & (juri == 'NSW') & (dis_meth == 'Email'):
                    df.loc['NSW_WP', 'Email'] += 1
                elif (doc_type == 'WelcomePack') & (juri == 'NSW') & (dis_meth == 'Print'):
                    df.loc['NSW_WP', 'Print'] += 1
                # Contract Novation
                elif (doc_type == 'ContractNovation') & (juri == 'VIC') & (dis_meth == 'Email'):
                    df.loc['VIC_CN', 'Email'] += 1
                elif (doc_type == 'ContractNovation') & (juri == 'VIC') & (dis_meth == 'Print'):
                    df.loc['VIC_CN', 'Print'] += 1
                elif (doc_type == 'ContractNovation') & (juri == 'NSW') & (dis_meth == 'Email'):
                    df.loc['NSW_CN', 'Email'] += 1
                elif (doc_type == 'ContractNovation') & (juri == 'NSW') & (dis_meth == 'Print'):
                    df.loc['NSW_CN', 'Print'] += 1
            elif doc_type == 'TransferLetter':
                juri = cus.find('TransferLetter/Jurisdiction').text
                # Transfer Letter
                if (juri == 'VIC') & (dis_meth == 'Email'):
                    df.loc['VIC_TL', 'Email'] += 1
                elif (juri == 'VIC') & (dis_meth == 'Print'):
                    df.loc['VIC_TL', 'Print'] += 1
                elif (juri == 'NSW') & (dis_meth == 'Email'):
                    df.loc['NSW_TL', 'Email'] += 1
                elif (juri == 'NSW') & (dis_meth == 'Print'):
                    df.loc['NSW_TL', 'Print'] += 1
            elif doc_type == 'PaymentPlan':
                juri = cus.find('PaymentPlanDetails/Jurisdiction').text
                # Payment Plan
                if (juri == 'VIC') & (dis_meth == 'Email'):
                    df.loc['VIC_PP', 'Email'] += 1
                elif (juri == 'VIC') & (dis_meth == 'Print'):
                    df.loc['VIC_PP', 'Print'] += 1
                elif (juri == 'NSW') & (dis_meth == 'Email'):
                    df.loc['NSW_PP', 'Email'] += 1
                elif (juri == 'NSW') & (dis_meth == 'Print'):
                    df.loc['NSW_PP', 'Print'] += 1

df['Total'] = df['Print'] + df['Email']

date = datetime.today().strftime('%Y%m%d')

reports = paths.reports
try:
    last_report = os.listdir(reports)[-1]
except IndexError:
    # To prevent IndexError if the folder is empty
    last_report = ' ' * 25

if last_report[11:19] == date:
    i = int(last_report[20:-4])
    df.to_csv(f'{reports}ccp_report_{date}_{i + 1}.csv', index = False)
else:
    df.to_csv(f'{reports}ccp_report_{date}_1.csv', index = False)

print('Report saved.')
