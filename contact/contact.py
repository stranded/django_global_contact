from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic

from ..geographic.country import Country
from ..geographic.address import Address
from suplementary import PhoneNumber, EmailAddress, IMAddress, MicroBlog, URLAddress

import re

class Person(models.Model):
  user = models.ForeignKey(User, unique=True, null=True)

  first_name = models.CharField(max_length=200)
  last_name = models.CharField(max_length=200)
  _middle_names = models.CharField(max_length=300, null=True, default='[]') # Stringified list
  gender = models.CharField(max_length=7, choices=(('MALE', _('Male')), ('FEMALE', _('Female')),('UNKNOWN',_('Unknown')),), default='UNKNOWN')
  birthdate = models.DateField(null=True)
  country = models.ForeignKey(CountryData, null=True)

  # Many to one .. these will all be deleted if the person is deleted
  addresses = generic.GenericRelation(Address)
  phonenumbers = generic.GenericRelation(PhoneNumber)
  emails = generic.GenericRelation(EmailAddress)
  ims = generic.GenericRelation(IMAddress)
  microblogs = generic.GenericRelation(MicroBlog)
  urls = generic.GenericRelation(URLAddress)

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
