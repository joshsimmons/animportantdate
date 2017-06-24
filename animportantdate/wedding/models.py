from django.db import models
from django_countries.fields import CountryField
from django.utils import timezone
# Create your models here.


class Group(models.Model):
    ''' A group is an organisation that receives an invitation. '''

    def __str__(self):
        return self.display_name

    pnr = models.CharField(
        max_length=6,
        unique=True,
        verbose_name="Confirmation Code",
    )

    address_1 = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Address Line 1",
    )
    address_2 = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Address Line 2",
    )
    address_city = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="City or Suburb",
    )
    address_state_province = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="State or Province",
    )
    address_postal_code = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Postal Code",
    )
    address_country = CountryField(
        blank=True,
        verbose_name="Country"
    )
    telephone = models.CharField(
        max_length=20,
        blank=True,
    )

    # 4 chars to allow for ICAO if absolutely necessary
    home_airport = models.CharField(
        max_length=4,
        blank=True,
    )

    display_name = models.CharField(max_length=255)
    events = models.ManyToManyField(
        "Event",
        blank=True,
    )


class Person(models.Model):

    def __str__(self):
        return self.name

    RSVP_UNKNOWN = 1
    RSVP_ATTENDING = 2
    RSVP_NOT_ATTENDING = 3

    RSVP_CHOICES = (
        (RSVP_UNKNOWN, "No Response"),
        (RSVP_ATTENDING, "Attending"),
        (RSVP_NOT_ATTENDING, "Not attending"),
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    group = models.ForeignKey(Group)
    rsvp_status = models.IntegerField(
        choices=RSVP_CHOICES,
        default=RSVP_UNKNOWN,
    )
    name_flagged = models.BooleanField()
    dietary_restrictions = models.TextField(blank=True)


class Event(models.Model):

    def __str__(self):
        return self.name

    short_name = models.CharField(
        max_length=20,
        help_text="This is used to look up an event, e.g. by the "
                  "group_has_event tag.",
        unique=True,
    )
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    address = models.TextField()
    directions_url = models.CharField(max_length=255)
    description = models.TextField()


class Mailout(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    event = models.ForeignKey(Event)
    subject = models.CharField(max_length=255)
    plain_text = models.TextField()


class MailSent(models.Model):

    def __str__(self):
        return "%s sent to %s" % (self.mailout, self.recipient)

    recipient = models.ForeignKey(Person)
    mailout = models.ForeignKey(Mailout)
    datestamp = models.DateTimeField(default=timezone.now)
