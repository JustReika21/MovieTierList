from django.shortcuts import render, get_object_or_404

from items.forms import ItemForm
from items.models import ItemTag, Item
from accounts.models import Account


def all_items(request, username):
    user_id = Account.objects.filter(
        username=username
    ).values_list('id', flat=True).first()
    items = Item.objects.prefetch_related('tags').filter(user=user_id)
    context = {
        'items': items,
    }
    return render(request, 'items/all_items.html', context)


def item_info(request, username, item_id):
    item = get_object_or_404(Item.objects.select_related('user'), id=item_id)
    context = {
        'item': item,
    }
    return render(request, 'items/item_info.html', context)


def create_item(request):
    form = ItemForm
    tags = ItemTag.objects.all()
    context = {
        'form': form,
        'tags': tags,
        'ratings': (i for i in range(1, 11))
    }
    return render(request, 'items/create_item.html', context)
