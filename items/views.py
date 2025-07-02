from django.shortcuts import render

from items.forms import ItemForm
from items.models import ItemTag


def create_item(request):
    form = ItemForm
    tags = ItemTag.objects.all()
    context = {
        'form': form,
        'tags': tags,
        'ratings': (i for i in range(1, 11))
    }
    return render(request, 'items/create_item.html', context)
