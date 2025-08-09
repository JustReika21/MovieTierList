from django.shortcuts import get_object_or_404

from reviews.models import ReviewTag, Review
from accounts.models import Account


def get_user_id(username):
    """Return the ID of the user with the given username or raise 404."""
    return get_object_or_404(Account, username=username).id


def get_filters(tag_filter, rating_filter):
    """
    Construct a dictionary of filters for querying reviews.

    Args:
        tag_filter (str): Tag name to filter by.
        rating_filter (int): Rating to filter by.

    Returns:
        dict: Query filters for review filtering. (field: filter)
    """
    filters = {}

    if tag_filter:
        filters['tags__name'] = tag_filter
    if rating_filter:
        filters['rating'] = rating_filter

    return filters


def get_user_reviews(user_id, filters):
    """
    Retrieve all reviews belonging to the given user with filters,
    ordered by latest.

    Args:
        user_id (int): User ID.
        filters (dict): Query filters for review filtering. (field: filter)

    Returns:
        Queryset[Review]: All reviews belonging to the given user with filters.
    """
    return Review.objects.prefetch_related(
        'tags'
    ).filter(user=user_id, **filters).order_by('-id')


def get_review_details(review_id):
    """
    Retrieve the details of the given review or raise 404.

    Args:
        review_id (int): Review ID.

    Returns:
        QuerySet[review]: Review details join with user.
    """
    return get_object_or_404(Review.objects.select_related('user'), id=review_id)


def get_tags():
    """Return QuerySet of all tags"""
    return ReviewTag.objects.all()


def get_selected_tags_ids(review):
    """
    Retrieve a set of tag IDs associated with the given review.

    Args:
        review (QuerySet[Review]): Review to retrieve tags for.

    Returns:
        set: Set of tag IDs
    """
    return set(review.tags.values_list('id', flat=True))
