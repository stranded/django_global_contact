from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.db import connection

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

class CanBePrimary(ContentModel):
  """This abstract model is used to handle the commonalities in the supplementary models."""
  comment = models.CharField(max_length=200, null=True) # With this we are able to comment on each model
  is_primary = models.BooleanField(default=False)
  class Meta:
    abstract = True

  def save(self, force_insert=False, force_update=False):
   # ".. there can be only one" primary 
    p = [self._meta.db_table, self.content_type, self.object_id]
    connection.cursor().execute("UPDATE %s SET is_primary = 0 WHERE content_type =%s' AND object_id = '%s'", p)
    super(CanBePrimary, self).save(force_insert, force_update)

