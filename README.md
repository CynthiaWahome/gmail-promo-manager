# Gmail Promotional Email Automation

## Overview
This project provides a set of Python scripts to help you manage promotional emails in your Gmail account. The scripts automate tasks such as:
- **Labeling Promotional Emails:** Scanning your inbox for promotional messages (using keywords, unsubscribe text, and sender hints) and labeling them with "Promo."
- **Processing Unsubscribe Links:** Extracting unsubscribe URLs from promotional emails and opening them in your browser for manual confirmation.
- **Deleting Promotional Emails:** Permanently removing emails that have been labeled as "Promo" to clean up your inbox.

By automating these tasks, you can efficiently manage your Gmail account and reduce clutter.

## Prerequisites
- **Python 3.x** installed.
- A **Gmail account** with IMAP access enabled.
- **2-Step Verification** turned **ON** for your Gmail account.
- An **App Password** generated for this project.
- The [python-dotenv](https://pypi.org/project/python-dotenv/) package (to load environment variables).

## Setup

### 1. Enable 2-Step Verification and Create an App Password
1. Visit [Google Account Security](https://myaccount.google.com/security) and ensure that 2-Step Verification is enabled.
2. Then visit [Google App Passwords](https://myaccount.google.com/apppasswords) to create an application-specific password. Use this 16‑character password in your configuration instead of your regular Gmail password.

### 2. Configure Environment Variables
1. Create a `.env` file in the project root directory. This file will store your Gmail credentials securely.
2. Add the following content to the `.env` file (replace with your own credentials):

```ini
GMAIL_USER=your_email@gmail.com
GMAIL_APP_PASSWORD=your_app_password
```

## Getting Started

### Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/CynthiaWahome/gmail-promo-manager.git
cd gmail-promo-manager
```
### Install Dependencies
1. Ensure you have Python 3.x installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
2. Install the required packages using pip. If you have a `requirements.txt` file, run:
Make sure you have Python 3.x installed. Install required packages using pip. If you have a `requirements.txt` file, run:

```bash
pip install -r requirements.txt
```

If not, ensure you install:

```bash
pip install python-dotenv
```

## Scripts Description

### `src/process_emails.py`
- **What It Does:**  
    Connects to Gmail via IMAP, scans your INBOX for promotional emails based on specific keywords (e.g., "deal", "discount", "offer"), the word "unsubscribe", and sender patterns (like "noreply@"). It then labels these emails with "Promo" while introducing random delays to mimic human behavior.
- **Usage:**  
    Run manually with:
    ```bash
    python src/process_emails.py
    ```

### `src/unsubscribe.py`
- **What It Does:**  
    Connects to the mailbox (labeled "Promo"), extracts HTTP unsubscribe URLs from the standard "List-Unsubscribe" header, and prompts you to open each link in your default web browser for manual unsubscription.
- **Usage:**  
    Run manually with:
    ```bash
    python src/unsubscribe.py
    ```

### `src/delete_emails.py`
- **What It Does:**  
    Searches your INBOX for emails that have been labeled "Promo" and permanently deletes them using Gmail's IMAP commands.
- **Usage:**  
    Run manually with:
    ```bash
    python src/delete_emails.py
    ```

## Scheduling the Scripts
On Windows, you can use Windows Task Scheduler to automate the execution of these scripts. For example, you can schedule the scripts to run daily during off-peak hours.

Basic Steps for Task Scheduler:
1. Open Task Scheduler (Win + R, type taskschd.msc).
2. Create a new basic task (e.g., "Gmail Promo Labeler").
3. Set the trigger (e.g., daily at 2:00 AM).
4. Set the action to Start a program and point it to your Python interpreter (e.g., C:\Python39\python.exe) with the script's full path as an argument.
5. Save the task.

If you prefer to run your scripts via Git Bash, ensure your Python environment is accessible from Git Bash and adjust the task settings accordingly.

## Helpful Links
- [Google Account Security](https://myaccount.google.com/security) – Confirm that 2-Step Verification is enabled.
- [Google App Passwords](https://myaccount.google.com/apppasswords) – Generate an App Password for your project.
- [python-dotenv on PyPI](https://pypi.org/project/python-dotenv/) – Package used for managing environment variables.

## Contributing
Contributions are welcome! If you have improvements or refactoring suggestions for the code, please follow these guidelines:
1. **Fork the Repository:** Create your own fork and work on a feature branch.
2. **Follow Code Style:** Adhere to Python best practices and PEP 8.
3. **Document Your Changes:** Add clear comments and update this README if needed.
4. **Submit a Pull Request:** Provide a clear description of your changes and why they benefit the project.
5. **Report Issues:** If you encounter any bugs or have suggestions, please open an issue with a detailed description.

## License
This project is open source and available under the MIT License.
