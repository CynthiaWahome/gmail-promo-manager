import imaplib
import email
import re
import time
import random
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = os.environ.get('GMAIL_USER')        
APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')    
MAILBOX = 'INBOX'
PROMO_LABEL = 'Promo'  # This is the label that will be applied

# Define promotional keywords (case-insensitive)
KEYWORDS = ['deal', 'discount', 'offer']

def is_promotional(msg):
    """
    Determine if an email appears to be promotional.
    Checks:
      1. If the subject contains any promotional keywords.
      2. If the body (for text/plain parts) contains the word "unsubscribe".
    """
    # Check subject
    subject = msg.get('Subject', '')
    if subject:
        subject_lower = subject.lower()
        for kw in KEYWORDS:
            if kw in subject_lower:
                return True

    # Check for "unsubscribe" in the plain text body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                try:
                    part_body = part.get_payload(decode=True).decode(errors='ignore')
                    body += part_body
                except Exception:
                    pass
    else:
        if msg.get_content_type() == 'text/plain':
            try:
                body = msg.get_payload(decode=True).decode(errors='ignore')
            except Exception:
                body = ""
    if body and 'unsubscribe' in body.lower():
        return True

    # Check sender's email address
    from_address = msg.get('From', '')
    if 'noreply@' in from_address.lower():
        return True

    return False                       

def process_emails():
    """
    Connects to Gmail via IMAP, scans through the INBOX,
    labels promotional emails with the "Promo" label, and delays
    between operations to mimic human behavior.
    """
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        mail.select(MAILBOX)
    except Exception as e:
        print("Failed to connect or login to Gmail:", e)
        return

    # Search for all emails in the mailbox
    typ, data = mail.search(None, 'ALL')
    if typ != 'OK':
        print("No messages found!")
        mail.logout()
        return

    email_ids = data[0].split()
    print(f"Found {len(email_ids)} emails.")

    promo_count = 0
    for num in email_ids:
        typ, msg_data = mail.fetch(num, '(RFC822)')
        if typ != 'OK':
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        try:
            if is_promotional(msg):
                promo_count += 1
        except imaplib.IMAP4.abort as e:
            print(f"IMAP abort error while fetching email id {num}: {e}")
            break
        except Exception as e:
            print(f"Error while processing email id {num}: {e}")
            continue
    print(f"Total promotional emails found: {promo_count}")

    # Process each email individually
    for num in email_ids:
        typ, msg_data = mail.fetch(num, '(RFC822)')
        if typ != 'OK':
            print(f"Failed to fetch email id {num}")
            continue

        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        try:
            if is_promotional(msg):
                # Use Gmail’s IMAP extension to add a label
                typ, response = mail.store(num, '+X-GM-LABELS', f'("{PROMO_LABEL}")')
                if typ == 'OK':
                    print(f"Labeled email {num.decode()} as '{PROMO_LABEL}'.")
                else:
                    print(f"Failed to label email {num.decode()}. Response: {response}")
                # Random delay between 2 to 5 seconds for promotional emails
                delay = random.uniform(2, 5)
                print(f"Sleeping for {delay:.2f} seconds.")
                time.sleep(delay)
            else:
                print(f"Email {num.decode()} is not promotional. Skipping.")
                # Shorter delay for non-promotional emails
                time.sleep(random.uniform(1, 2))
        except imaplib.IMAP4.abort as e:
            print(f"IMAP abort error while processing email id {num}: {e}")
            break
        except Exception as e:
            print(f"Error while processing email id {num}: {e}")
            continue
            continue
    try:
        mail.logout()
    except imaplib.IMAP4.abort as e:
        print(f"IMAP abort error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        print("Processing complete.")

if __name__ == '__main__':
    process_emails()