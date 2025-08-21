from django.urls import path

from api.reviews_api import views

urlpatterns = [
    path(
        'v1/reviews/',
        views.ReviewCreateAPIView.as_view(),
        name='review-list'
    ),
    path(
        'v1/reviews/<int:review_id>/',
        views.ReviewUpdateDeleteAPIView.as_view(),
        name='review-detail'
    ),

    path(
        'v1/reviews/search/',
        views.ReviewSearchAPIView.as_view(),
        name='review-search'
    ),
    path(
        'v1/tags/',
        views.ReviewTagGetAPIView.as_view(),
        name='tag-get'
    ),
]
