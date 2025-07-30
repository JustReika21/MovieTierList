from django.urls import path

from item_collections import views

app_name = 'item_collections'

urlpatterns = [
    path('<str:username>/all/', views.all_collections, name='all_collections'),
    path(
        '<int:collection_id>/',
        views.collection_info,
        name='collection_info'
    ),
    path('create/', views.create_collection, name='create_collection'),
    path(
        '/<int:collection_id>/update/',
        views.update_collection,
        name='update_collection'
    ),
]
