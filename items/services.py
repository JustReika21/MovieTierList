from django.shortcuts import get_object_or_404

from items.models import ItemTag, Item
from accounts.models import Account


def get_user_id(username):
    return Account.objects.get(username=username).id


def get_filters(tag_filter, rating_filter):
    filters = {}

    if tag_filter:
        filters['tags__name'] = tag_filter
    if rating_filter:
        filters['rating'] = rating_filter

    return filters


def get_user_items(user_id, filters):
    return Item.objects.prefetch_related(
        'tags'
    ).filter(user=user_id, **filters).order_by('-id')


def get_item_details(item_id):
    return get_object_or_404(Item.objects.select_related('user'), id=item_id)


def get_item_tags():
    return ItemTag.objects.all()


def get_selected_tags_ids(item):
    return set(item.tags.values_list('id', flat=True))
