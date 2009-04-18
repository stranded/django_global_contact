from django.contrib import admin
from ..contact.supplemental import PhoneNumber, EmailAddress, IMAddress, MicroBlog, URLAddress
import django.forms as forms

admin.site.register(PhoneNumber)
admin.site.register(EmailAddress)
admin.site.register(IMAddress)
admin.site.register(MicroBlog)
admin.site.register(URLAddress)
