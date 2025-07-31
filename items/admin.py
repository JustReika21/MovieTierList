from django.contrib import admin

from items.models import Item, ItemTag


@admin.register(ItemTag)
class ItemTagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cover')
    list_display_links = ('id', 'title', 'cover')
