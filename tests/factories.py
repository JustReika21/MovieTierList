from random import randint
import factory

from movie_tier_list import settings
from review_collections.models import Collection

from reviews.models import ReviewTag, Review


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = 'password'


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ReviewTag

    name = factory.Faker('name')


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    description = factory.Faker('text')
    rating = randint(1, 10)


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Collection

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')
    description = factory.Faker('text')
