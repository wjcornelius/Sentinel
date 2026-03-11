import smtplib
from email.mime.text import MIMEText
import sys
sys.path.insert(0, '.')
from config import GMAIL_APP_PASSWORD

gmail_addr = 'wjcornelius@gmail.com'

body = r"""ROBOCOPY TRANSFER INSTRUCTIONS
==============================

SHARE ADDRESS (type in File Explorer on LenovoLOQ):
\\LAPTOP-1FV3ILC1\wjcor

The batch file ROBOCOPY_TRANSFER.bat is in that folder.
Right-click it and Run as administrator.

OR open Command Prompt as Administrator on LenovoLOQ and paste this:

robocopy "\\LAPTOP-1FV3ILC1\wjcor" "C:\Users\wjcor" /E /COPYALL /R:1 /W:5 /MT:8 /LOG:C:\transfer_log.txt /TEE

It will skip files already transferred.

- Claude
"""

msg = MIMEText(body, 'plain')
msg['From'] = gmail_addr
msg['To'] = gmail_addr
msg['Subject'] = 'File Transfer Instructions for LenovoLOQ'

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(gmail_addr, GMAIL_APP_PASSWORD)
server.send_message(msg)
server.quit()

print('Email sent successfully!')
