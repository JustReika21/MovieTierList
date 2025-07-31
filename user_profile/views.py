from django.http import Http404
from django.shortcuts import render

from user_profile.services import (
    get_user_id,
    get_user_items,
    get_user_collections
)


def user_profile(request, username):
    user_id = get_user_id(username)

    if not user_id:
        raise Http404('User not found')

    user_items = get_user_items(user_id)

    user_collections = get_user_collections(user_id)

    context = {
        'user_id': user_id,
        'username': username,
        'user_items': user_items,
        'user_collections': user_collections,
    }
    return render(request, 'user_profile/profile.html', context)
