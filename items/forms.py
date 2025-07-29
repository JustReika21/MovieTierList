from PIL import Image
from django import forms
from django.core.exceptions import ValidationError
from items.models import Item


IMG_FORMATS = ('jpg', 'jpeg', 'png')


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'rating', 'cover', 'tags', 'user']
