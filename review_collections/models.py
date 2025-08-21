from uuid import uuid4
from django.db import models

from reviews.models import Review
from reviews.validators import validate_description_length
from movie_tier_list import settings


def cover_upload_to_path(instance, filename):
    img_format = filename.split('.')[-1].lower()
    return f'collections/{uuid4()}.{img_format}'


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
    reviews = models.ManyToManyField(Review, related_name='collections')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collections',
    )

    def __str__(self):
        return self.title
