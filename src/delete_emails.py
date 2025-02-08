import imaplib
import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# --- Configuration ---
IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = os.environ.get('GMAIL_USER')         # Your Gmail address
APP_PASSWORD = os.environ.get('GMAIL_APP_PASSWORD')    # Your Gmail App Password
LABEL = 'Promo'                                      # The label that was applied to promotional emails
PROCESSED_EMAILS_FILE = 'processed_emails.json'  # Path to the processed emails JSON file

def delete_promo_emails():
    """
    Connects to Gmail via IMAP, searches for emails with the given label,
    moves them to the Trash folder, and expunges them from the mailbox.
    """
    try:
        # Connect securely to Gmail's IMAP server
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
    except Exception as e:
        print("Failed to connect or login to Gmail:", e)
        return

    try:
        # Select the "All Mail" folder.
        mail.select('"[Gmail]/All Mail"')

        # Search for emails that have the label "Promo" using Gmail's X-GM-RAW search.
        typ, data = mail.search(None, 'X-GM-RAW', f'"label:{LABEL}"')
        if typ != 'OK':
            print("No messages found with label:", LABEL)
            mail.logout()
            return

        email_ids = data[0].split()
        print(f"Found {len(email_ids)} emails with label '{LABEL}'.")

        # Move each email to the Trash folder
        for num in email_ids:
            try:
                typ, response = mail.store(num, '+X-GM-LABELS', '\\Trash')
                if typ == 'OK':
                    print(f"Email {num.decode() if isinstance(num, bytes) else num} moved to Trash.")
                else:
                    print(f"Failed to move email {num.decode() if isinstance(num, bytes) else num} to Trash. Response: {response}")
            except imaplib.IMAP4.abort as e:
                print(f"IMAP abort error while moving email {num.decode() if isinstance(num, bytes) else num} to Trash: {e}")
                break
            except Exception as e:
                print(f"Error while moving email {num.decode() if isinstance(num, bytes) else num} to Trash: {e}")
                continue

        # Select the Trash folder and expunge emails
        mail.select('[Gmail]/Trash')
        mail.expunge()
        print("Emails moved to Trash and expunged.")

        # Delete emails from the Trash folder in batches
        BATCH_SIZE = 100
        typ, data = mail.search(None, 'ALL')
        if typ == 'OK':
            email_ids = data[0].split()
            for i in range(0, len(email_ids), BATCH_SIZE):
                batch = email_ids[i:i + BATCH_SIZE]
                for num in batch:
                    mail.store(num, '+FLAGS', '\\Deleted')
                mail.expunge()
                print(f"Batch {i // BATCH_SIZE + 1} of {len(email_ids) // BATCH_SIZE + 1} processed.")
            print("Trash folder emptied.")
        else:
            print("Failed to search Trash folder for emails to delete.")

        print("Deletion complete. All emails with label 'Promo' have been permanently removed.")
    except imaplib.IMAP4.abort as e:
        print("IMAP connection aborted:", e)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        mail.logout()
 # Delete the processed_emails.json file
        try:
            if os.path.exists(PROCESSED_EMAILS_FILE):
                os.remove(PROCESSED_EMAILS_FILE)
                print(f"{PROCESSED_EMAILS_FILE} has been deleted.")
            else:
                print(f"{PROCESSED_EMAILS_FILE} does not exist.")
        except Exception as e:
            print(f"An error occurred while deleting {PROCESSED_EMAILS_FILE}: {e}")

if __name__ == '__main__':
    delete_promo_emails()
