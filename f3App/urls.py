
from django.urls import path
from .views import index,download#,upload
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',index),
    path('download',download,name="download"),
    # url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
    
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)