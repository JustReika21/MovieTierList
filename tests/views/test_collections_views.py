import pytest
from django.urls import reverse


class TestCollectionsViews:
    @pytest.mark.django_db
    def test_00_collections_list_view(
            self, user, user_2, client, create_collections
    ):
        create_collections(11, user)

        response = client.get(
            reverse(
                'review_collections:all-collections',
                kwargs={'username': user.username}
            )
        )

        assert response.status_code == 200
        assert len(response.context['page_obj']) == 10
        assert response.context['paginator'].num_pages == 2

        response = client.get(
            reverse(
                'review_collections:all-collections',
                kwargs={'username': user_2.username}
            )
        )

        assert response.status_code == 200
        assert len(response.context['page_obj']) == 0

    @pytest.mark.django_db
    def test_01_collection_detail(self, user, client, create_collections):
        collection = create_collections(1, user)[0]
        response = client.get(
            reverse(
                'review_collections:collection-info',
                kwargs={'collection_id': collection.id}
            )
        )

        assert response.status_code == 200
        response_collection = response.context['collection']
        assert response_collection.title == collection.title
        assert response_collection.description == collection.description
        assert response_collection.reviews == collection.reviews
        assert response_collection.user == collection.user

    @pytest.mark.django_db
    def test_02_collection_detail_not_exist(self, client):
        response = client.get(
            reverse(
                'review_collections:collection-info',
                kwargs={'collection_id': 999}
            )
        )

        assert response.status_code == 404

    @pytest.mark.django_db
    def test_03_collection_create_login_required(self, client):
        response = client.get(reverse('review_collections:create-collection'))

        assert response.status_code == 302

    @pytest.mark.django_db
    def test_04_collection_authenticated(
            self, user, user_2, auth_user_client, create_reviews
    ):
        reviews = create_reviews(5, user)
        create_reviews(1, user_2)
        response = auth_user_client.get(
            reverse('review_collections:create-collection')
        )

        assert response.status_code == 200
        response_reviews = response.context['reviews']
        assert len(response_reviews) == len(reviews)

        response_ids = {r.id for r in response_reviews}
        expected_ids = {r.id for r in reviews}
        assert response_ids == expected_ids

    @pytest.mark.django_db
    def test_05_update_collection_login_required(
            self, user, client, create_collection
    ):
        collection = create_collection(user)
        response = client.get(
            reverse(
                'review_collections:update-collection',
                kwargs={'collection_id': collection.id}
            )
        )

        assert response.status_code == 302

    @pytest.mark.django_db
    def test_06_update_collection_authenticated(
            self, user, auth_user_client, create_collections
    ):
        collection = create_collections(1, user)[0]
        response = auth_user_client.get(
            reverse(
                'review_collections:update-collection',
                kwargs={'collection_id': collection.id}
            )
        )

        assert response.status_code == 200
        body = response.context['collection']
        assert body.title == collection.title
        assert body.description == collection.description
        assert body.reviews == collection.reviews
        assert body.user == collection.user

    @pytest.mark.django_db
    def test_07_update_collection_by_not_creator(
            self, user, auth_user_client_2, create_collection
    ):
        collection = create_collection(user)
        response = auth_user_client_2.get(
            reverse(
                'review_collections:update-collection',
                kwargs={'collection_id': collection.id}
            )
        )

        assert response.status_code == 403

    @pytest.mark.django_db
    def test_08_update_collection_not_exist(self, auth_user_client):
        response = auth_user_client.get(
            reverse(
                'review_collections:update-collection',
                kwargs={'collection_id': 999}
            )
        )

        assert response.status_code == 404
