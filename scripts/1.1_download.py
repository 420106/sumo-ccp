import os
import importlib.util
from datetime import datetime

# ---------------------------------------------------------------------------------------------------------
root = 'C:\\Users\\sliu\\Documents\\GitHub\\sumo-ccp\\'
os.chdir(root)

modules = 'scripts\\modules\\'

spec = importlib.util.spec_from_file_location('paths', f'{modules}paths.py')
paths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paths)

spec = importlib.util.spec_from_file_location('connections', f'{modules}connections.py')
connections = importlib.util.module_from_spec(spec)
spec.loader.exec_module(connections)
# ---------------------------------------------------------------------------------------------------------

logs = paths.download_logs

try:
    last_log = os.listdir(logs)[-1]
except IndexError:
    # To prevent IndexError if the folder is empty
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
        if (file.endswith('.xml')) & (len(file) == 39) & (file not in checklist):
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
