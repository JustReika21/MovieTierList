from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path(
        'v1/item/create/',
        views.ItemCreateAPIView.as_view(),
        name='item_create'
    ),
    path(
        'v1/item/delete/<int:item_id>/',
        views.ItemDeleteAPIView.as_view(),
        name='item_delete'
    )
]
