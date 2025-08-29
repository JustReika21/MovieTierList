import os
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from review_collections.models import Collection


class TestCollectionSignals:
    @pytest.mark.django_db
    def test_00_delete_old_cover(self, user):
        old_file = SimpleUploadedFile(
            "old.jpg", b"old content", content_type="image/jpeg"
        )
        new_file = SimpleUploadedFile(
            "new.jpg", b"new content", content_type="image/jpeg"
        )

        collection = Collection.objects.create(
            title="Signal Test",
            user=user,
            cover=old_file,
        )
        old_path = collection.cover.path

        collection.cover = new_file
        collection.save()

        new_path = collection.cover.path

        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)

        collection.delete()
        assert not os.path.exists(new_path)
