from time import time

from django.db import models

from items.models import Item
from items.validators import validate_description_length
from movie_tier_list import settings


def cover_upload_to_path(instance, filename):
    img_format = filename.split('.')[-1].lower()
    timestamp = str(time())
    return f'collections/{str(instance.user)}_{timestamp}.{img_format}'


class Collection(models.Model):
    title = models.CharField(max_length=127)
    description = models.TextField(
        blank=True,
        validators=[validate_description_length]
    )
    cover = models.ImageField(
        upload_to=cover_upload_to_path,
        default='collections/default.jpg',
    )
    items = models.ManyToManyField(Item, related_name='collections')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collections',
    )

    def __str__(self):
        return self.title
