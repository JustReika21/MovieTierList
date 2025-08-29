from django.contrib import admin

from reviews.models import Review, ReviewTag, ReviewType


@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(ReviewType)
class ReviewTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'cover')
    list_display_links = ('id', 'title', 'cover')
