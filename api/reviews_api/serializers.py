from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from reviews.models import Review, ReviewTag

from api.services import cover_validator


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


class ReviewTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTag
        fields = ['id', 'name']
