# STILL TESTING !!!!!!!!!!

import imaplib
import email
from datetime import datetime, timedelta

# Email server settings (Gmail example)
EMAIL_HOST = 'imap.gmail.com'
EMAIL_PORT = 993
EMAIL_USERNAME = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_email_password'  # Or the generated "App Password" for Gmail

# Number of days threshold for deleting emails
DAYS_THRESHOLD = 30  # Change this to the desired threshold

def delete_old_emails():
    try:
        mail = imaplib.IMAP4_SSL(EMAIL_HOST, EMAIL_PORT)
        mail.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        mail.select('inbox')

        # Get the list of all emails in the inbox
        status, messages = mail.search(None, 'ALL')
        messages_ids = messages[0].split()

        # Calculate the date threshold
        date_threshold = (datetime.now() - timedelta(days=DAYS_THRESHOLD)).strftime('%d-%b-%Y')

        # Loop through the messages and delete the old ones
        for message_id in messages_ids:
            status, msg_data = mail.fetch(message_id, '(RFC822)')
            email_msg = email.message_from_bytes(msg_data[0][1])

            # Check the sent date of the email
            sent_date = email.utils.parsedate(email_msg['Date'])
            sent_date_str = datetime.fromtimestamp(email.utils.mktime_tz(sent_date)).strftime('%d-%b-%Y')

            # Delete the email if it is older than the threshold
            if sent_date_str < date_threshold:
                print(f"Deleting email ID: {message_id}")
                mail.store(message_id, '+FLAGS', '\\Deleted')

        # Permanently delete the emails marked for deletion
        mail.expunge()
        mail.logout()
        print("Old emails have been deleted successfully.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    delete_old_emails()
