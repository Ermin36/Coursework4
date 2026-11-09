from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('send_track.urls', namespace='send_track')),
    path('', include('msg_client.urls', namespace='msg_client')),
]
