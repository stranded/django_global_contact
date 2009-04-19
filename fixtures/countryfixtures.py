#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

def run():
    from globalcontact.geographic.country import Country

    geographic_country_1 = Country()
    geographic_country_1.alpha_2 = u'NO'
    geographic_country_1.alpha_3 = u'NOR'
    geographic_country_1.name = u"{'no':'Norge','en':'Norway'}"
    geographic_country_1.phone_countrycode = 47L
    geographic_country_1._phone_valid_digitcount = u'(8,)'
    geographic_country_1._phone_formats = u"[ ( (9,4),'+%(ccode)s ### ## ###'), ((2,),'+%(ccode)s ## ## ## ##'),(('#',),'+%(ccode)s #### ####')]"
    geographic_country_1.phone_format_default = 0L
    geographic_country_1._address_format = u"['%(postcode_prefix)s-%(postcode)s %(postplace)s','%(country)s']"
    geographic_country_1.save()

