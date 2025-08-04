from django.shortcuts import get_object_or_404

from items.models import ItemTag, Item
from accounts.models import Account


def get_user_id(username):
    return Account.objects.get(username=username).id


def get_user_items(user_id, tag_filter=None):
    if tag_filter:
        items = Item.objects.prefetch_related(
            'tags'
        ).filter(user=user_id, tags__name=tag_filter)
    else:
        items = Item.objects.prefetch_related('tags').filter(user=user_id)

    return items


def get_item_details(item_id):
    return get_object_or_404(Item.objects.select_related('user'), id=item_id)


def get_item_tags():
    return ItemTag.objects.all()


def get_selected_tags_ids(item):
    return set(item.tags.values_list('id', flat=True))
