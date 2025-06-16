from django.urls import path
from core import views

app_name = 'core'

handler403 = views.custom_handler403
handler404 = views.custom_handler404
handler500 = views.custom_handler500

urlpatterns = [
    path('', views.home, name='home'),
]
