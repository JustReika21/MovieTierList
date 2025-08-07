from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render

from item_collections.services import (
    get_user_id,
    get_user_items,
    get_user_collections,
    get_collection,
    get_selected_items_ids
)


def all_collections(request, username):
    user_id = get_user_id(username)
    collections = get_user_collections(user_id)

    paginator = Paginator(collections, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)

    context = {
        'username': username,
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


@login_required
def create_collection(request):
    items = get_user_items(request.user.id)
    context = {
        'items': items,
    }
    return render(request, 'item_collections/create_collection.html', context)


@login_required
def update_collection(request, collection_id):
    collection = get_collection(collection_id)

    if collection.user != request.user:
        return HttpResponseForbidden(
            'You don\'t have permission to edit this collection.'
        )

    all_items = get_user_items(request.user.id)
    selected_items_ids = get_selected_items_ids(collection)

    context = {
        'collection': collection,
        'all_items': all_items,
        'selected_items_ids': selected_items_ids,
    }
    return render(request, 'item_collections/update_collection.html', context)
