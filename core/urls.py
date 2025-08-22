from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from main.views import SingerViewSet, AlbumViewSet, SongsViewSet

router = DefaultRouter()
router.register('singers', SingerViewSet)
router.register('albums', AlbumViewSet)
router.register('songs', SongsViewSet)

from main.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('singer/', SingerAPIView.as_view()),
    path('singer/<int:pk>', SingerRetrieveUpdateDeleteAPIVIew.as_view()),
    # path('albums/', AlbumAPIView.as_view()),
    # path('albums/<int:pk>', AlbumRetrieveUpdateDeleteAPIVIew.as_view()),
    path('song/', SongAPIView.as_view()),
    path('song/<int:pk>', SongRetrieveUpdateDeleteAPIVIew.as_view()),
    path('', include(router.urls)),
]
