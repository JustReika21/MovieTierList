from django.shortcuts import render

from items.forms import ItemForm
from items.models import ItemTag, Item


def create_item(request):
    form = ItemForm
    tags = ItemTag.objects.all()
    context = {
        'form': form,
        'tags': tags,
        'ratings': (i for i in range(1, 11))
    }
    return render(request, 'items/create_item.html', context)


def all_items(request):
    user_id = request.user.id
    items = Item.objects.prefetch_related('tags').filter(user=user_id)
    context = {
        'items': items,
    }
    return render(request, 'items/all_items.html', context)


def item_info(request, item_id):
    item = Item.objects.prefetch_related(
        'tags'
    ).select_related('user').get(id=item_id)
    context = {
        'item': item,
    }
    return render(request, 'items/item_info.html', context)
