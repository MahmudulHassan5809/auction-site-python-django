from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from accounts.views import HomeLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('', HomeLoginView.as_view(), name="home_login"),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.FORCE_STATIC_FILE_SERVING and not settings.DEBUG:
    settings.DEBUG = True
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    settings.DEBUG = False


admin.site.site_header = "AuctionBD Admin"
admin.site.site_title = "AuctionBD Admin Portal"
admin.site.index_title = "AuctionBD to Finder Researcher Portal"
