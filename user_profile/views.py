from django.http import Http404
from django.shortcuts import render

from accounts.models import Account
from item_collections.models import Collection
from items.models import Item


def user_profile(request, username):
    user_id = Account.objects.filter(
        username=username
    ).values_list('id', flat=True).first()

    if not user_id:
        raise Http404('User not found')

    user_items = Item.objects.filter(
        user=user_id
    ).order_by('-id').prefetch_related('tags')[:5]

    user_collections = Collection.objects.filter(
        user=user_id
    ).order_by('-id')[:5]

    context = {
        'user_id': user_id,
        'username': username,
        'user_items': user_items,
        'user_collections': user_collections,
    }
    return render(request, 'user_profile/profile.html', context)
