from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic

class ContentModel(models.Model):
  content_type = models.ForeignKey(ContentType)
  object_id = models.IntegerField(_('object ID'))
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  
  def get_content_object(self):
    try:
      return self.content_type.get_object_for_this_type(pk=self.object_id)
    except ObjectDoesNotExist:
      return None
  get_content_object.short_description = _('Content object')
  class Meta:
    abstract = True
