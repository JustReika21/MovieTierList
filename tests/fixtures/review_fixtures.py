import pytest

from reviews.models import Review, ReviewTag, ReviewType
from tests.factories import TagFactory, ReviewFactory


@pytest.fixture
def create_type():
    def _create(name='Book'):
        return ReviewType.objects.create(name=name)
    return _create


@pytest.fixture
def create_tag():
    def _create(name='Tag'):
        return ReviewTag.objects.create(name=name)
    return _create


@pytest.fixture
def create_tags():
    def _create(count_tags=1):
        return TagFactory.create_batch(count_tags)
    return _create


@pytest.fixture
def create_review():
    def _create(user, title='Review', rating=5):
        return Review.objects.create(
            user=user,
            title=title,
            rating=rating,
        )
    return _create


@pytest.fixture
def fill_data_for_review():
    def _create(
            title='Title', description='Description', rating=1, tags=None,
            review_type=None
    ):
        return {
            'title': title,
            'description': description,
            'rating': rating,
            'tags': [tag.id for tag in tags] if tags else [],
            'type': review_type.id if review_type else [],
        }
    return _create


@pytest.fixture
def create_reviews():
    def _create(count_reviews=1, user=None):
        return ReviewFactory.create_batch(count_reviews, user=user)
    return _create
