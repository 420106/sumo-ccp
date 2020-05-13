import os
import paramiko
from ftplib import FTP

def main():
    '''
        Test connectivity
    '''
    brave_ftp()
    bluestar_ftp()
    bluestar_sftp()

def brave_ftp():
    '''
        Sumo FTP to receive Brave XMLs
    '''
    host = 'ftp.sumo.com.au'
    usr = os.environ.get('BRAVE_USR')
    pwd = os.environ.get('BRAVE_PWD')
    dir_ = 'Sales Collateral//'

    ftp = FTP(host)
    ftp.login(usr, pwd)
    ftp.cwd(dir_)
    print(f'Brave FTP connected\nDirectory: {dir_}')
    return ftp

def bluestar_ftp():
    '''
        BlueStar FTP to upload PDFs
    '''
    host = 'ftp.securitymail.com.au'
    usr = os.environ.get('BLUESTAR_USR')
    pwd = os.environ.get('BLUESTAR_PWD')
    dir_ = 'incoming//'

    # host = 'ftp.sumo.com.au' # Test
    # usr = os.environ.get('BRAVE_USR') # Test
    # pwd = os.environ.get('BRAVE_PWD') # Test
    # dir = 'test folder//' # Test

    ftp = FTP(host)
    ftp.login(usr, pwd)
    ftp.cwd(dir_)
    print(f'BlueStar FTP connected\nDirectory: {dir_}')
    return ftp

def bluestar_sftp():
    '''
        BlueStar SFTP to upload PDFs
    '''
    host, port = 'ftp.securitymail.com.au', 22
    usr = os.environ.get('BLUESTAR_USR')
    pwd = os.environ.get('BLUESTAR_PWD')
    dir_ = 'incoming//'

    transport = paramiko.Transport((host, port))
    transport.connect(None, usr, pwd)
    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.chdir(dir_)
    print(f'BlueStar SFTP connected\nDirectory: {dir_}')
    return sftp

if __name__ == '__main__':
    main()
