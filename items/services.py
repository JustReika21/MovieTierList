from django.shortcuts import get_object_or_404

from items.models import ItemTag, Item
from accounts.models import Account


def get_user_id(username):
    """Return the ID of the user with the given username or raise 404."""
    return get_object_or_404(Account, username=username).id


def get_filters(tag_filter, rating_filter):
    """
    Construct a dictionary of filters for querying items.

    Args:
        tag_filter (str): Tag name to filter by.
        rating_filter (int): Rating to filter by.

    Returns:
        dict: Query filters for item filtering. (field: filter)
    """
    filters = {}

    if tag_filter:
        filters['tags__name'] = tag_filter
    if rating_filter:
        filters['rating'] = rating_filter

    return filters


def get_user_items(user_id, filters):
    """
    Retrieve all items belonging to the given user with filters,
    ordered by latest.

    Args:
        user_id (int): User ID.
        filters (dict): Query filters for item filtering. (field: filter)

    Returns:
        Queryset[Item]: All items belonging to the given user with filters.
    """
    return Item.objects.prefetch_related(
        'tags'
    ).filter(user=user_id, **filters).order_by('-id')


def get_item_details(item_id):
    """
    Retrieve the details of the given item or raise 404.

    Args:
        item_id (int): Item ID.

    Returns:
        QuerySet[Item]: Item details join with user.
    """
    return get_object_or_404(Item.objects.select_related('user'), id=item_id)


def get_tags():
    """Return QuerySet of all tags"""
    return ItemTag.objects.all()


def get_selected_tags_ids(item):
    """
    Retrieve a set of tag IDs associated with the given item.

    Args:
        item (QuerySet[Item]): Item to retrieve tags for.

    Returns:
        set: Set of tag IDs
    """
    return set(item.tags.values_list('id', flat=True))
