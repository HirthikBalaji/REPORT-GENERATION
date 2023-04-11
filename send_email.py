import helper
from datetime import datetime

current_year = datetime.now().year
academic_year = str(current_year)+str(int(current_year+1))

MYMAIL = 'senderemail@example.com'
PASSWORD = helper.retrive_pass()
SUBJ = f"REPORT CARD - {academic_year}"
creds = helper.get_credentials(creds_file_path="credentials.pickle.encrypted",PASSWORD=PASSWORD,secret_json_path="client_secret.json.encrypted")

report_data = helper.read_data("REPORT_DATA.csv")

for i in report_data:
    message = helper.report_card(i)
    helper.send_email(creds=creds,sender_email=MYMAIL,recipient=i['EMAIL'],subject=SUBJ,body=message)
