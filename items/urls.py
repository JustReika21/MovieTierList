from django.urls import path

from items import views

app_name = 'items'

urlpatterns = [
    path('info/<int:item_id>', views.item_info, name='item_info'),
    path('create/', views.create_item, name='create_item'),
    path('all/', views.all_items, name='all_items'),
]
