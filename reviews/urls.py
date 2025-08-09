from django.urls import path

from reviews import views

app_name = 'reviews'

urlpatterns = [
    path(
        '<str:username>/all/',
        views.all_reviews,
        name='all-reviews'
    ),
    path(
        'info/<int:review_id>/',
        views.review_info,
        name='review-info'
    ),
    path(
        'create/',
        views.create_review,
        name='create-review'
    ),
    path(
        'update/<int:item_id>/',
        views.update_review,
        name='update-review'
    ),
]
