from PIL import Image
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from item_collections.models import Collection
from items.models import Item, ItemTag

IMG_FORMATS = ('jpg', 'jpeg', 'png')


def cover_validator(cover):
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


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['title', 'description', 'rating', 'cover', 'tags', 'user']

    def validate_cover(self, cover):
        return cover_validator(cover)

    def validate_tags(self, tags):
        if not tags:
            raise ValidationError('You must chose at least one tag')
        return tags


class UserOwnedItemPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return Item.objects.filter(user=user)


class CollectionSerializer(serializers.ModelSerializer):
    items = UserOwnedItemPKField(many=True, write_only=True)

    items_details = serializers.PrimaryKeyRelatedField(
        source='items',
        many=True,
        read_only=True
    )

    class Meta:
        model = Collection
        fields = [
            'title', 'description', 'cover', 'items', 'items_details', 'user'
        ]

    def validate_cover(self, cover):
        return cover_validator(cover)

    def validate_items(self, items):
        if not items:
            raise ValidationError('You must choose at least one item')
        return items


class ItemTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTag
        fields = '__all__'
