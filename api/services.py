from PIL import Image
from rest_framework.exceptions import ValidationError

IMG_FORMATS = ('jpg', 'jpeg', 'png')


def cover_validator(cover):
    """
    Validate an uploaded image file.

    Checks:
        - File must not exceed 4MB.
        - Must be a valid image (jpg, jpeg, png).
        - File must be an actual image file.

    Raises:
        ValidationError: If any condition fails.

    Returns:
        File: The validated image file.
    """
    if not cover:
        return

    if cover.size > 4 * 1024 * 1024:
        raise ValidationError('Cover must be less than 4 mb')

    try:
        img = Image.open(cover)
        img.verify()
    except Exception:
        raise ValidationError('Uploaded file is not a valid image')

    img_format = img.format.lower()
    if img_format not in IMG_FORMATS:
        raise ValidationError(
            'Cover must be one of this formats: ' + ', '.join(IMG_FORMATS)
        )

    return cover
