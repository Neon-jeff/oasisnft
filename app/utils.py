from django.conf import settings
import smtplib
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

sender=settings.EMAIL_USER
auth=settings.EMAIL_AUTH
def SendEmail(user):
    sender = sender
    recipient = f'{user.email}'

# Create message
    msg = MIMEMultipart("alternative")
    email_template=render_to_string('pages/transactional.html',{'user':user})
    # text="Hi, welcome to nello"
    msg['Subject'] = f"Welcome to Nello"
    msg['From'] = sender
    msg['To'] = recipient
    part2 = MIMEText(email_template, 'html')
    msg.attach(part2)
# Create server object with SSL option
    server = smtplib.SMTP_SSL("smtp.zoho.com", 465)

# Perform operations via server
    server.login(sender, auth)
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()


def BulkEmail(emails):
    sender = sender

# Create message
    msg = MIMEMultipart("alternative")
    email_template=render_to_string('pages/transactional.html',{'user':user})
    text="Hi, welcome to nello"
    msg['Subject'] = f"Welcome to Nello"
    msg['From'] = sender
    msg['To'] = ", ".join(emails)
    part2 = MIMEText(email_template, 'html')
    msg.attach(part2)
# Create server object with SSL option
    server = smtplib.SMTP_SSL("smtp.zoho.com", 465)

# Perform operations via server
    server.login(sender, auth)
    server.sendmail(sender, emails, msg.as_string())
    server.quit()

def WithdrawNotification(user,amount):
    sender = sender
    recipient = f'{user.email}'

# Create message
    msg = MIMEMultipart("alternative")
    email_template=render_to_string('pages/withdraw-email.html',{'user':user,'amount':amount,'fee':(round(float(amount),4)/10)})
    # text="Hi, welcome to nello"
    msg['Subject'] = f"Withdrawal Created"
    msg['From'] = sender
    msg['To'] = recipient
    part2 = MIMEText(email_template, 'html')
    msg.attach(part2)
# Create server object with SSL option
    server = smtplib.SMTP_SSL("smtp.zoho.com", 465)

# Perform operations via server
    server.login(sender, auth)
    server.sendmail(sender, [recipient], msg.as_string())
    server.quit()
