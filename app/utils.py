from django.conf import settings
import smtplib
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
import base64
import requests


sender=settings.EMAIL_USER
auth=settings.EMAIL_AUTH
key=settings.IMHOST
def SendEmail(user):

    recipient = f'{user.email}'

# Create message
    msg = MIMEMultipart("alternative")
    email_template=render_to_string('pages/transactional.html',{'user':user})
    # text="Hi, welcome to nello"
    msg['Subject'] = f"Explore with Nello"
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
# Create message
    msg = MIMEMultipart("alternative")
    email_template=render_to_string('pages/bulk.html')
    text="Hi, welcome to nello"
    msg['Subject'] = f"Explore with Nello"
    msg['From'] = sender
    msg['Bcc'] = ", ".join(emails)
    part2 = MIMEText(email_template, 'html')
    msg.attach(part2)
# Create server object with SSL option
    server = smtplib.SMTP_SSL("smtp.zoho.com", 465)

# Perform operations via server
    server.login(sender, auth)
    server.sendmail(sender, emails, msg.as_string())
    server.quit()


# withdraw notification
def WithdrawNotification(user,amount):

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


def SendDirect(user,email,content,subject):
# Create message
    msg = MIMEMultipart("alternative")
    email_template=render_to_string('pages/notification.html',{'user':user,'content':content,'subject':subject})
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = email
    part2 = MIMEText(email_template, 'html')
    msg.attach(part2)
# Create server object with SSL option
    server = smtplib.SMTP_SSL("smtp.zoho.com", 465)
# Perform operations via server
    server.login(sender, auth)
    server.sendmail(sender, [email], msg.as_string())
    server.quit()


def UploadImage(file,name):
    data={
            "key":key,
            "image":base64.b64encode(file),
            "name":name
        }
    resp= requests.post("https://api.imgbb.com/1/upload",data=data)
    # Perform Error Handling here
    return resp.json()['data']['url']


# def ReadUploadedLinks():
#     with open('new.txt','r') as links:
#         arr=links.read().split('\n')
#     link_ids=[x for x in arr if x!='']
#     return link_ids
