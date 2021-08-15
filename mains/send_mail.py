import smtplib
from email.message import EmailMessage


def send_mail(name):
    gmail_user = 'noreplypythonprogram123@gmail.com'
    gmail_password = 'PP200200'
    if name == "non-enrolled user":
        name = "An unknown user"
    sent_from = gmail_user
    to = ['irad9731@gmail.com', 'ronel.packer1@gmail.com']
    subject = 'Someone else tried to access your folder!'
    body = f'{name} tried to access your folder!\n we don\'t like it!'
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = to

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(gmail_user, gmail_password)
        smtp_server.send_message(msg)
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as ex:
            print("Something went wrong….", ex)
