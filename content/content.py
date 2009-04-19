from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes import generic
from django.db import connection
from django.contrib.auth.models import User

class ContentModel(models.Model):
  content_type = models.ForeignKey(ContentType)
  object_id = models.IntegerField(_('object ID'))
  content_object = generic.GenericForeignKey('content_type', 'object_id')
  date_created = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  
  def get_content_object(self):
    try:
      return self.content_type.get_object_for_this_type(pk=self.object_id)
    except ObjectDoesNotExist:
      return None
  get_content_object.short_description = _('Content object')

  class Meta:
    abstract = True

  def save(self, user=None, force_insert=False, force_update=False):
    if user:
      if not self.id:
        created_by = user
      else:
        modified_by = user
    super(ContentModel, self).save(force_insert, force_update)

class CanBePrimary(ContentModel):
  """This abstract model is used to handle the commonalities in the supplementary models."""
  comment = models.CharField(max_length=200, blank=True, null=True) # With this we are able to comment on each model
  is_primary = models.BooleanField(default=False)
  def get_property_str(self): return self.is_primary and _("Primary") or _("Secondary")
  primary_str = property(get_property_str)

  class Meta:
    abstract = True

  def save(self, force_insert=False, force_update=False):
    # ".. there can be only one" primary 
    if self.is_primary:
      p = (self._meta.db_table, self.content_type_id, self.object_id)
      sql = "UPDATE %s SET is_primary = 0 WHERE content_type_id =%s AND object_id =%s" % p
      connection.cursor().execute(sql)

    # And for that matter, there HAS to be ONE
    if not self.is_primary:
      ct= self.__class__.objects.count()
      if ct == 0 or (self.id and ct == 1): 
        # Logic is, if this is the first one or the only one set to primar
        self.is_primary = True

    super(CanBePrimary, self).save(force_insert, force_update)

  def delete(self):
    super(CanBePrimary, self).delete()
    if self.is_primary and self.__class__.objects.count():
      # This instance was primary. Now we name a successor.
      i = self.__class__.objects.all()[0] # Get the first in line
      i.is_primary=True
      i.save()
