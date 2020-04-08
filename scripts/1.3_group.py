import os
import importlib.util
import shutil
import xml.etree.ElementTree as ET

# ---------------------------------------------------------------------------------------------------------
# root = 'C:\\Users\\sliu\\Documents\\GitHub\\sumo-ccp\\' # Local dev repo
root = 'C:\\Apps\\sumo-ccp\\' # Server repo
os.chdir(root)

modules = 'scripts\\modules\\'

spec = importlib.util.spec_from_file_location('paths', f'{modules}paths.py')
paths = importlib.util.module_from_spec(spec)
spec.loader.exec_module(paths)
# ---------------------------------------------------------------------------------------------------------

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

# # Notify us when there is any XML remaining ungrouped
# notify = False
# for file in os.listdir(src):
#     if file.endswith('.xml'):
#         notify = True
#         break
#
# if notify:
#     '''Send an email'''
# else:
#     print('No XML remains ungrouped..')
