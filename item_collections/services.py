from django.db.models import Count
from django.shortcuts import get_object_or_404

from accounts.models import Account
from items.models import Item
from item_collections.models import Collection


def get_user_id(username):
    """Return the ID of the user with the given username or raise 404."""
    return get_object_or_404(Account, username=username).id


def get_user_collections(user_id):
    """
    Retrieve collections belonging to the given user ID, ordered by latest.

    Args:
        user_id (int): ID of the user

    Returns:
        Queryset[Collection]: Collections with count items belonging to this
        collection.
    """
    return Collection.objects.filter(
        user=user_id
    ).annotate(count_items=Count('items')).order_by('-id')


def get_collection(collection_id):
    """
    Retrieve collection belonging to the given collection ID or raise 404.

    Args:
        collection_id (int): ID of the collection

    Returns:
        Queryset[Collection]: Collection join with user and with prefetched
        items belonging to this collection.
    """
    return get_object_or_404(
        Collection.objects.select_related('user').prefetch_related('items'),
        id=collection_id
    )


def get_user_items(user_id):
    """Retrieve items belonging to the given user ID, ordered by latest."""
    return Item.objects.filter(user=user_id).order_by('-id')


def get_selected_items_ids(collection):
    """
    Retrieve a set of items IDs associated with the given collection.

    Args:
        collection (QuerySet[Collection]): Collection to retrieve items for.

    Returns:
        set: Set of items IDs
    """
    return set(collection.items.values_list('id', flat=True))
