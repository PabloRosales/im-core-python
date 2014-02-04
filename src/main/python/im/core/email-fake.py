
from __future__ import absolute_import

import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from im.core.config import conf

logger = logging.getLogger('im.core.email')


def send_email(_from, to, subject, message_text, message_html=None):

    smpp_host = conf('email.host')
    smpp_port = conf('email.port')
    smpp_user = conf('email.user')

    logger.debug('Sending email to SMPP %s@%s:%s',
        smpp_user, smpp_host, smpp_port)
    logger.debug('Sending email to %s, from %s', to, _from)
    logger.debug('Email plain message with subject %s is: %s',
        subject, message_text)

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = _from
    msg['To'] = ', '.join(to)

    part1 = MIMEText(message_text, 'plain')
    msg.attach(part1)
    if message_html:
        logger.debug('Email html message with subject %s is: %s',
            subject, message_html)
        part2 = MIMEText(message_html, 'html')
        msg.attach(part2)

    mailServer = smtplib.SMTP(smpp_host, smpp_port)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(smpp_user, conf('email.pass'))
    mailServer.sendmail(smpp_user, to, msg.as_string())
    mailServer.close()


def send_email_monitoring(subject, body):
    if conf('config.send_monitoring_emails', False):
        send_email(
            conf('config.monitoring_email_from'),
            conf('config.monitoring_recipients'),
            subject,
            body
        )
