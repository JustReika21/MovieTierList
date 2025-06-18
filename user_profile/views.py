from django.http import Http404
from django.shortcuts import render

from accounts.models import Account


def user_profile(request, username):
    user_id = Account.objects.filter(
        username=username
    ).values_list('id', flat=True).first()

    if not user_id:
        return Http404('Account not found')

    context = {
        'user_id': user_id,
        'username': username
    }
    return render(request, 'user_profile/profile.html', context)
