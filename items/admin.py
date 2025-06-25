from django.contrib import admin

from items.forms import ItemForm
from items.models import Item, ItemTag


@admin.register(ItemTag)
class ItemTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_display_links = ('name', 'user')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    list_display = ('id', 'title', 'cover')
    list_display_links = ('id', 'title', 'cover')
