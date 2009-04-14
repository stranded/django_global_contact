from django.contrib import admin
from country import Country
import django.forms as forms

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