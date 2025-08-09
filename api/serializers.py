from PIL import Image
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from review_collections.models import Collection
from reviews.models import Review, ReviewTag

IMG_FORMATS = ('jpg', 'jpeg', 'png')


def cover_validator(cover):
    """
    Validate an uploaded image file.

    Checks:
        - File must not exceed 4MB.
        - Must be a valid image (jpg, jpeg, png).
        - File must be an actual image file.

    Raises:
        ValidationError: If any condition fails.

    Returns:
        File: The validated image file.
    """
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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['title', 'description', 'rating', 'cover', 'tags', 'user']

    def validate_cover(self, cover):
        return cover_validator(cover)

    def validate_tags(self, tags):
        if not tags:
            raise ValidationError('You must chose at least one tag')
        return tags


class ReviewSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'rating', 'cover']


class UserOwnedReviewPKField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        return Review.objects.filter(user=user)


class CollectionSerializer(serializers.ModelSerializer):
    reviews = UserOwnedReviewPKField(many=True, write_only=True)

    review_details = serializers.PrimaryKeyRelatedField(
        source='reviews',
        many=True,
        read_only=True
    )

    class Meta:
        model = Collection
        fields = [
            'title', 'description', 'cover', 'reviews', 'review_details', 'user'
        ]

    def validate_cover(self, cover):
        return cover_validator(cover)

    def validate_reviews(self, reviews):
        if not reviews:
            raise ValidationError('You must choose at least one review')
        return reviews


class ReviewTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTag
        fields = '__all__'
