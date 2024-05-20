from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from auth import authenticate
from helpers import run_script
from appleScripts import read_emails
from ChatGPT import send_message_to_gpt
from Objects import EmailNode
import re

# Email account credentials
sender = "nick@midnightinshibuya.com"


def send_email(to_address):
    msg = MIMEMultipart()
    msg.set_unixfrom('author')
    msg['From'] = sender
    msg['To'] = to_address

    # ChatGPT will take over this part
    msg['Subject'] = 'Test 1'
    message = 'OHHOOO'

    msg.attach(MIMEText(message))

    mailserver = authenticate()
    mailserver.sendmail(sender, to_address, msg.as_string())
    mailserver.quit()

email_data = run_script(read_emails)

# Define a function to extract email components
def extract_email_components(email_data):
    pattern = re.compile(r'\nOn .+? wrote:\n')
    matches = list(pattern.finditer(email_data))

    # Add the indices of the start and end of each part
    indices = [0] + [match.start() for match in matches] + [len(email_data)]
    email_components = []
    
    # Process the first part
    first_part = email_data[indices[0]:indices[1]]
    sender_match = re.search(r'Sender: (.+)', first_part)
    subject_match = re.search(r'Subject: (.+)', first_part)
    content_match = re.search(r'Content: (.+)', first_part, re.DOTALL)
    
    sender = sender_match.group(1).strip() if sender_match else ""
    subject = subject_match.group(1).strip() if subject_match else ""
    content = content_match.group(1).strip() if content_match else ""
    
    email_components.append((sender, subject, content))
    
    # Process the remaining parts with the main subject from the first message
    for i in range(1, len(indices) - 1):
        part = email_data[indices[i]:indices[i + 1]]
        sender_match = re.search(r'([\w\s]+ <[\w\.]+@[\w\.]+\.[a-zA-Z]+>)', part)
        content_match = re.search(r'wrote:\n(.+)', part, re.DOTALL)
        
        sender = sender_match.group(1).strip() if sender_match else ""
        content = content_match.group(1).strip() if content_match else ""
        
        email_components.append((sender, subject, content))
    
    return email_components

# Get the email components
emails = extract_email_components(email_data)

# Format the output
def format_emails(emails):
    output = ""
    indent = ""
    for i, email in enumerate(emails[::-1]):
        sender, subject, content = email
        truncated_content = content + "..." if len(content) > 47 else content
        output += f"{indent}Sender: {sender}\n"
        output += f"{indent}Subject: {subject}\n"
        output += f"{indent}Content: {truncated_content}\n"
        output += f"{indent}Replies: {1 if i < len(emails) - 1 else 0}\n"
        indent += "    "
    return output

# Print the formatted output
formatted_output = format_emails(emails)
print(formatted_output)