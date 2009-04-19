import urllib
import urllib2
import re
from django.db import models
from django.forms.fields import EMPTY_VALUES, Field
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from django.forms import ValidationError
import re
import django.forms as forms

#dependency: http://code.google.com/p/transdb/
import transdb

class CountryManager(models.Manager):
  pass
  
class Country(models.Model):
  alpha_2 = models.CharField(max_length=2) # http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
  alpha_3 = models.CharField(max_length=3) # http://en.wikipedia.org/wiki/ISO_3166-1_alpha-3
  name = transdb.TransCharField(max_length=250)
  phone_countrycode = models.IntegerField() # http://en.wikipedia.org/wiki/List_of_country_calling_codes
  _phone_valid_digitcount = models.CharField(max_length=10, null=True, verbose_name=_("Phone Valid Digit Count")) # A stringified tupple of possible lengths
  _phone_formats = models.CharField(max_length=200, verbose_name=_('Phone Formats'), default='[]', help_text=_("Make sure it is a valid stringified list with tupples in format: [ ( (9,4),'+%(ccode)s ### ## ###'), ((2,'#'),'+%(ccode)s ## ## ## ##')]. This would producte formatting +47 22 22 22 22 and +47 900 11 000 in Norway. The first # encountered in the match digits is used as default."))
  phone_format_default = models.IntegerField(default=0) # 0 based index from phone_formats
  _address_format = models.CharField(max_length=300, null=True, verbose_name=_('Address Format'), help_text=_("eg. ['%(postcode_prefix)s-%(postcode)s %(postplace)s','%(country)s'] would be correct for Norway. Make it a stringified list.")) # stored as a stringified list.
  # Example address format ['%(postcode_prefix)s-%(postcode)s','%(country)s'] . Lines are added as is.

  class Meta:
    verbose_name_plural = _("Countries") # Looks better in Admin

  def __unicode__(self):
    localname = self.name
    return "%s (%s)" % (localname,self.alpha_2)

  def _get_phone_formats(self):
    try:
      phoneformats = eval(self._phone_formats)
    except:
      # The phone format is not legal .. so we just return empty
      phoneformats = []
    return phoneformats
      
  def _set_phone_formats(self, phoneformats):
    if not isinstance(phoneformats, list):
      raise TypeError, _(u"Phone formats must be in list format")
    self._phone_format = str(phoneformats)
  
  phone_formats = property(_get_phone_formats, _set_phone_formats)

  def _get_phone_valid_digitcount(self):
    try:
      tdigits = eval(self._phone_valid_digitcount)
    except:
      if self.phone_formats:
        # We try to harness the length from the formatting
        alengths = []
        for format in self.phone_formats:
          alengths.append(len(re.findall('#',format[1])))
        self._phone_valid_digitcount = tuple(alengths)
        self.save()

  def _set_phone_valid_digitcount(self, tdigits):
    pass

  phone_valid_digitcount = property(_get_phone_valid_digitcount, _set_phone_valid_digitcount)

  def default_phone_formats(self):
    try:
      return self.phoneformats[self.phone_format_default]
    except:
      return '' # If there is no 

  def formatted_phone_number(self,phonenumber, formatindex=0):
    if len(self.phone_formats) == 0:
      return str(phonenumber)

    # 1. Find which format to use
    preformat = ""
    for format in self.phone_formats:
      for pre in format[0]:
        spre = str(pre)
        if spre == '#' or spre == str(phonenumber)[:len(spre)]: 
          preformat = format[1]
          break
      if preformat: break


    # Check if the number is international
    preformat = preformat % {'ccode': str(self.phone_countrycode)}
    digits = re.findall('\d',str(phonenumber))
    formatted_number=""
    for c in preformat:
      if c == '#':
        formatted_number += digits.pop(0)
      else:
        formatted_number += c

    return formatted_number

  def _get_address_format(self):
    try:
      addressformat = eval(self._address_format)
    except:
      # The phone format is not legal .. so we just return empty
      addressformat = []
    return addressformat

  def _set_address_format(self, addressformat):
    if not isinstance(addressformat, list):
      raise TypeError, _(u"Must be in list format")
    self.address_format = str(addressformat)

  address_format = property(_get_address_format, _set_address_format)

  def formatted_address(self, address):
    """Returns a list of lines representing the formatted lines in the address"""
    fa = []
    for line in self.address_format:
      fa.append( line % address )
    return fa

  objects = CountryManager()

