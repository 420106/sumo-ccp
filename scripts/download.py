import os
import importlib.util
import pandas as pd
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime


basdir = os.environ.get('BASEDIR') \
or 'C:\\Users\\sliu\\Documents\\GitHub\\sumo-ccp\\' # local dev repo

os.chdir(basdir)
modules = 'scripts\\modules\\'
# Paths module
spec = importlib.util.spec_from_file_location('paths', f'{modules}paths.py')
paths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paths)
# Connections module
spec = importlib.util.spec_from_file_location('connections', f'{modules}connections.py')
connections = importlib.util.module_from_spec(spec)
spec.loader.exec_module(connections)


def main():
    download()
    report()
    group()

def download():
    '''
        To download new received XMLs from Brave
    '''
    logs = paths.download_logs
    try:
        last_log = os.listdir(logs)[-1]
    except IndexError:
        # to prevent IndexError if the folder is empty
        last_log = ' ' * 20
    date = datetime.today().strftime('%Y%m%d')
    if last_log[6:14] == date:
        i = int(last_log[15:-4])
        log = open(f'{logs}log_d_{date}_{i + 1}.txt', 'w+')
    else:
        log = open(f'{logs}log_d_{date}_1.txt', 'w+')
    try:
        log.write(f'Date: {date}\n')
        log.write('--------------------------------------------------\n')
        print('Connecting to Brave FTP...')
        log.write(f'{datetime.now().strftime("[%H:%M:%S]")} Connecting to Brave FTP...\n')
        ftp = connections.brave_ftp()
        with open(paths.xml_checklist, 'r') as f:
            checklist = f.read().splitlines()
            f.close()
        update = open(paths.xml_checklist, 'a')
        dst = paths.xmls
        c = 0
        log.write('--------------------------------------------------\n')
        for file in ftp.nlst():
            if file.endswith('.xml') and len(file) == 39 and file not in checklist:
                print(f'Downloading {file}...')
                log.write(f'{datetime.now().strftime("[%H:%M:%S]")} Downloading {file}...\n')
                ftp.retrbinary(f'RETR {file}', open(dst + file, 'wb').write)
                update.write(f'{file}\n')
                c += 1
        update.close()
        ftp.close()
        log.write('--------------------------------------------------\n')
        print(f'Total: {c}')
        log.write(f'Total: {c}')
    except Exception as e:
        print(f'Error: {e}')
        log.write(f'{datetime.now().strftime("[%H:%M:%S]")} Error: {e}\n')
    finally:
        log.close()

def report():
    '''
        To create a report, grouping XMLs by jurisdiction, distribution method and document type
    '''
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
        if file.endswith('.xml') and len(file) == 39:
            tree = ET.parse(xmls + file)
            root = tree.getroot()
            for cus in root.findall('Customer'):
                # common tree structure:
                # <DocumentType> and <DistributionMethod> under <Batch><Customer>
                # <Jurisdiction> under <Batch><Customer><Whatever the DocumentType Is>
                # but this convention is not followed by all types
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

def group():
    '''
        To group XMLs into subfolders by <DocumentType>
    '''
    src = paths.xmls
    print('Grouping XMLs into subfolders...')
    try:
        for file in os.listdir(src):
            if file.endswith('.xml'):
                tree = ET.parse(src + file)
                root = tree.getroot()
                doc_type = root.find('Customer/DocumentType').text
                if doc_type == 'Invoice':
                    shutil.move(src + file, paths.invoice + file)
                elif doc_type in ['WelcomePack', 'ContractNovation']:
                    shutil.move(src + file, paths.welcome_pack + file)
                elif doc_type == 'TransferLetter':
                    shutil.move(src + file, paths.transfer_letter + file)
                elif doc_type == 'PaymentPlan':
                    shutil.move(src + file, paths.payment_plan + file)
    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':
    main()
