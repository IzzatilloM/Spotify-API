from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from main.views import SingerViewSet, AlbumViewSet, SongsViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


schema_view = get_schema_view(
   openapi.Info(
      title="Spotify API",
      default_version='v1',
      description="For learning about DRF",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="musayevizzatillo1@gmail.com"),
      license=openapi.License(name="Spotify License"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

router = DefaultRouter()
router.register('singers', SingerViewSet)
router.register('albums', AlbumViewSet)
router.register('songs', SongsViewSet)

from main.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('singer/', SingerListView.as_view()),
    path('singer/<int:pk>', SingerRetrieveUpdateDeleteAPIVIew.as_view()),
    # path('albums/', AlbumAPIView.as_view()),
    # path('albums/<int:pk>', AlbumRetrieveUpdateDeleteAPIVIew.as_view()),
    path('song/', SongAPIView.as_view()),
    path('song/<int:pk>', SongRetrieveUpdateDeleteAPIVIew.as_view()),
    path('', include(router.urls)),
]

urlpatterns += [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
