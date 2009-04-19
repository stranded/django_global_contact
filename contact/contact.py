from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from globalcontact.geographic.country import Country
from globalcontact.geographic.address import Address
from globalcontact.contact.supplemental import PhoneNumber, EmailAddress, IMAddress, MicroBlog, URLAddress

import re

class Person(models.Model):
  user = models.ForeignKey(User, blank=True, null=True)

  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  _middle_names = models.CharField(max_length=300, null=True, default='[]') # Stringified list
  genderchoices = (('MALE', _('Male')), ('FEMALE', _('Female')),('UNKNOWN',_('Unknown')),)
  gender = models.CharField(max_length=7, choices=genderchoices, default='UNKNOWN')
  birthdate = models.DateField(null=True)
  country = models.ForeignKey(Country, null=True)

  # Many to one .. these will all be deleted if the person is deleted
  addresses = generic.GenericRelation(Address)
  phonenumbers = generic.GenericRelation(PhoneNumber)
  emails = generic.GenericRelation(EmailAddress)
  ims = generic.GenericRelation(IMAddress)
  microblogs = generic.GenericRelation(MicroBlog)
  urls = generic.GenericRelation(URLAddress)

  class Meta:
    unique_together = ("user",)
    verbose_name_plural = _("People")

  # Properties
  def set_middle_names(self, mnlist):
    if not isinstance(mnlist,list): raise TypeError, "Field middle_names accepts only type list."
    self._middle_names = str(mnlist)

  def get_middle_names(self):
    if self._middle_names:
      try:
        return eval(self._middle_names)
      except:
        self._middle_names = '[]'

    return []
  
  middle_names = property(get_middle_names, set_middle_names)
  def __unicode__(self):
    name = self.first_name
    if self.middle_names:
      name += " " + " ".join( self.middle_names )
    name += " " + self.last_name
    return name
