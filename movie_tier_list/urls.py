from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from debug_toolbar.toolbar import debug_toolbar_urls

from movie_tier_list import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('api/', include('api.urls')),
    path('', include('core.urls')),
    path('collections/', include('item_collections.urls')),
    path('items/', include('items.urls')),
    path('profile/', include('user_profile.urls')),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
