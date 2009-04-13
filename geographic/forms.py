import urllib
import urllib2
import re
from django.forms.fields import EMPTY_VALUES, Field
from django.utils.translation import get_language, ugettext, ugettext_lazy as _
from django.forms import ValidationError
from django.utils.encoding import smart_unicode
import re

class CountryField(Field):
  default_error_messages = {
      'illegal_length': _(u'The countrycode %(country_code)s does not comply with ISO 3166-1 alpha_%(alpha_type)s'),
      'unknown_code': _(u'The countrycode %(country_code)s you provided does not exist in the ISO 3166-1 standard'),
  }

  def __init__(self, alpha_type, *args, **kwargs):
    if not alpha_type in (2,3):
      raise AttributeError("Currently only alpha_type 2 and 3 are supported")
    self.alpha_type=alpha_type
    super(CountryField, self).__init__(*args, **kwargs)

  def clean(self, value):
    super(CountryField, self).clean(value)
    if value in EMPTY_VALUES:
      return u''
    value = smart_unicode(value)
    if not len(value) == self.alpha_type:
      raise ValidationError(self.error_messages['unknown_code'] % {'country_code': value})
    try:
      if self.alpha_type == 2:
        cdata = CountryData.objects.get(alpha_2=value)
      else:
        cdata = CountryData.objects.get(alpha_3=value)
    except:
      raise ValidationError(self.error_mess)
    return value
    
  def widget_attrs(self, widget):
      return {}
