from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from DevTest.settings import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER
from email.mime.multipart import MIMEMultipart
from .utils import delete_temp_file_after_time

import smtplib

def send_mail(to, subject="", body="", attachments=""):

    # smtp server init
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()

    # Email generation
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'plain'))

    with open(attachments, 'rb') as file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(file.read())  # Read the file content into the payload
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="Summary_Report.xlsx"')
        msg.attach(part)
    
    msg['Subject'] = subject
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = to
    try:
        server.login(EMAIL_HOST_USER,EMAIL_HOST_PASSWORD)

        server.sendmail(EMAIL_HOST_USER, to, msg.as_string())
    except Exception as e:
        return 500, f"Error: {e}"
    finally:
        server.quit()
    
    delete_temp_file_after_time(attachments, delay=120)

    return 200, "Sent Successfully"
