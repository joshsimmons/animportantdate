from . import models

from collections import namedtuple
from django.conf import settings
from django.core import mail
from django.template import Context, Template  # TODO: use other engines?

MessageBase = namedtuple(
    'MessageBase',
    ("subject", "body", "from_", "recipient", "bcc"),
)


class Message(MessageBase):
    pass


class MailoutHelper(object):

    def __init__(self, mailout, recipients):
        self._mailout = mailout
        self._recipients = recipients
        self._render_messages()

    @property
    def messages(self):
        return list(self._messages)

    def _render_messages(self):
        messages = []

        for recipient in self._recipients:
            messages.append(self._render_single_message(recipient))

        self._messages = messages

    def send_messages(self):
        try:
            sent = []
            with mail.get_connection() as connection:
                for message in self.messages:
                    mail.EmailMessage(
                        message.subject,
                        message.body,
                        message.from_,
                        [message.recipient.email],
                        message.bcc,
                        connection,
                    ).send()

                    sent.append(models.MailSent(
                        mailout=self._mailout, recipient=message.recipient
                    ))
        finally:
            models.MailSent.objects.bulk_create(sent)


    def _render_single_message(self, recipient):
        subject_t = Template(self._mailout.subject)
        body_t = Template(self._mailout.plain_text)
        context = Context({"recipient": recipient})

        subject = subject_t.render(context)
        body = body_t.render(context)
        recipient = recipient
        from_ = settings.MAILOUTS_FROM_ADDRESS
        bcc = settings.MAILOUTS_ARCHIVE_ADDRESS

        return Message(subject, body, from_, recipient, bcc)
