from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseForbidden
from django.shortcuts import render


from reviews.services import (
    get_user_id,
    get_user_reviews,
    get_filters,
    get_tags,
    get_review_details,
    get_selected_tags_ids,
)


def all_reviews(request, username):
    user_id = get_user_id(username)
    tag_filter = request.GET.get('tag_filter', None)
    rating_filter = request.GET.get('rating_filter', None)

    filters = get_filters(tag_filter, rating_filter)

    reviews = get_user_reviews(user_id, filters)

    paginator = Paginator(reviews, 10)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)

    context = {
        'username': username,
        'user_id': user_id,
        'page_obj': page_obj,
        'paginator': paginator,
        'tag_filter': tag_filter,
        'rating_filter': rating_filter,
    }
    return render(request, 'reviews/all_reviews.html', context)


def review_info(request, review_id):
    review = get_review_details(review_id)
    context = {
        'review': review,
    }
    return render(request, 'reviews/review_info.html', context)


@login_required
def create_review(request):
    tags = get_tags()
    context = {
        'tags': tags,
        'ratings': (i for i in range(1, 11))
    }
    return render(request, 'reviews/create_review.html', context)


@login_required
def update_review(request, item_id):
    review = get_review_details(item_id)

    if review.user_id != request.user.id:
        return HttpResponseForbidden(
            'You don\'t have permission to edit this review.'
        )

    tags = get_tags()
    selected_tag_id = get_selected_tags_ids(review)
    context = {
        'review': review,
        'tags': tags,
        'selected_tag_id': selected_tag_id,
        'ratings': (i for i in range(1, 11))
    }
    return render(request, 'reviews/update_review.html', context)
