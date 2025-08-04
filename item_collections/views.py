from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Count

from accounts.models import Account
from items.models import Item
from item_collections.models import Collection


def get_user_id(username):
    return Account.objects.get(username=username).id


def get_user_collections(user_id):
    return Collection.objects.filter(
        user=user_id
    ).annotate(count_reviews=Count('items')).order_by('-id')


def get_collection(collection_id):
    return get_object_or_404(
        Collection.objects.select_related('user').prefetch_related('items'),
        id=collection_id
    )


def get_user_items(user):
    return Item.objects.filter(user=user).order_by('-id')


def get_selected_items_ids(collection):
    return set(collection.items.values_list('id', flat=True))


def all_collections(request, username):
    user_id = get_user_id(username)
    collections = get_user_collections(user_id)

    paginator = Paginator(collections, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
    }
    return render(request, 'item_collections/all_collections.html', context)


def collection_info(request, collection_id):
    collection = get_collection(collection_id)
    context = {
        'collection': collection,
    }
    return render(request, 'item_collections/collection_info.html', context)


def create_collection(request):
    items = get_user_items(request.user)
    context = {
        'items': items,
    }
    return render(request, 'item_collections/create_collection.html', context)


def update_collection(request, collection_id):
    collection = get_collection(collection_id)

    if collection.user != request.user:
        raise Http404('Collection does not exist')

    all_items = get_user_items(request.user)
    selected_items_ids = get_selected_items_ids(collection)

    context = {
        'collection': collection,
        'all_items': all_items,
        'selected_items_ids': selected_items_ids,
    }
    return render(request, 'item_collections/update_collection.html', context)
