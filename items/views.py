from django.core.paginator import Paginator
from django.shortcuts import render


from items.services import (
    get_user_items,
    get_user_id,
    get_item_tags,
    get_item_details,
    get_selected_tags_ids,
)


def all_items(request, username):
    user_id = get_user_id(username)
    tag_filter = request.GET.get('tag_filter', None)
    items = get_user_items(user_id, tag_filter).order_by('-id')

    paginator = Paginator(items, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)

    context = {
        'username': username,
        'page_obj': page_obj,
        'paginator': paginator,
        'tag_filter': tag_filter,
    }
    return render(request, 'items/all_items.html', context)


def item_info(request, item_id):
    item = get_item_details(item_id)
    context = {
        'item': item,
    }
    return render(request, 'items/item_info.html', context)


def create_item(request):
    tags = get_item_tags()
    context = {
        'tags': tags,
        'ratings': (i for i in range(1, 11))
    }
    return render(request, 'items/create_item.html', context)


def update_item(request, item_id):
    item = get_item_details(item_id)
    tags = get_item_tags()
    selected_tag_id = get_selected_tags_ids(item)
    context = {
        'item': item,
        'tags': tags,
        'selected_tag_id': selected_tag_id,
        'ratings': (i for i in range(1, 11))
    }
    return render(request, 'items/update_item.html', context)
