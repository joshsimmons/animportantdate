from django.core.mail import mail_managers


class MailAlert(object):

    def send(self, **k):
        mail_managers(self.subject(**k), self.message(**k))

    def subject(self, **k):
        return self.__SUBJECT__.format_map(k)

    def message(self, **k):
        return self.__TEMPLATE__.format_map(k)


class GroupContactUpdate(MailAlert):
    __SUBJECT__ = "Group contact details updated"
    __TEMPLATE__ = '''Hello!

The following group has has updated their contact information.
Enjoy!

Group: {group.display_name}


<3,

--Your wedding app.'''


def group_contact_update(group):
    GroupContactUpdate().send(group=group)
