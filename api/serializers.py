from PIL import Image
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from items.models import Item

IMG_FORMATS = ('jpg', 'jpeg', 'png')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['title', 'description', 'rating', 'cover', 'tags', 'user']

    def validate_cover(self, cover):
        if not cover:
            return

        if cover.size > 4 * 1024 * 1024:
            raise ValidationError('Cover must be less than 4 mb')

        try:
            img = Image.open(cover)
            img.verify()
        except Exception:
            raise ValidationError('Uploaded file is not a valid image')

        img_format = img.format.lower()
        if img_format not in IMG_FORMATS:
            raise ValidationError(
                'Cover must be one of this formats: ' + ', '.join(IMG_FORMATS)
            )

        return cover
