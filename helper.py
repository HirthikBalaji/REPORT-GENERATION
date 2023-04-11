import csv
import os
import pickle
import base64
from getpass import getpass

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from Crypto.Cipher import AES

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


def retrive_pass():
    passwrd = getpass("ENTER THE PASSWORD TO DECRYPT :")
    return passwrd


def read_data(file):
    report_data = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            report_data.append(row)
    return report_data


def encrypt_file(key, filename):
    chunksize = 64 * 1024
    outputFile = f"{filename}.encrypted"
    filesize = str(os.path.getsize(filename)).zfill(16)
    iv = os.urandom(16)

    encryptor = AES.new(key, AES.MODE_CBC, iv)

    with open(filename, 'rb') as infile:
        with open(outputFile, 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))
    os.remove(filename)


def decrypt_file(key, filename):
    chunksize = 64 * 1024
    outputFile = filename[:-10]
    with open(filename, 'rb') as infile:
        filesize = int(infile.read(16))
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(outputFile, 'wb') as outfile:
            # with open(outputFile.split(".enc")[0],"wb") as out:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(filesize)


def get_credentials(creds_file_path, PASSWORD, secret_json_path):
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    if os.path.exists(creds_file_path):
        decrypt_file(PASSWORD, creds_file_path)
        with open(creds_file_path[:-10], 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            decrypt_file(PASSWORD, secret_json_path)
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        encrypt_file(PASSWORD, secret_json_path)
        with open(creds_file_path[:-10], 'wb') as token:
            pickle.dump(creds, token)
            encrypt_file(PASSWORD, creds_file_path[:-10])
    return creds


def send_email(creds, sender_email, recipient, subject, body, image_file_path=None):
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEMultipart()
    message['to'] = str(recipient)
    message['subject'] = subject

    # Attach the plain text and HTML versions of the email body
    message.attach(MIMEText(body, 'plain'))
    message.attach(MIMEText(body, 'html'))

    # Attach the image file to the email
    if image_file_path is not None and os.path.exists(image_file_path):
        with open(image_file_path, 'rb') as f:
            img_data = f.read()
        image = MIMEImage(img_data, name=os.path.basename(image_file_path))
        message.attach(image)
    try:
        # Create a message and encode it in base64
        create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        # Send the message using the Gmail API
        send_message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(
            F'The email was sent from {sender_email} to {recipient} with email Id: {send_message["id"]} with message: \n {body}')
    except HttpError as error:
        print(F'An error occurred:{error}')
    except ConnectionError as error:
        print(F'An error occurred:{error}. Check your internet connection and try again.')
    except ValueError as error:
        print(F'An error occurred:{error}. Check the email address provided and try again.')
    except Exception as error:
        print(F'An error occurred:{error}')
    return None



def report_card(subjects):
    keys = list(subjects.keys())
    keys.remove("NAME")
    keys.remove("EMAIL")
    string_report = f"Report Card for {subjects['NAME']}"
    string_report = string_report + "\n" + "Subject\t\tPercentage"
    string_report = string_report + "\n" + "==========================="
    for i in keys:
        string_report = string_report + "\n" + f"{i}\t\t{subjects[i]}%"
    string_report = string_report + "\n" + "==========================="
    return string_report
    # print(f"Overall Percentage: {sum(subjects.values()) / len(subjects):.2f}%")
