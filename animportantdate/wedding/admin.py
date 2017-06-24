from django.contrib import admin
from django.shortcuts import redirect, reverse

from . import models
from . import views


# Register your models here.

@admin.register(models.Person)
@admin.register(models.Event)
class BasicAdmin(admin.ModelAdmin):
    pass


class PersonInline(admin.TabularInline):
    model = models.Person

@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    inlines = [
        PersonInline,
    ]


@admin.register(models.Mailout)
class MailoutAdmin(admin.ModelAdmin):
    fields = ('name', 'event', 'subject', 'plain_text')

    def view_on_site(self, obj):
        return reverse(views.mailout, args=(obj.id,))
