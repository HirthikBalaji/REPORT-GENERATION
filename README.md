# Report Emailer

This repository contains code that allows you to send report emails to parents about their child's academic progress. The code is written in Python and uses the Gmail API to send emails.

## Features

- Generate personalized reports for each student based on their grades and attendance
- Send emails to parents with the report as an attachment
- Customize the email subject and message
- Use a template for the report format
- Store the student data and parent contacts in CSV files

## Requirements

- Python 3.6 or higher
- Gmail account with API access enabled
- Google Cloud Platform project with Gmail API enabled
- Credentials file for the Gmail API

## Installation

- Clone this repository or download the zip file
- Install the required packages using pip:

```bash
pip install -r requirements.txt
```
- Create a credentials.json file for the Gmail API following this guide: https://developers.google.com/gmail/api/quickstart/python
- Place the credentials.json file in the same folder as the code

## Usage
- Edit the send_email.py file to set your email address, subject, and message
- Edit the REPORT_DATA.csv file to add or modify the student data 📈

Run the send_email.py file to send the report emails: 👍
