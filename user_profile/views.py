from django.http import Http404
from django.shortcuts import render

from accounts.models import Account
from items.models import Item


def user_profile(request, username):
    user_id = Account.objects.filter(
        username=username
    ).values_list('id', flat=True).first()

    if not user_id:
        return Http404 # TODO: FIX

    user_items = Item.objects.filter(user=user_id).prefetch_related('tags')

    context = {
        'user_id': user_id,
        'username': username,
        'user_items': user_items,
    }
    return render(request, 'user_profile/profile.html', context)
