# Sending Report Emails to Parents
This repository contains code that allows you to send report emails to parents about their child's academic progress. The code is written in Python and uses the Gmail API to send emails.

# Installation
To use this code, you'll need to follow these steps:

Clone this repository to your local machine.

Install the required packages by running pip install -r requirements.txt.

Set up a Google Cloud Platform (GCP) project and enable the Gmail API. You can follow the instructions in the Gmail API documentation.

Download the credentials.json file and save it in the root directory of the repository.

Prepare the report data in a CSV file. The file should have the following columns: name, subject, grade, comments and email address . Each row represents a report for a single student. Save the file in the data directory with the name reports.csv.

# Usage
To send report emails to parents, simply run the send_emails.py script:

python send_emails.py
The script will read the report data from the reports.csv file and send an email to each parent using the Gmail API. The email will contain the student's name, subject, grade, and comments.

# Contributing
If you find any issues or have any suggestions for improvement, feel free to create a pull request or open an issue.
