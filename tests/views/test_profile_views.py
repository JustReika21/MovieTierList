import pytest
from django.urls import reverse


class TestProfileViews:
    @pytest.mark.django_db
    def test_00_profile_view_by_owner(
            self, user, auth_user_client, auth_user_client_2,
            create_reviews, create_collections
    ):
        create_reviews(10, user)
        create_collections(10, user)

        response = auth_user_client.get(
            reverse(
                'user_profile:user-profile',
                kwargs={'username': user.username}
            )
        )

        assert response.status_code == 200
        assert response.context['username'] == user.username
        assert len(response.context["reviews"]) == 4
        assert len(response.context["collections"]) == 4

    @pytest.mark.django_db
    def test_01_profile_by_another_person(
            self, user, auth_user_client, auth_user_client_2,
            create_reviews, create_collections
    ):
        create_reviews(10, user)
        create_collections(10, user)

        response = auth_user_client_2.get(
            reverse(
                'user_profile:user-profile',
                kwargs={'username': user.username}
            )
        )

        assert response.status_code == 200
        assert response.context['username'] == user.username
        assert len(response.context["reviews"]) == 5
        assert len(response.context["collections"]) == 5

    @pytest.mark.django_db
    def test_02_profile_not_exist(self, client):
        response = client.get(
            reverse(
                'user_profile:user-profile',
                kwargs={'username': 'not_exist_account'}
            )
        )

        assert response.status_code == 404
