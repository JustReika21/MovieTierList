import pytest
from django.urls import reverse


class TestReviewsAPI:
    default_review_cover_path = '/media/reviews/default.jpg'
    invalid_image_size = 'invalid_image_size.png'
    valid_image = 'valid_image.jpg'
    valid_image2 = 'valid_image2.png'
    valid_image3 = 'valid_image3.jpeg'

    @pytest.mark.django_db
    def test_00_create_review_not_auth(
        self, client, create_tags, fill_data_for_review
    ):
        data = fill_data_for_review('Title', 'Description', 5, create_tags())
        response = client.post(reverse('api:review-list'), data=data)
        assert response.status_code == 403, response.data

    @pytest.mark.django_db
    @pytest.mark.parametrize('title, description, rating', [
        ('A' * 128, 'Description', 5),
        ('', 'Description', 5),
        ('Title', 'A' * 1025, 5),
        ('Title', 'Description', 0),
        ('Title', 'Description', 11),
    ])
    def test_01_create_review_with_invalid_data(
        self, auth_user_client, create_tags, fill_data_for_review,
        title, description, rating
    ):
        tags = create_tags(5)
        data = fill_data_for_review(title, description, rating, tags)
        response = auth_user_client.post(reverse('api:review-list'), data=data)
        assert response.status_code == 400, response.data

    @pytest.mark.django_db
    def test_02_create_review_with_invalid_cover_size(
        self, auth_user_client, create_tags, fill_data_for_review,
        open_image_file
    ):
        big_img = open_image_file(self.invalid_image_size)
        data = fill_data_for_review('Big Cover', 'Desc', 5, create_tags())
        data['cover'] = big_img
        response = auth_user_client.post(
            reverse('api:review-list'),
            data=data,
            format='multipart'
        )
        assert response.status_code == 400, response.data

    @pytest.mark.django_db
    @pytest.mark.parametrize('title, description, rating', [
        ('Title', 'Description', 10),
        ('Название', 'Описание', 1),
        ('А' * 127, 'A' * 1024, 5),
        ('А', '', 5),
    ])
    def test_03_create_review_with_valid_data(
        self, auth_user_client, create_tags, create_type, fill_data_for_review,
        title, description, rating
    ):
        tags = create_tags(2)
        review_type = create_type()
        data = fill_data_for_review(
            title, description, rating, tags, review_type
        )
        response = auth_user_client.post(reverse('api:review-list'), data=data)
        assert response.status_code == 201, response.data
        body = response.json()
        assert body['title'] == title
        assert body['description'] == description
        assert body['rating'] == rating
        assert body['tags'] == [tag.id for tag in tags]
        assert body['type'] == review_type.id
        assert body['cover'] == self.default_review_cover_path

    @pytest.mark.django_db
    @pytest.mark.parametrize('cover_name', [
        valid_image,
        valid_image2,
        valid_image3,
    ])
    def test_04_create_valid_review_with_cover(
        self, auth_user_client, create_tags, fill_data_for_review,
        open_image_file, cover_name
    ):
        img = open_image_file(cover_name)
        data = fill_data_for_review('Big Cover', 'Desc', 5, create_tags())
        data['cover'] = img
        response = auth_user_client.post(
            reverse('api:review-list'),
            data=data,
            format='multipart'
        )
        assert response.status_code == 201, response.data
        assert response.json()['cover'] != self.default_review_cover_path, (
            response.data
        )

        response = auth_user_client.delete(
            reverse(
                'api:review-detail',
                kwargs={'review_id': response.json()["id"]}
            ),
        )
        assert response.status_code == 204, response.data

    @pytest.mark.django_db
    @pytest.mark.parametrize('title, description, rating', [
        ('Updated', 'Review', 10,),
        ('Title', 'Description', 10),
        ('Название', 'Описание', 1),
        ('А' * 127, 'A' * 1024, 5),
        ('А', '', 5),
    ])
    def test_05_update_review_with_valid_data_by_creator(
        self, user, auth_user_client, create_tags, create_review, create_type,
        fill_data_for_review, title, description, rating
    ):
        review = create_review(user)
        tags = create_tags(5)
        review_type = create_type()
        data = fill_data_for_review(
            title, description, rating, tags, review_type
        )
        response = auth_user_client.patch(
            reverse(
                'api:review-detail',
                kwargs={'review_id': review.id}
            ),
            data=data
        )

        body = response.json()
        assert response.status_code == 200, body
        assert body['title'] == title
        assert body['description'] == description
        assert body['rating'] == rating
        assert body['tags'] == [tag.id for tag in tags]
        assert body['type'] == review_type.id
        assert body['cover'] == self.default_review_cover_path

    @pytest.mark.django_db
    def test_06_update_cover_valid(
        self, user, auth_user_client, create_tags, create_review,
        fill_data_for_review, open_image_file
    ):
        review = create_review(user)
        data = {'cover': open_image_file(self.valid_image)}
        response = auth_user_client.patch(
            reverse(
                'api:review-detail',
                kwargs={'review_id': review.id}
            ),
            data=data,
            format='multipart'
        )
        assert response.status_code == 200, response.data
        assert response.json()['cover'] != self.default_review_cover_path, (
            response.data
        )

        response = auth_user_client.delete(f'/api/v1/reviews/{review.id}/')
        assert response.status_code == 204, response.data

    @pytest.mark.django_db
    @pytest.mark.parametrize('title, description, rating', [
        ('A' * 128, 'Description', 5),
        ('', 'Description', 5),
        ('Title', 'A' * 1025, 5),
        ('Title', 'Description', 0),
        ('Title', 'Description', 11),
    ])
    def test_07_update_with_invalid_data(
        self, user, auth_user_client, create_tags, create_review,
        fill_data_for_review, title, description, rating
    ):
        review = create_review(user)
        data = fill_data_for_review(
            title, description, rating, create_tags()
        )
        response = auth_user_client.patch(
            reverse(
                'api:review-detail',
                kwargs={'review_id': review.id}
            ),
            data=data
        )

        assert response.status_code == 400, response.data

    @pytest.mark.django_db
    def test_08_update_with_invalid_cover_size(
        self, user, auth_user_client, fill_data_for_review,
        open_image_file, create_review
    ):
        review = create_review(user)
        data = {'cover': open_image_file(self.invalid_image_size)}
        response = auth_user_client.patch(
            reverse(
                'api:review-detail',
                kwargs={'review_id': review.id}
            ),
            data=data,
            format='multipart'
        )
        assert response.status_code == 400, response.data

    @pytest.mark.django_db
    def test_09_update_by_not_creator(
        self, user, auth_user_client_2, create_tags,
        create_review, fill_data_for_review
    ):
        review = create_review(user)
        tags = [tag.id for tag in create_tags(5)]
        data = {
            'title': 'Updated',
            'description': 'Updated',
            'rating': 9,
            'tags': tags
        }
        response = auth_user_client_2.patch(
            reverse(
                'api:review-detail',
                kwargs={'review_id': review.id}
            ),
            data=data
        )
        assert response.status_code == 403, response.data

    @pytest.mark.django_db
    def test_10_update_not_exist_review(self, auth_user_client):
        data = {
            'title': 'Updated',
            'description': 'Updated',
            'rating': 9
        }
        response = auth_user_client.patch(
            reverse(
                'api:review-detail',
                kwargs={'review_id': 999}
            ),
            data=data)
        assert response.status_code == 404, response.data

    @pytest.mark.django_db
    def test_11_delete_review_by_creator(
        self, user, auth_user_client, create_review
    ):
        review = create_review(user)
        response = auth_user_client.delete(
            reverse(
                'api:review-detail',
                kwargs={'review_id': review.id}
            ),
        )
        assert response.status_code == 204, response.data

    @pytest.mark.django_db
    def test_12_delete_review_by_not_creator(
        self, user, auth_user_client_2, create_review
    ):
        review = create_review(user)
        response = auth_user_client_2.delete(
            reverse(
                'api:review-detail',
                kwargs={'review_id': review.id}
            ),
        )
        assert response.status_code == 403, response.data

    @pytest.mark.django_db
    def test_13_delete_not_exist_review(self, auth_user_client):
        response = auth_user_client.delete(
            reverse(
                'api:review-detail',
                kwargs={'review_id': 99999}
            ),
        )
        assert response.status_code == 404, response.data

    @pytest.mark.django_db
    def test_14_get_review_tags_by_query(self, auth_user_client, create_tag):
        tag1 = create_tag('Created')
        tag2 = create_tag('USO')
        tag3 = create_tag('Created2')
        right_tag_ids = {tag1.id, tag3.id}

        response = auth_user_client.get(
            reverse('api:tag-get'), {'query': 'c'},
        )
        assert response.status_code == 200, response.data
        tag_ids = {tag['id'] for tag in response.json()}
        assert tag_ids == right_tag_ids, f"Expected {right_tag_ids}, got {tag_ids}"

    @pytest.mark.django_db
    def test_15_get_reviews_by_query(
            self, user, auth_user_client, create_review
    ):
        review1 = create_review(user, 'Created')
        review2 = create_review(user, 'USO')
        review3 = create_review(user, 'Created2')
        right_review_ids = {review1.id, review3.id}

        response = auth_user_client.get(
            reverse('api:review-search'), {'user_id': user.id,'query': 'c'},
        )
        assert response.status_code == 200, response.data
        review_ids = {review['id'] for review in response.json()}
        assert review_ids == right_review_ids, f"Expected {right_review_ids}, got {review_ids}"

    @pytest.mark.django_db
    def test_16_get_limit_reviews_by_query(
            self, user, auth_user_client, create_review
    ):
        for i in range(10):
            create_review(user, f'Created{i}')

        response = auth_user_client.get(
            reverse('api:review-search'), {'user_id': user.id, 'query': 'c'},
        )

        assert response.status_code == 200, response.data
        assert len(response.json()) == 5

    @pytest.mark.django_db
    def test_17_get_reviews_with_wrong_user_id(
            self, user, user_2, auth_user_client, create_review
    ):
        create_review(user_2, 'Created')

        response = auth_user_client.get(
            reverse('api:review-search'), {'user_id': user.id, 'query': 'c'},
        )

        assert response.status_code == 200, response.data
        assert len(response.json()) == 0

    @pytest.mark.django_db
    def test_18_get_reviews_by_another_user(
            self, user, auth_user_client_2, create_review
    ):
        create_review(user, 'Created')

        response = auth_user_client_2.get(
            reverse('api:review-search'), {'user_id': user.id, 'query': 'c'},
        )

        assert response.status_code == 200, response.data
        assert len(response.json()) == 1
