from django.urls import path

from items import views

urlpatterns = [
    path('create/', views.create_item, name='create_item'),
]
