from django.urls import path

from api.review_collections_api import views

urlpatterns = [
    path(
        'v1/collections/',
        views.CollectionCreateAPIView.as_view(),
        name='collection-list'
    ),
    path(
        'v1/collections/<int:collection_id>',
        views.CollectionUpdateDeleteAPIView.as_view(),
        name='collection-detail'
    ),
]