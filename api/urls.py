from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path(
        'v1/items/',
        views.ItemCreateAPIView.as_view(),
        name='item-list'
    ),
    path(
        'v1/items/<int:item_id>',
        views.ItemUpdateDeleteAPIView.as_view(),
        name='item-detail'
    ),

    path(
        'v1/items/search/',
        views.ItemSearchAPIView.as_view(),
        name='item-search'
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
        views.ItemTagGetAPIView.as_view(),
        name='tag-get'
    ),
]
