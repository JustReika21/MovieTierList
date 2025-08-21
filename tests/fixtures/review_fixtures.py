import pytest

from reviews.models import Review, ReviewTag
from tests.factories import TagFactory


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
    def _create(title='Title', description='Description', rating=1, tags=None):
        return {
            'title': title,
            'description': description,
            'rating': rating,
            'tags': [tag.id for tag in tags] if tags else [],
        }
    return _create