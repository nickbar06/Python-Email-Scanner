class EmailNode:
    def __init__(self, message_id, sender, subject, date_sent, content):
        self.message_id = message_id
        self.sender = sender
        self.subject = subject
        self.date_sent = date_sent
        self.content = content
        self.replies = []