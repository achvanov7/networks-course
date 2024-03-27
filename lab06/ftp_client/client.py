from ftplib import FTP
import argparse

def ls(ftp_server : FTP, dir):
  ftp_server.cwd(dir)
  print(ftp_server.nlst())

def upload(ftp_server : FTP, dir, remote, local):
  ftp_server.cwd(dir)
  with open(local, 'rb') as file:
    ftp_server.storbinary('STOR ' + remote, file)

def download(ftp_server : FTP, dir, remote, local):
  ftp_server.cwd(dir)
  with open(local, 'wb') as file:
    ftp_server.retrbinary('RETR ' + remote, file.write)

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', type = str, default = 'ftp.dlptest.com')
parser.add_argument('-un', '--username', type = str, default = 'dlpuser')
parser.add_argument('-p', '--password', type = str, default = 'rNrKYTX9g7z3RgJRmxWuGHbeu')
parser.add_argument('-c', '--cmd', type = str)
parser.add_argument('-d', '--dir', type = str, default = '')
parser.add_argument('-r', '--remote', type = str, default = '')
parser.add_argument('-l', '--local', type = str, default = '')
args = parser.parse_args()

try:
  ftp_server = FTP(args.url)
  ftp_server.login(args.username, args.password)
except:
  print('Oops, something went wrong')
  exit(1)

try:
  if args.cmd == 'ls':
    ls(ftp_server, args.dir)
  elif args.cmd == 'upload':
    upload(ftp_server, args.dir, args.remote, args.local)
  elif args.cmd == 'download':
    download(ftp_server, args.dir, args.remote, args.local)
  else:
    print('Command is not supported')
except:
  print('Oops, something went wrong')
  exit(1)

ftp_server.quit()
