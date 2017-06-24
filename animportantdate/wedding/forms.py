from . import models
from django import forms
from django.utils.translation import ugettext_lazy as _

class AuthForm(forms.Form):

    pnr = forms.CharField(
        max_length=6,
        label="Confirmation code",
    )


class GroupForm(forms.ModelForm):

    class Meta:
        model = models.Group
        fields = [
            "telephone",
            "address_1",
            "address_2",
            "address_city",
            "address_state_province",
            "address_postal_code",
            "address_country",
        ]

    def make_required(self, field):
        self.fields[field].required = True

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        required_fields = [
            "address_1",
            "address_city",
            "address_postal_code",
            "address_country",
            "telephone",
        ]
        for i in required_fields:
            self.make_required(i)


class DoMailoutForm(forms.Form):
    ACTION_PREVIEW = 1
    ACTION_SEND_MAIL = 2

    ACTIONS = (
        (ACTION_PREVIEW, "Preview"),
        (ACTION_SEND_MAIL, "Send mailout"),
    )

    people = forms.ModelMultipleChoiceField(queryset=models.Person.objects)
    action = forms.TypedChoiceField(choices=ACTIONS, coerce=int)
