from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from ..geographic.country import Country
import re
from ..content.content import ContentModel

class EmailAddress(ContentModel):
  emailaddr = models.EmailField()  #contactinfo = models.ForeignKey(ContactDetails)
  def __unicode__(self):
    return self.emailaddr
  
class PhoneNumber(ContentModel):
  phonenumbertype = models.CharField(max_length=6, choices=(('FAX', _('Fax')), ('WORK', _('Work')),('OFFICE',_('Office')),('MOBILE',_('Mobile')),('DIRECT',_('Direct')),('HOME',_('Home')),))
  country = models.ForeignKey(Country)
  phonenumber = models.PositiveIntegerField()
  comment = models.CharField(max_length=20,null=True)

  def __unicode__(self):
    return self.formated_phone_number()

  def formated_phone_number(self, format_index=0):
    return self.county.formated_phone_number(self.phonenumber, format_index)
  
