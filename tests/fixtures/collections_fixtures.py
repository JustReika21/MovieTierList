import pytest

from review_collections.models import Collection
from tests.factories import ReviewFactory

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
def create_reviews():
    def _create(count_reviews=1, user=None):
        return ReviewFactory.create_batch(count_reviews, user=user)
    return _create