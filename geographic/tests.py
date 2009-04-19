"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from globalcontact.geographic.country import Country

class CountryTests(TestCase):
  def setUp(self):
    self.test_country = Country()
    self.test_country.alpha_2 = u'NO'
    self.test_country.alpha_3 = u'NOR'
    self.test_country.name = u"{'no':'Norge','en':'Norway'}"
    self.test_country.phone_countrycode = 47L
    self.test_country._phone_valid_digitcount = u'(8,)'
    self.test_country._phone_formats = u"[ ( (9,4),'+%(ccode)s ### ## ###'), ((2,),'+%(ccode)s ## ## ## ##'),(('#',),'+%(ccode)s #### ####')]"
    self.test_country.phone_format_default = 0L
    self.test_country._address_format = u"['%(postcode_prefix)s-%(postcode)s %(postplace)s','%(country)s']"
    self.test_country.save()

  def test_localized_name(self):
    """
    Tests that the name is valid with different languages
    """
    self.failUnlessEqual(self.test_country.name.get_in_language('no'), "Norge")
    self.failUnlessEqual(self.test_country.name.get_in_language('en'), "Norway")

  def test_phone_formatting(self):
    self.failUnlessEqual(self.test_country.formatted_phone_number(90909090),'+47 909 09 090')
    self.failUnlessEqual(self.test_country.formatted_phone_number(40044000),'+47 400 44 000')
    self.failUnlessEqual(self.test_country.formatted_phone_number(22222222),'+47 22 22 22 22')
    self.failUnlessEqual(self.test_country.formatted_phone_number(55555555),'+47 5555 5555')

  def test_address_formatting(self):
    testaddress = {'postcode_prefix':'NO','postcode':'0001','postplace':'Oslo','country':self.test_country.name}
    self.failUnlessEqual(self.test_country.formatted_address(testaddress), ['NO-0001 Oslo',self.test_country.name])
