import sendgrid
import logging
import requests
import os
from CouncilTag import settings
from sendgrid.helpers.mail import Email, Content, Mail, Attachment
import base64

log = logging.Logger(__name__)


def verify_recaptcha(token):
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data={
                      'secret': os.environ["RECAPTCHAKEY"], 'response': token})
    response = r.json()
    return response['success']


def send_mail(mail_message):
    APIKEY = os.environ["SENDGRIDKEY"]
    sg = sendgrid.SendGridAPIClient(apikey=APIKEY)
    from_email = Email("do-not-reply@engage.town")
    if type(mail_message["user"]) is dict:
        to_email = Email(mail_message["user"]["email"])
    else:
        to_email = Email(mail_message["user"].email)
    subject = mail_message["subject"]
    content = Content('text/html', (mail_message["content"]))
    mail = Mail(from_email=from_email, subject=subject,
                to_email=to_email, content=content)

    if "attachment_file_path" in mail_message:
        with open(mail_message["attachment_file_path"], 'rb') as f:
            data = f.read()
            f.close()

        encode = base64.b64encode(data).decode()
        attachment = Attachment()
        attachment.content = encode
        attachment.type = mail_message["attachment_type"]
        attachment.filename = mail_message["attachment_file_name"]
        attachment.disposition = "attachment"
        mail.add_attachment(attachment)

    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code == 200 or response.status_code == 202:
        return True
    else:
        log.error("Could not send an email from {} to {} about {}".format(from_email,
                                                                          to_email, subject))
        log.error(response.body)
        log.error(response.status_code)
        return False


def send_message(message_record):
    sg = sendgrid.SendGridAPIClient(apikey=settings.SENDGRID_API_KEY)
    from_email = Email(message_record["user"].email)
    to_email = Email(settings.COUNCIL_CLERK_EMAIL)
    subject = "Comment on {}".format(message_record.agenda_item.title)
    content = Content('text/html', message_record.content)
    mail = Mail(from_email=from_email, subject=subject,
                to_email=to_email, content=content)
    response = sg.client.mail.send.post(request_body=mail.get())
    if response.status_code == 200 or response.status_code == 202:
        return True
    else:
        log.error("Could not send an email from {} to {} about {}".format(from_email,
                                                                          to_email, subject))
        log.error(response.body)
        log.error(response.status_code)
        return False
