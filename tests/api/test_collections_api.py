import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestCollectionsApi:
    default_cover = 'default.jpg'
    invalid_image_size = 'invalid_image_size.png'
    valid_image = 'valid_image.jpg'
    valid_image2 = 'valid_image2.png'
    valid_image3 = 'valid_image3.jpeg'

    def test_00_create_collection_not_auth(
            self, client, fill_data_for_collection
    ):
        data = fill_data_for_collection(
            'Title', 'Description'
        )
        response = client.post(reverse('api:collection-list'), data=data)
        assert response.status_code == 403, response.data

    @pytest.mark.parametrize('title, description', [
        ('A' * 128, 'Description'),
        ('', 'Description'),
        ('Title', 'A' * 1025),
    ])
    def test_01_create_collection_with_invalid_data(
            self, user, auth_user_client, fill_data_for_collection,
            create_reviews, title, description
    ):
        reviews = create_reviews(2, user)
        data = fill_data_for_collection(title, description, reviews)
        response = auth_user_client.post(reverse('api:collection-list'), data=data)
        assert response.status_code == 400, response.data

    def test_02_create_review_with_invalid_cover_size(
            self, user, auth_user_client, fill_data_for_collection,
            open_image_file, create_reviews
    ):
        big_img = open_image_file(self.invalid_image_size)
        data = fill_data_for_collection(
            'title', 'description', create_reviews(1, user)
        )
        data['cover'] = big_img
        response = auth_user_client.post(
            reverse('api:collection-list'),
            data=data,
            format='multipart'
        )
        assert response.status_code == 400, response.data

    @pytest.mark.parametrize('title, description', [
        ('Title', 'Description'),
        ('Название', 'Описание'),
        ('А' * 127, 'A' * 1024),
        ('А', ''),
    ])
    def test_03_create_collection_with_valid_data(
            self, user, auth_user_client, fill_data_for_collection,
            create_reviews, title, description
    ):
        reviews = create_reviews(5, user)

        data = fill_data_for_collection(title, description, reviews)
        response = auth_user_client.post(
            reverse('api:collection-list'),
            data=data
        )
        assert response.status_code == 201, response.data
        body = response.json()
        assert body['title'] == title
        assert body['description'] == description
        assert body['review_details'] == [review.id for review in reviews]
        assert body['cover'].split('/')[-1] == self.default_cover

    @pytest.mark.parametrize('cover_name', [
        valid_image,
        valid_image2,
        valid_image3,
    ])
    def test_04_create_valid_collection_with_cover(
        self, auth_user_client, create_tags, fill_data_for_collection,
        open_image_file, cover_name
    ):
        img = open_image_file(cover_name)
        data = fill_data_for_collection('Title', 'Description')
        data['cover'] = img
        response = auth_user_client.post(
            reverse('api:collection-list'),
            data=data,
            format='multipart'
        )
        assert response.status_code == 201, response.data
        body = response.json()
        assert body['cover'].split('/')[-1] != 'default.jpg'

        response = auth_user_client.delete(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': response.json()['id']}
            )
        )
        assert response.status_code == 204, response.data

    @pytest.mark.parametrize('title, description', [
        ('Updated', 'Review'),
        ('Title', 'Description'),
        ('Название', 'Описание'),
        ('А' * 127, 'A' * 1024),
        ('А', ''),
    ])
    def test_05_update_collection_with_valid_data_by_creator(
            self, user, auth_user_client, create_collection, create_reviews,
            fill_data_for_collection, title, description,
    ):
        collection = create_collection(user)
        reviews = create_reviews(5, user)
        data = fill_data_for_collection(title, description, reviews)

        response = auth_user_client.patch(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': collection.id}
            ),
            data=data,
        )

        body = response.json()
        assert response.status_code == 200, body
        assert body['title'] == data['title']
        assert body['description'] == data['description']
        assert body['review_details'] == [review.id for review in reviews]
        assert body['cover'].split('/')[-1] == self.default_cover

    def test_06_update_cover_valid(
            self, user, auth_user_client, create_collection, open_image_file
    ):
        collection = create_collection(user)
        data = {'cover': open_image_file(self.valid_image)}
        response = auth_user_client.patch(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': collection.id}
            ),
            data=data,
            format='multipart'
        )
        assert response.status_code == 200, response.data
        body = response.json()
        assert body['cover'].split('/')[-1] != self.default_cover

        response = auth_user_client.delete(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': collection.id}
            ),
        )
        assert response.status_code == 204, response.data

    @pytest.mark.parametrize('title, description', [
        ('A' * 128, 'Description'),
        ('', 'Description'),
        ('Title', 'A' * 1025),
    ])
    def test_07_update_with_invalid_data(
            self, user, auth_user_client, create_collection,
            fill_data_for_collection, create_reviews, title, description
    ):
        collection = create_collection(user)
        data = fill_data_for_collection(
            title, description, create_reviews(1, user)
        )
        response = auth_user_client.patch(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': collection.id}
            ),
            data=data,
        )

        assert response.status_code == 400, response.data

    def test_08_update_with_reviews_not_belong_to_user(
            self, user, user_2, auth_user_client, create_collection,
            fill_data_for_collection, create_reviews
    ):
        collection = create_collection(user)
        data = fill_data_for_collection(
            'title', 'description', create_reviews(1, user_2)
        )
        response = auth_user_client.patch(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': collection.id}
            ),
            data=data,
        )

        assert response.status_code == 400, response.data

    def test_09_update_with_invalid_cover_size(
            self, user, auth_user_client, fill_data_for_collection,
            open_image_file, create_collection
    ):
        collection = create_collection(user)
        data = {'cover': open_image_file(self.invalid_image_size)}
        response = auth_user_client.patch(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': collection.id}
            ),
            data=data,
            format='multipart'
        )
        assert response.status_code == 400, response.data

    def test_10_update_by_not_creator(
            self, user, auth_user_client_2, create_collection,
            fill_data_for_collection, create_reviews
    ):
        collection = create_collection(user)
        data = fill_data_for_collection(
            'title', 'description', create_reviews(1, user)
        )
        response = auth_user_client_2.patch(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': collection.id}
            ),
            data=data,
        )

        assert response.status_code == 403, response.data

    def test_11_update_not_exist_review(self, auth_user_client):
        data = {
            'title': 'Updated',
            'description': 'Updated',
        }
        response = auth_user_client.patch(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': 999}
            ),
            data=data,
        )
        assert response.status_code == 404, response.data

    def test_12_delete_review_by_creator(
            self, user, auth_user_client, create_collection
    ):
        collection = create_collection(user)
        response = auth_user_client.delete(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': collection.id}
            ),
        )
        assert response.status_code == 204, response.data

    def test_13_delete_review_by_not_creator(
            self, user, auth_user_client_2, create_collection
    ):
        collection = create_collection(user)
        response = auth_user_client_2.delete(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': collection.id}
            ),
        )
        assert response.status_code == 403, response.data

    def test_14_delete_not_exist_review(self, auth_user_client):
        response = auth_user_client.delete(
            reverse(
                'api:collection-detail',
                kwargs={'collection_id': 99999}
            ),)
        assert response.status_code == 404, response.data

