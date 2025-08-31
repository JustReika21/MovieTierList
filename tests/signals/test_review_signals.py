import os
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from reviews.models import Review


class TestReviewSignals:
    def test_00_delete_old_cover(self, user):
        old_file = SimpleUploadedFile(
            "old.jpg", b"old content", content_type="image/jpeg"
        )
        new_file = SimpleUploadedFile(
            "new.jpg", b"new content", content_type="image/jpeg"
        )

        review = Review.objects.create(
            title="Signal Test",
            rating=5,
            user=user,
            cover=old_file,
        )
        old_path = review.cover.path

        review.cover = new_file
        review.save()

        new_path = review.cover.path

        assert not os.path.exists(old_path)
        assert os.path.exists(new_path)

        review.delete()
        assert not os.path.exists(new_path)
