from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path(
        'v1/reviews/',
        views.ReviewCreateAPIView.as_view(),
        name='review-list'
    ),
    path(
        'v1/reviews/<int:review_id>',
        views.ReviewUpdateDeleteAPIView.as_view(),
        name='review-detail'
    ),

    path(
        'v1/reviews/search/',
        views.ReviewSearchAPIView.as_view(),
        name='review-search'
    ),

    path(
        'v1/collection/create/',
        views.CollectionCreateAPIView.as_view(),
        name='collection-create'
    ),
    path(
        'v1/collection/update/<int:collection_id>/',
        views.CollectionUpdateAPIView.as_view(),
        name='collection-update'
    ),
    path(
        'v1/collection/delete/<int:collection_id>/',
        views.CollectionDeleteAPIView.as_view(),
        name='collection-delete'
    ),

    path(
        'v1/tags/get/',
        views.ReviewTagGetAPIView.as_view(),
        name='tag-get'
    ),
]
