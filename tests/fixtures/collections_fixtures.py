import pytest

from review_collections.models import Collection
from tests.factories import CollectionFactory, ReviewFactory


@pytest.fixture
def fill_data_for_collection():
    def _create(title='Title', description='Description', reviews=None):
        return {
            'title': title,
            'description': description,
            'reviews': [review.id for review in reviews] if reviews else [],
        }
    return _create


@pytest.fixture
def create_collection():
    def _create(user):
        return Collection.objects.create(
            user=user,
            title='Title',
        )
    return _create


@pytest.fixture
def create_collections():
    def _create(collection_count=1, user=None):
        reviews = ReviewFactory.create_batch(5, user=user)
        collections = CollectionFactory.create_batch(collection_count, user=user)

        for collection in collections:
            collection.reviews.set(reviews)

        return collections
    return _create
