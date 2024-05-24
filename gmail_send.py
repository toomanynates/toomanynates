from email.message import EmailMessage
import ssl
import smtplib

# This sends a message from gmail to yahoo
# from https://www.youtube.com/watch?v=g_j6ILT-X0k

email_sender = 'toomanynates@gmail.com'
email_password = 'mbbu qnyd rnxl ztoj'
email_receiver = 'toomanynates@yahoo.com'

subject = 'Automation from gmail'
body = """
Hi,

This is a test email sent with Python from my gmail.

-Nate
"""

em = EmailMessage()

em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

mycontext = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = mycontext) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string() )

print("Done")