from PIL import Image
from django import forms
from django.core.exceptions import ValidationError
from items.models import Item, ItemTag


IMG_FORMATS = ('jpg', 'jpeg', 'png')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'rating', 'cover', 'tags', 'user']

    def clean_cover(self):
        cover = self.cleaned_data['cover']

        if not cover:
            return

        if type(cover) is str:
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
