from django.urls import path

from user_profile import views

app_name = 'user_profile'

urlpatterns = [
    path('<str:username>/', views.user_profile, name='user-profile'),
]
