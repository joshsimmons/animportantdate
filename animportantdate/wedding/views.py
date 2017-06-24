from . import forms
from . import mail_alerts
from . import mailouts
from . import models

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import mail_managers
from django.shortcuts import redirect, render, reverse



# Create your views here.

def index(request):

    auth_form = forms.AuthForm(
        request.GET or None,
        prefix="auth",
    )

    if request.GET and auth_form.is_valid():
        try:
            authenticate(request, auth_form.cleaned_data["pnr"])
            return redirect(guest_details)
        except models.Group.DoesNotExist:
            auth_form.add_error("pnr", "This confirmation code is invalid.")

    data = {
        "auth_form": auth_form,
        "body_class": "home",
    }

    return render(request, "wedding/index.html", data)


def guest_login(request, pnr):
    try:
        authenticate(request, pnr)
        return redirect(guest_details)
    except models.Group.DoesNotExist:
        base_url = reverse(index) + "?auth-pnr=%s" % pnr
        return redirect(base_url)


def guest_details(request):

    group = get_group(request)

    group_form = forms.GroupForm(
        request.POST or None,
        instance=group,
        prefix="group",
    )

    if request.POST and group_form.is_valid():
        group_form.save()
        messages.success(request, "Thank you! We've got your contact details.")
        mail_alerts.group_contact_update(group)

    data = {
        "group_form": group_form,
        "group": group,
        "body_class": "guest",
    }

    return render(request, "wedding/guest_details.html", data)


def authenticate(request, pnr):
    group = models.Group.objects.get(pnr=pnr)
    request.session["group_id"] = group.id


def get_group(request):
    if "group_id" in request.session:
        group_id = request.session["group_id"]
        group = models.Group.objects.get(id=group_id)
        return group
    else:
        return None


def content_page(request, page_name=None):
    data = {
        "body_class": page_name,
        "group": get_group(request),
    }

    return render(request, "wedding/pages/%s.html" % page_name, data)


@staff_member_required
def mailout(request, mailout_id):

    mailout_id = int(mailout_id)

    mailout = models.Mailout.objects.get(id=mailout_id)
    # TODO tidy up query here.
    already_sent = models.MailSent.objects.filter(mailout__event=mailout.event)
    groups_eligible = mailout.event.group_set.all()
    people_eligible = models.Person.objects.filter(group=groups_eligible)
    people_already_sent_id = set(item.recipient.id for item in already_sent)

    initial = {
        "people": people_eligible.exclude(id__in=people_already_sent_id),
    }

    form = forms.DoMailoutForm(
        request.POST or None,
        prefix="mailout",
        initial=initial,
    )

    # Restrict the people who appear to the people who are eligible
    form.fields["people"].queryset = people_eligible

    data = {
        "mailout": mailout,
        "mailout_form": form,
    }

    if request.POST and form.is_valid():
        # Construct mailouts
        m = mailouts.MailoutHelper(mailout, form.cleaned_data["people"])
        data["mailouts"] = m.messages

        if form.cleaned_data["action"] == forms.DoMailoutForm.ACTION_SEND_MAIL:
            try:
                m.send_messages()
                messages.success(request, "The messages have been sent successfully")
                return redirect(
                    'admin:%s_%s_change' % (
                        mailout._meta.app_label, mailout._meta.model_name),
                        mailout.id,
                    )
            except Exception as e:
                # SHOW ERROR HERE.
                if True:
                    raise e
                # messages.error(request, "Error:" + str(e))

    return render(request, "wedding/mailout_form.html", data)
