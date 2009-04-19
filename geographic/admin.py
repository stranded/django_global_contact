from django.contrib import admin
import django.forms as forms

from globalcontact.geographic.country import Country
from globalcontact.geographic.address import Address

class CountryAdminForm(forms.ModelForm):
  class Meta:
    model = Country

class CountryAdmin(admin.ModelAdmin):
  form = CountryAdminForm
  fieldsets = [
    ('Country data',      {'fields': [('alpha_2', 'alpha_3'), 'name','phone_countrycode']}),
    ('Phone formating',   {'fields': ['phone_format_default','_phone_formats' ], 'classes': ['collapse']}),
    ('Address formating', {'fields': ['_address_format'], 'classes': ['collapse']}),
  ]
  list_display = ('__unicode__',)

admin.site.register(Country, CountryAdmin)
admin.site.register(Address)
