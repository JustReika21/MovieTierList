from time import time

from django.db import models

from movie_tier_list import settings
from items.validators import validate_description_length


IMG_FORMATS = ('jpg', 'jpeg', 'png')


def cover_upload_to_path(instance, filename):
    img_format = filename.split('.')[-1].lower()
    timestamp = str(time())
    return f'items/{str(instance.user)}_{timestamp}.{img_format}'


class ItemTag(models.Model):
    name = models.CharField(max_length=127)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tags',
    )

    def __str__(self):
        return self.name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_item_tag'
            ),
        ]


class Item(models.Model):
    title = models.CharField(max_length=127)
    description = models.TextField(
        blank=True,
        validators=[validate_description_length]
    )
    rating = models.SmallIntegerField(choices=((i, i) for i in range(1, 11)))
    cover = models.ImageField(
        upload_to=cover_upload_to_path,
        default='items/default.jpg',
    )
    tags = models.ManyToManyField(ItemTag, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='items',
    )

    def __str__(self):
        return self.title
