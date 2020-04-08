import os

# ---------------------------------------------------------------------------------------------------------
'''
    Local
'''
root = 'C:\\Users\\sliu\\Documents\\GitHub\\sumo-ccp\\' # Local dev repository

# Reference files
xml_checklist = f'{root}scripts\\ref\\xml_checklist.csv'
report_template = f'{root}scripts\\ref\\report_template.csv'
# ---------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------
'''
    Cloud
'''
files = 'C:\\Users\\sliu\\Documents\\GitHub\\sumo-ccp\\files\\' # Test path

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
# ---------------------------------------------------------------------------------------------------------
