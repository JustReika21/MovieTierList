from django.db.models import Count
from django.shortcuts import get_object_or_404

from accounts.models import Account
from item_collections.models import Collection
from items.models import Item


def get_user_id(username):
    """Return the ID of the user with the given username or raise 404."""
    return get_object_or_404(Account, username=username).id


def get_user_items(user_id, limit=5):
    """
    Retrieve items belonging to the given user ID with the given limit,
    ordered by latest.

    Args:
        user_id (int): ID of the user
        limit (int): Number of items to return

    Returns:
        Queryset[Item]: Items with prefetched tags.
    """
    return Item.objects.prefetch_related('tags').filter(
        user=user_id
    ).order_by('-id')[:limit]


def get_user_collections(user_id, limit=5):
    """
    Retrieve collections belonging to the given user ID with the given
    limit, ordered by latest.

    Args:
        user_id (int): ID of the user
        limit (int): Number of items to return

    Returns:
        Queryset[Collection]: Collections with count items belonging to this
        collection.
    """
    return Collection.objects.filter(
        user=user_id
    ).annotate(count_items=Count('items')).order_by('-id')[:limit]
