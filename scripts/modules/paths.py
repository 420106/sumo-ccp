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
s3 = 'C:\\Users\\sliu\\Documents\\GitHub\\sumo-ccp\\test\\' # Test path

# XMLs
xmls = f'{s3}xmls\\'
invoice = f'{xmls}invoice\\' # Invoice; Final Invoice; Reminder Notice; Final Notice (Disconnection Notice)
welcome_pack = f'{xmls}welcome_pack\\' # Welcome Pack; Contract Novation
transfer_letter = f'{xmls}transfer_letter\\' # Transfer Letter
payment_plan = f'{xmls}payment_plan\\' # Payment Plan

# PDFs
pdfs = f'{s3}pdfs\\'

# Logs
download_logs = f'{s3}logs\\download\\'
upload_logs = f'{s3}logs\\upload\\'

# Reports
reports = f'{s3}reports\\'
# ---------------------------------------------------------------------------------------------------------
