from django.contrib import admin

from reviews.models import Review, ReviewTag


@admin.register(ReviewTag)
class ItemTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Review)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cover')
    list_display_links = ('id', 'title', 'cover')
