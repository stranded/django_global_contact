from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.contrib.localflavor.us.models import USStateField

from globalcontact.geographic.country import Country
from globalcontact.content.content import ContentModel


class AddressLine(ContentModel):
  linedata = models.CharField(max_length=75)
  lineorder = models.IntegerField()
  class Meta:
    ordering = ['lineorder']
  def __unicode__(self):
    return self.linedata

class Address(ContentModel):
  addresstype = models.CharField(max_length=6, choices=(('POST', _('Post Address')), ('VISIT', _('Visit Address')),('BILLING',_('Billing Address')),('OTHER',_('Other Address'))))
  country = models.ForeignKey(Country)
  city = models.CharField(max_length=50)
  state = USStateField(null=True)
  locationcode = models.CharField(max_length=10) # Postnr, Zip code, etc
  
  latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
  longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)

  comment = models.CharField(max_length=200, null=True)
  # By adding a reverse generic relation we ensure that the lines are deleted when 
  # the address is deleted
  _lines = generic.GenericRelation(AddressLine)
  class Meta(ContentModel.Meta):
    # Ensuring that we can only have one of each type address on a single model. This to simplify logic later
    unique_together = ("content_type", "object_id", "addresstype")
    verbose_name_plural = "Addresses"

  def add_line(self, line):
    index = self._lines.count()
    newline = self._lines.create(linedata=line,lineorder=index)
    return newline

  def _get_lines(self):
    # For ease of use in templates
    lines = []
    for line in self._lines.all():
      lines.append(line.linedata)

    return lines

  lines = property(_get_lines)
    
  def __getitem__(self, key):
    """This is used for formating. When passing the address object to country for formatting, 
    string formating is passed through this function.
    """ 
    if key in ('postplace','city'):
      return self.city
    elif key in ('postcode','locationcode','zip'):
      return self.locationcode
    elif key == 'country' or key == 'country_name':
      return self.country.name
    elif key == 'postcode_prefix':
      return self.country.alpha_2
    elif key == 'state':
      return self.state
    
    raise KeyError, "Unknown key %s" % key
    
  def formatted(self):
    return self.lines + self.country.formatted_address(self)
    
  def __unicode__(self):
    return u", ".join( self.formatted() )
  
