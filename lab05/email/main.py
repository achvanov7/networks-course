import sys
import email.message
import smtplib
from getpass import getpass

file = sys.argv[1]
recipient = sys.argv[2]
subject = sys.argv[3]

login = input('Login: ')
password = getpass()

msg = email.message.EmailMessage()
msg["From"] = login
msg["To"] = recipient
msg["Subject"] = subject

with open(file) as f:
  data = f.read()

if file.endswith('txt'):
  msg.set_content(data)
elif file.endswith('html'):
  msg.add_alternative(data, 'html')

smpt_server = 'smtp.yandex.ru'
smpt_port = 465
server = smtplib.SMTP_SSL(smpt_server, smpt_port)
server.ehlo()
server.login(login, password)
server.send_message(msg)
server.quit()
