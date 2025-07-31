from accounts.models import Account
from item_collections.models import Collection
from items.models import Item


def get_user_id(username):
    return Account.objects.get(username=username).id


def get_user_items(user_id, limit=5):
    return Item.objects.filter(
        user=user_id
    ).order_by('-id').prefetch_related('tags')[:limit]


def get_user_collections(user_id, limit=5):
    return Collection.objects.filter(
        user=user_id
    ).order_by('-id')[:limit]
