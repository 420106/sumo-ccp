import os


'''
    App
'''
basdir = os.environ.get('BASEDIR') \
or 'C:\\Users\\sliu\\Documents\\GitHub\\sumo-ccp\\' # local dev repo

# Reference files
xml_checklist = f'{basdir}scripts\\ref_data\\xml_checklist.csv'
report_template = f'{basdir}scripts\\ref_data\\report_template.csv'

'''
    Files
'''
files = f'{basdir}files\\'
# XMLs
xmls = f'{files}xmls\\'
invoice = f'{xmls}invoice\\' # Invoice; Final Invoice; Reminder Notice; Final Notice (Disconnection Notice)
welcome_pack = f'{xmls}welcome_pack\\' # Welcome Pack; Contract Novation
transfer_letter = f'{xmls}transfer_letter\\' # Transfer Letter
payment_plan = f'{xmls}payment_plan\\' # Payment Plan
# PDFs
pdfs = f'{files}pdfs\\'
# Logs
download_logs = f'{files}logs\\download\\'
upload_logs = f'{files}logs\\upload\\'
# Reports
reports = f'{files}reports\\'
