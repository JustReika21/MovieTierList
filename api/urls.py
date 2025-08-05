from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path(
        'v1/items/create/',
        views.ItemCreateAPIView.as_view(),
        name='item_create'
    ),
    path(
        'v1/items/update/<int:item_id>/',
        views.ItemUpdateAPIView.as_view(),
        name='item_update'
    ),
    path(
        'v1/items/delete/<int:item_id>/',
        views.ItemDeleteAPIView.as_view(),
        name='item_delete'
    ),
    path(
        'v1/items/search/',
        views.ItemSearchAPIView.as_view(),
        name='item_search'
    ),

    path(
        'v1/collection/create/',
        views.CollectionCreateAPIView.as_view(),
        name='collection_create'
    ),
    path(
        'v1/collection/update/<int:collection_id>/',
        views.CollectionUpdateAPIView.as_view(),
        name='collection_update'
    ),
    path(
        'v1/collection/delete/<int:collection_id>/',
        views.CollectionDeleteAPIView.as_view(),
        name='collection_delete'
    ),

    path(
        'v1/tags/get/',
        views.ItemTagGetAPIView.as_view(),
        name='tag_get'
    ),
]
