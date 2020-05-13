import importlib.util
import os
from datetime import datetime


root = os.environ.get('ROOT') \
or 'C:\\Users\\sliu\\Documents\\GitHub\\sumo-ccp\\' # local dev repo

os.chdir(root)
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
    upload()

def upload():
    '''
        To upload PDFs to BlueStar
    '''
    logs = paths.upload_logs
    try:
        last_log = os.listdir(logs)[-1]
    except IndexError:
        # To prevent IndexError if the folder is empty
        last_log = ' ' * 20
    date = datetime.today().strftime('%Y%m%d')
    if last_log[6:14] == date:
        i = int(last_log[15:-4])
        log = open(f'{logs}log_u_{date}_{i + 1}.txt', 'w+')
    else:
        log = open(f'{logs}log_u_{date}_1.txt', 'w+')
    try:
        log.write(f'Date: {date}\n')
        log.write('--------------------------------------------------\n')
        print('Connecting to BlueStar FTP...')
        log.write(f'{datetime.now().strftime("[%H:%M:%S]")} Connecting to Brave FTP...\n')
        # ftp = connections.bluestar_ftp() # replaced with SFTP
        sftp = connections.bluestar_sftp()
        src = paths.pdfs
        summary = []
        log.write('--------------------------------------------------\n')
        for file in os.listdir(src):
            if file.endswith('.pdf') and len(file) == 47:
                print(f'Uploading {file}...')
                log.write(f'{datetime.now().strftime("[%H:%M:%S]")} Uploding {file}...\n')
                summary.append(file[:2])
                # with open(src + file, 'rb') as f: # replaced with SFTP
                #     ftp.storbinary(f'STOR {file}', f)
                #     f.close()
                sftp.put(src + file, file, confirm = False)
                os.remove(src + file)
        # ftp.close() # replaced with SFTP
        sftp.close()
        log.write('--------------------------------------------------\n')
        print('Summarizing...')
        d = {'IN': 'Invoice',
             'RE': 'Reminder Notice',
             'FI': 'Disconnection Notice',
             'WP': 'Welcome Pack',
             'CN': 'Contract Novation',
             'TR': 'Transfer Letter',
             'PP': 'Payment Plan', 'DD': 'Direct Debit Letter'}
        for k, v in d.items():
            log.write(f'{v}: {summary.count(k)}\n')
        log.write('--------------------------------------------------\n')
        print(f'Total: {len(summary)}')
        log.write(f'Total {len(summary)}\n')
    except Exception as e:
        print(f'Error: {e}')
        log.write(f'{datetime.now().strftime("[%H:%M:%S]")} Error: {e}\n')
    finally:
        log.close()

if __name__ == '__main__':
    main()
