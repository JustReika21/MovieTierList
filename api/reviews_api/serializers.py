from rest_framework import serializers

from reviews.models import Review, ReviewTag

from api.services import cover_validator


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'title', 'description', 'rating', 'cover', 'tags', 'user']

    def validate_cover(self, cover):
        return cover_validator(cover)


class ReviewSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'title', 'rating', 'cover']


class ReviewTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewTag
        fields = ['id', 'name']
