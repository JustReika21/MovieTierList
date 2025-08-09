from time import time

from django.db import models

from movie_tier_list import settings
from reviews.validators import validate_description_length


def cover_upload_to_path(instance, filename):
    img_format = filename.split('.')[-1].lower()
    timestamp = str(time())
    return f'reviews/{str(instance.user)}_{timestamp}.{img_format}'


class ReviewTag(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class ReviewType(models.Model):
    name = models.CharField(max_length=127)

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.CharField(max_length=127)
    description = models.TextField(
        blank=True,
        validators=[validate_description_length]
    )
    rating = models.SmallIntegerField(choices=((i, i) for i in range(1, 11)))
    cover = models.ImageField(
        upload_to=cover_upload_to_path,
        default='reviews/default.jpg',
    )
    tags = models.ManyToManyField(ReviewTag, blank=True, related_name='reviews')
    # type = models.ForeignKey(ReviewType, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )

    def __str__(self):
        return self.title
