import os
from ftplib import FTP


def brave_ftp():
    '''
        Sumo FTP to receive Brave XMLs
    '''
    host = 'ftp.sumo.com.au'
    usr = os.environ.get('BRAVE_USR')
    pwd = os.environ.get('BRAVE_PWD')
    dir = '//Sales Collateral//'

    ftp = FTP(host)
    ftp.login(usr, pwd)
    ftp.cwd(dir)
    print('Brave FTP connected\nDirectory: {}'.format(dir))
    return ftp

def bluestar_ftp():
    '''
        BlueStar FTP to upload PDFs
    '''
    host = 'ftp.securitymail.com.au'
    usr = os.environ.get('BLUESTAR_USR')
    pwd = os.environ.get('BLUESTAR_PWD')
    dir = '/incoming'

    host = 'ftp.sumo.com.au' # Test
    usr = os.environ.get('BRAVE_USR') # Test
    pwd = os.environ.get('BRAVE_PWD') # Test
    dir = '//test folder//' # Test

    ftp = FTP(host)
    ftp.login(usr, pwd)
    ftp.cwd(dir)
    print('BlueStar FTP connected\nDirectory: {}'.format(dir))
    return ftp
