from django.shortcuts import get_object_or_404

from accounts.models import Account


def get_user_id(username):
    """Return the ID of the user with the given username or raise 404."""
    return get_object_or_404(Account, username=username).id
