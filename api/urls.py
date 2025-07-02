from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path(
        'v1/item/create/',
        views.ItemCreateAPIView.as_view(),
        name='item_create'
    ),
]
