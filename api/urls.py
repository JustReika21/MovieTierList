from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('', include('api.reviews_api.urls')),
    path('', include('api.review_collections_api.urls'))
]
