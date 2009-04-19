from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from globalcontact.geographic.country import Country
from globalcontact.content.content import CanBePrimary
import re

class EmailAddress(CanBePrimary):
  emailtype = models.CharField(max_length=10, choices=(('PUBLIC',_('Public')),('PRIVATE',_('Private'))), default='PRIVATE' )
  emailaddr = models.EmailField() 
  class Meta(CanBePrimary.Meta):
    verbose_name_plural = _("Email Addresses")

  def __unicode__(self):
    return u"%s (%s)" % (self.emailaddr, self.primary_str)
  
class PhoneNumber(CanBePrimary):
  phonenumbertype = models.CharField(max_length=6, choices=(('FAX', _('Fax')), ('WORK', _('Work')),('OFFICE',_('Office')),('MOBILE',_('Mobile')),('DIRECT',_('Direct')),('HOME',_('Home')),))
  country = models.ForeignKey(Country)
  phonenumber = models.PositiveIntegerField()
  class Meta(CanBePrimary.Meta):
    verbose_name_plural = _("Phone Numbers")

  def __unicode__(self):
    return u"%s (%s)" % (self.formatted_phone_number(), self.primary_str)

  def formatted_phone_number(self, format_index=0):
    return self.county.formatted_phone_number(self.phonenumber, format_index)
  
class IMAddress(CanBePrimary):
  imchoices = ( # Types taken from http://en.wikipedia.org/wiki/Instant_messaging
                ('AIM',_('AOL Instant Messenger')),
                ('EBUDDY',_('eBuddy')),
                ('GADUGADU',_('Gadu-Gadu')),
                ('SAMETIME',_('IBM Lotus Sametime')),
                ('ICQ',_('ICQ')),
                ('IMVU',_('IMVU')),
                ('XMPP',_('Jabber')),
                ('GOOGLETALK',_('Google Talk')),
                ('MRA',_('Mail.ru Agent')),
                ('MEEBO',_('Meebo')),
                ('MUNDU',_('Mundu Messenger')),
                ('MXIT',_('MXit')),
                ('PALTALK',_('Paltalk')),
                ('PSYC',_('PSYC')),
                ('SKYPE',_('Skype')),
                ('TENCENTQQ',_('Tencent QQ')),
                ('VZO',_('VZOchat')),
                ('MSN',_('Windows Live Messenger (MSN)')),
                ('XFIRE',_('Xfire')),
                ('YAHOO',_('Yahoo! Messenger')),
              )
  imtype = models.CharField(max_length=15, choices=imchoices )
  account = models.CharField(max_length=200)
  class Meta(CanBePrimary.Meta):
    verbose_name_plural = _("IM Addresses")

  def __unicode__(self):
    return "IM [%s] %s (%s)" % (self.get_imtype_display(), self.account, self.primary_str)

class MicroBlog(CanBePrimary):
  microblogchoices = (
    ('TWITTER',_('Twitter')),
    ('POWNCE',_('Pownce')),
    ('JAIKU',_('Jaiku')),
  )
  microblogtype = models.CharField(max_length=15, choices=microblogchoices)
  address = models.CharField(max_length=200)
  class Meta(CanBePrimary.Meta):
    verbose_name_plural = _("Micro Blogs")

  def __unicode__(self):
    return u"Micro Blog [%s] %s (%s)" % (self.get_microblogtype_display(), self.address, self.primary_str)

class URLAddress(CanBePrimary):
  urlchoices = (
    ('CORPORATE',_('Corporate Website')),
    ('BLOG',_('Personal Blog')),
    ('OTHER',_('Other Website')),
  )
  urltype = models.CharField(max_length=15, choices=urlchoices, default='OTHER')
  url = models.URLField()
  class Meta(CanBePrimary.Meta):
    verbose_name = _("URL Address")
    verbose_name_plural = _("URL Addresses")
  
  def __unicode__(self):
    return u"URL [%s] %s (%s)" % (self.get_urltype_display(), self.url, self.primary_str)

