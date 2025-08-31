import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestReviewViews:
    def test_00_review_list(self, user, user_2, client, create_reviews):
        create_reviews(11, user)

        response = client.get(
            reverse('reviews:all-reviews', kwargs={'username': user.username}),
        )

        assert response.status_code == 200
        assert len(response.context['page_obj']) == 10
        assert response.context['paginator'].num_pages == 2

        response = client.get(
            reverse('reviews:all-reviews', kwargs={'username': user_2.username}),
        )

        assert response.status_code == 200
        assert 'page_obj' in response.context
        assert len(response.context['page_obj']) == 0
        assert response.context['paginator'].num_pages == 1

    def test_01_review_detail(self, user, client, create_review):
        review = create_review(user, 'Title', 10)

        response = client.get(
            reverse('reviews:review-info', kwargs={'review_id': review.id})
        )

        assert response.status_code == 200
        response_review = response.context['review']
        assert response_review.title == review.title
        assert response_review.description == review.description
        assert response_review.rating == review.rating
        assert response_review.user == review.user

    def test_02_review_detail_not_exist(self, client):
        response = client.get(
            reverse('reviews:review-info', kwargs={'review_id': 999})
        )

        assert response.status_code == 404

    def test_03_create_review_login_required(self, client):
        response = client.get(reverse('reviews:create-review'))

        assert response.status_code == 302

    def test_04_create_review_authenticated(self, auth_user_client):
        response = auth_user_client.get(reverse('reviews:create-review'))

        assert response.status_code == 200

    def test_05_update_review_login_required(self, user, client, create_review):
        review = create_review(user)
        response = client.get(reverse(
            'reviews:update-review', kwargs={'review_id': review.id})
        )

        assert response.status_code == 302

    def test_06_update_review_authenticated(
            self, user, auth_user_client, create_review
    ):
        review = create_review(user)
        response = auth_user_client.get(reverse(
            'reviews:update-review', kwargs={'review_id': review.id})
        )

        assert response.status_code == 200
        body = response.context['review']
        assert body.title == review.title
        assert body.description == review.description
        assert body.rating == review.rating
        assert body.tags == review.tags
        assert body.type == review.type
        assert body.user == review.user

    def test_07_update_review_by_not_creator(
            self, user, auth_user_client_2, create_review
    ):
        review = create_review(user)
        response = auth_user_client_2.get(
            reverse('reviews:update-review', kwargs={'review_id': review.id})
        )

        assert response.status_code == 403

    def test_08_update_review_not_exist(self, auth_user_client):
        response = auth_user_client.get(
            reverse('reviews:update-review', kwargs={'review_id': 999})
        )

        assert response.status_code == 404
