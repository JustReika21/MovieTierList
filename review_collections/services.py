from django.db.models import Count
from django.shortcuts import get_object_or_404

from reviews.models import Review
from review_collections.models import Collection


def get_user_collections(user_id):
    """
    Retrieve collections belonging to the given user ID, ordered by latest.

    Args:
        user_id (int): ID of the user

    Returns:
        Queryset[Collection]: Collections with count reviews belonging to this
        collection.
    """
    return Collection.objects.filter(
        user=user_id
    ).annotate(count_reviews=Count('reviews')).order_by('-id')


def get_collection(collection_id):
    """
    Retrieve collection belonging to the given collection ID or raise 404.

    Args:
        collection_id (int): ID of the collection

    Returns:
        Queryset[Collection]: Collection join with user and with prefetched
        reviews belonging to this collection.
    """
    return get_object_or_404(
        Collection.objects.select_related('user').prefetch_related(
            'reviews',
        ).annotate(count_reviews=Count('reviews')),
        id=collection_id,
    )


def get_collection_with_review_info(collection_id):
    """
    Retrieve collection with review types and tags belonging to the given
    collection ID or raise 404.

    Args:
        collection_id (int): ID of the collection

    Returns:
        Queryset[Collection]: Collection join with user and with prefetched
        reviews belonging to this collection.
    """
    return get_object_or_404(
        Collection.objects.select_related('user').prefetch_related(
            'reviews', 'reviews__type', 'reviews__tags'
        ).annotate(
            count_reviews=Count('reviews')
        ),
        id=collection_id
    )


def get_user_reviews(user_id):
    """
    Retrieve reviews ids and titles belonging to the given user ID, ordered by
    latest.

    Args:
        user_id (int): ID of the user

    Returns:
        Queryset[Review]: Reviews ids and titles
    """
    return Review.objects.filter(
        user=user_id
    ).only('id', 'title').order_by('-id')


def get_selected_review_ids(collection):
    """
    Retrieve a set of reviews IDs associated with the given collection.

    Args:
        collection (QuerySet[Collection]): Collection to retrieve reviews for.

    Returns:
        set: Set of reviews IDs
    """
    return set(collection.reviews.values_list('id', flat=True))
