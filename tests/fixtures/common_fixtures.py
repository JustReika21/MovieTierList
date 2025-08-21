import pytest
import io
import os

from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile

from movie_tier_list import settings


@pytest.fixture
def open_image_file():
    def _create(name='valid_image.jpg'):
        img = Image.open(os.path.join(settings.BASE_DIR, 'tests/test_images/', name))
        img_format = name.split('.')[-1].lower()
        if img_format == 'jpg':
            img_format = 'jpeg'
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=img_format)
        img_bytes.seek(0)
        return SimpleUploadedFile(name, img_bytes.read(), content_type=f'image/{img_format}')
    return _create
