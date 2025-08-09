from django.http import Http404
from django.shortcuts import render

from core.services import get_user_id

from user_profile.services import (
    get_user_reviews,
    get_user_collections
)


def user_profile(request, username):
    user_id = get_user_id(username)

    if not user_id:
        raise Http404('User not found')

    limit = 5
    if request.user.id == user_id:
        limit = 4

    reviews = get_user_reviews(user_id, limit)
    collections = get_user_collections(user_id, limit)

    context = {
        'user_id': user_id,
        'username': username,
        'reviews': reviews,
        'collections': collections,
    }
    return render(request, 'user_profile/profile.html', context)
