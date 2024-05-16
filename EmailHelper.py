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

def parse_email_data(data):
    emails = {}
    email_blocks = data.strip().split("\n----------------------------------\n")
    
    for block in email_blocks:
        lines = block.strip().split("\n")
        sender = subject = date_sent = message_id = None
        content_lines = []
        
        for line in lines:
            if line.startswith("Sender: "):
                sender = line[len("Sender: "):].strip()
            elif line.startswith("Subject: "):
                subject = line[len("Subject: "):].strip()
            elif line.startswith("Date Sent: "):
                date_sent = line[len("Date Sent: "):].strip()
            elif line.startswith("Message ID: "):
                message_id = line[len("Message ID: "):].strip()
            elif line.startswith("Content: "):
                content = line[len("Content: "):].strip()
                content_lines = [content]
            else:
                content_lines.append(line)
        
        if message_id and sender and subject and date_sent:
            content = "\n".join(content_lines)
            # Parse the content into individual replies
            replies = parse_replies(content)
            for i, reply_content in enumerate(replies):
                reply_id = f"{message_id}-{i+1}"
                print(reply_id)
                if i == 0:
                    email_node = EmailNode(reply_id, sender, subject, date_sent, reply_content)
                else:
                    pattern = re.compile(r"On (.*?) at (.*?), (.*?) <(.*?)> wrote:")
                    match = pattern.search(reply_content)
                    cleaned_data = pattern.sub("", reply_content)


                    if match:
                        date = match.group(1)
                        sendername = match.group(3)
                        senderaddress = match.group(4)
                    else:
                        raise ValueError("The provided string does not match the expected format.")
                    
                    email_node = EmailNode(reply_id, sendername + " <" + senderaddress + ">", subject, date, cleaned_data)
                emails[reply_id] = email_node
    
    return emails

def parse_replies(data):
    messages = []
    # Use regular expressions to find the positions of "> wrote:"
    pattern = re.compile(r"On .*? wrote:")
    positions = [match.start() for match in pattern.finditer(data)]
    
    # Append the end of the data to the positions list
    positions.append(len(data))
    
    # Extract messages based on the positions
    start = 0
    for pos in positions:
        if start < pos:
            message = data[start:pos].strip()
            if message:
                messages.append(message)
        start = pos
    
    return messages

def link_emails(emails):
    pattern = re.compile(r"> wrote:")
    email_list = list(emails.values())
    
    for email in email_list:
        lines = email.content.split("\n")
        reply_content = []
        for line in lines:
            if pattern.search(line):
                if reply_content:
                    reply_message = "\n".join(reply_content).strip()
                    for potential_reply in email_list:
                        if potential_reply.content.strip() == reply_message:
                            potential_reply.replies.append(email)
                            break
                    reply_content = []
            else:
                reply_content.append(line)
                
    return emails

def print_linked_emails(emails):
    def print_email(email, indent=0):
        print(" " * indent + f"Sender: {email.sender}")
        print(" " * indent + f"Subject: {email.subject}")
        print(" " * indent + f"Date Sent: {email.date_sent}")
        print(" " * indent + f"Content: {email.content}")  # Print a snippet of the content for brevity
        print(" " * indent + f"Replies: {len(email.replies)}")
        print("")
        for reply in email.replies:
            print_email(reply, indent + 4)

    for email in emails.values():
        if not any(email in e.replies for e in emails.values()):  # Find top-level emails (not replies)
            print_email(email)

email_data = run_script(read_emails)
# print(email_data)

emails = parse_email_data(email_data)
linked_emails = link_emails(emails)
print_linked_emails(linked_emails)