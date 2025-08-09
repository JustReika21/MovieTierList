from django.urls import path

from review_collections import views

app_name = 'review_collections'

urlpatterns = [
    path(
        '<str:username>/all/',
        views.all_collections,
        name='all-collections'
    ),
    path(
        '<int:collection_id>/',
        views.collection_info,
        name='collection-info'
    ),
    path(
        'create/',
        views.create_collection,
        name='create-collection'
    ),
    path(
        'update/<int:collection_id>/',
        views.update_collection,
        name='update-collection'
    ),
]
