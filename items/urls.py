from django.urls import path

from items import views

app_name = 'items'

urlpatterns = [
    path('<str:username>/all/', views.all_items, name='all-items'),
    path(
        'info/<int:item_id>/',
        views.item_info,
        name='item-info'
    ),
    path('create/', views.create_item, name='create-item'),
    path(
        'update/<int:item_id>/',
        views.update_item,
        name='update-item'
    ),
]
