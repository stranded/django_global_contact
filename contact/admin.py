from django.contrib import admin
from globalcontact.contact.supplemental import PhoneNumber, EmailAddress, IMAddress, MicroBlog, URLAddress
from globalcontact.contact.contact import Person
import django.forms as forms

admin.site.register(PhoneNumber)
admin.site.register(EmailAddress)
admin.site.register(IMAddress)
admin.site.register(MicroBlog)
admin.site.register(URLAddress)
admin.site.register(Person)
