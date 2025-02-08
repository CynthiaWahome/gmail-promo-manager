import imaplib
import email
import re
import os
import webbrowser
import json
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# --- Configuration ---
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = os.environ.get('GMAIL_USER')         # Your Gmail address
APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')    # Your Gmail App Password
MAILBOX = 'Promo'                                    # The mailbox/label where promotional emails reside

def extract_unsubscribe_urls(msg):
    """
    Extract HTTP unsubscribe URLs from the "List-Unsubscribe" header.
    The header may contain multiple entries (e.g., a mailto and a URL).
    We choose the HTTP/HTTPS URL if present.
    """
    urls = []
    list_unsub = msg.get('List-Unsubscribe')
    if list_unsub:
        # Split header on commas and remove enclosing angle brackets
        parts = re.split(r',\s*', list_unsub)
        for part in parts:
            part = part.strip().strip('<>').strip()
            if part.startswith('http'):
                urls.append(part)
    return urls

def process_unsubscribe_links():
    """
    Connect to Gmail via IMAP, scan through emails in the specified mailbox,
    and for each email that includes a List-Unsubscribe header,
    extract the unsubscribe URL(s) and open them in the default web browser
    (after prompting for confirmation).
    """
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        mail.select(MAILBOX)
    except imaplib.IMAP4.abort as e:
        print("IMAP connection aborted:", e)
        return
    except Exception as e:
        print("Failed to connect or login to Gmail:", e)
        return

    try:
        typ, data = mail.search(None, 'ALL')
        if typ != 'OK':
            print("No messages found in mailbox!")
            mail.logout()
            return
    except imaplib.IMAP4.abort as e:
        print("IMAP search aborted:", e)
        mail.logout()
        return
    except Exception as e:
        print("Failed to search emails:", e)
        mail.logout()
        return

    email_ids = data[0].split()
    print(f"Found {len(email_ids)} emails in the '{MAILBOX}' mailbox.")

    # Load processed email IDs from file
    processed_emails_file = 'processed_emails.json'
    if os.path.exists(processed_emails_file):
        with open(processed_emails_file, 'r') as f:
            processed_emails = json.load(f)
    else:
        processed_emails = []

    for num in email_ids:
        email_id = num.decode()
        if email_id in processed_emails:
            print(f"Email ID {email_id} already processed. Skipping.")
            continue

        typ, msg_data = mail.fetch(num, '(RFC822)')
        if typ != 'OK':
            print(f"Failed to fetch email id {num}")
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        subject = msg.get('Subject', '(No Subject)')
        urls = extract_unsubscribe_urls(msg)
        if urls:
            print(f"\nEmail ID {num.decode() if isinstance(num, bytes) else num}: {subject}")
            for url in urls:
                print(f"Found unsubscribe URL: {url}")
                # Prompt user before opening the URL
                user_input = input("Press Enter to open this unsubscribe link in your browser (or type 'skip' to skip): ")
                if user_input.lower() != 'skip':
                    webbrowser.open_new_tab(url)
                    print("Opened the URL in your default browser.")
            else:
                processed_emails.append(email_id)
                processed_emails.append(num.decode())
        else:
            print(f"Email ID {num.decode() if isinstance(num, bytes) else num}: {subject} - No unsubscribe URL found.")

    # Save processed email IDs to file
    with open(processed_emails_file, 'w') as f:
        json.dump(processed_emails, f)

    try:
        mail.logout()
    except Exception as e:
        print("Error logging out:", e)
    finally:
        print("Done processing unsubscribe links.")

if __name__ == '__main__':
    process_unsubscribe_links()
