from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from review_collections.models import Collection
from reviews.models import Review

from api.services import cover_validator


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
