from django import forms

from item_collections.models import Collection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['title', 'description', 'cover', 'user']
