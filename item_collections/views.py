from django.shortcuts import render, get_object_or_404

from accounts.models import Account
from items.models import Item
from item_collections.models import Collection


def all_collections(request, username):
    user_id = Account.objects.filter(
        username=username
    ).values_list('id', flat=True).first()
    collections = Collection.objects.filter(user=user_id).order_by('-id')
    context = {
        'collections': collections,
    }
    return render(request, 'item_collections/all_collections.html', context)


def collection_info(request, username, collection_id):
    collection = get_object_or_404(
        Collection.objects.select_related('user').prefetch_related('items'),
        id=collection_id
    )
    context = {
        'collection': collection,
    }
    return render(request, 'item_collections/collection_info.html', context)


def create_collection(request):
    items = Item.objects.filter(user=request.user).order_by('-id')
    context = {
        'items': items,
    }
    return render(request, 'item_collections/create_collection.html', context)
