from django.contrib import admin
from ..contact.supplemental import PhoneNumber, EmailAddress
import django.forms as forms

admin.site.register(PhoneNumber)
admin.site.register(EmailAddress)
