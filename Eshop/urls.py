from django.contrib import admin
from django.urls import path  , include
from django.conf.urls import url
from django.conf.urls.static import static
from . import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , include('store.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = settings.SITE_NAME + " Admin"
admin.site.site_title = settings.SITE_NAME + " Admin"
admin.site.index_title = "Welcome to " + settings.SITE_NAME