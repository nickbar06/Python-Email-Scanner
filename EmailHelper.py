from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from auth import authenticate
from helpers import run_script
from appleScripts import read_emails

# Email account credentials
sender = "nick@midnightinshibuya.com"

def send_email(to_address):
    msg = MIMEMultipart()
    msg.set_unixfrom('author')
    msg['From'] = sender
    msg['To'] = to_address

    msg['Subject'] = 'Test 1'
    message = 'OHHOOO'

    msg.attach(MIMEText(message))

    mailserver = authenticate()
    mailserver.sendmail(sender, to_address, msg.as_string())
    mailserver.quit()

def read_email():
    inbox = run_script(read_emails)
    print(inbox)

read_email()
print("hooray")