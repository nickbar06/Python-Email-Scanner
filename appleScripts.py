read_emails = """
set output to ""
tell application "Mail"
	set theAccount to the second account
	set theMailbox to mailbox "Inbox" of theAccount
	set theMessages to messages of theMailbox
	
	set messageCount to count of theMessages
	set maxMessages to 1
	
	if messageCount < maxMessages then
		set maxMessages to messageCount
	end if
	
	repeat with i from 1 to maxMessages
		set theMessage to item i of theMessages
		set messageInfo to ""
		set messageInfo to messageInfo & "Sender: " & (sender of theMessage as rich text) & return
		set messageInfo to messageInfo & "Subject: " & (subject of theMessage as rich text) & return
		set messageInfo to messageInfo & "Date Sent: " & (date sent of theMessage as rich text) & return
        set messageInfo to messageInfo & "Message ID: " & (message id of theMessage as text) & return
		set messageInfo to messageInfo & "Content: " & (content of theMessage as rich text) & return
		set output to output & messageInfo
	end repeat
end tell
return output
"""