from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from store.models import Product
# Create your models here.

class TaggedItemManager(models.Manager):
    def get_tags_for(self,obj_type,object_id):
        content_type = ContentType.objects.get_for_model(obj_type)

        query_set = TaggedItem.objects \
            .select_related('tag') \
            .filter(content_type = content_type, object_id = object_id)
        return query_set
    
class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.label

class TaggedItem(models.Model):
    objects = TaggedItemManager()
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    #TYPE(product,video,article)
    content_type = models.ForeignKey(ContentType, models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey() #actual object the tag is applied to