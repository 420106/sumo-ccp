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
df = pd.read_csv(paths.report_template, index_col = ['Jurisdiction', 'Type'])
xmls = paths.xmls

d = {'doc_type':{'Invoice': 'Invoice',
                 'Final Invoice': 'Invoice', # Final Invoice grouped into normal Invoice
                 'Reminder Notice': 'Reminder Notice',
                 'Final Notice': 'Disconnection Notice', # Final Notice commonly referred to as Disconnection Notice
                 'WelcomePack': 'Welcome Pack',
                 'ContractNovation': 'Contract Novation',
                 'TransferLetter': 'Transfer Letter',
                 'PaymentPlan': 'Payment Plan'},
     'juri': {'VIC': 'VIC', 'NSW': 'NSW'},
     'dis_meth': {'Email': 'Email', 'Print': 'Print'}}

print('Sorting XML data...')
for file in os.listdir(xmls):
    if file.endswith('.xml') & (len(file) == 39):
        tree = ET.parse(xmls + file)
        root = tree.getroot()
        for cus in root.findall('Customer'):
            # common tree structure:
            # <DocumentType> and <DistributionMethod> under <Batch><Customer>
            # <Jurisdiction> under <Batch><Customer><Whatever the DocumentType Is>
            # but the convention is not followed by all types
            dis_meth = cus.find('DistributionMethod').text
            doc_type = cus.find('DocumentType').text
            if doc_type == 'Invoice':
                # Invoice, Final Invoice, Reminder Notice, Final Notice
                # <DocumentType> = Invoice; <InvoiceType> differs
                doc_type = cus.find('Invoices/Invoice/InvoiceType').text
                juri = cus.find('Invoices/Invoice/Jurisdiction').text
            elif doc_type == 'ContractNovation':
                # Contract Novation
                # Contract Novation is mixed in the same batch file with Welcome Pack
                juri = cus.find('WelcomePack/Jurisdiction').text
            elif doc_type == 'PaymentPlan':
                # Payment Plan
                juri = cus.find('PaymentPlanDetails/Jurisdiction').text
            else:
                juri = cus.find(f'{doc_type}/Jurisdiction').text
            df.loc[(d['juri'][juri], d['doc_type'][doc_type]),
                   d['dis_meth'][dis_meth]] += 1

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
    df.to_csv(f'{reports}ccp_report_{date}_{i + 1}.csv')
else:
    df.to_csv(f'{reports}ccp_report_{date}_1.csv')

print('Report saved.')
