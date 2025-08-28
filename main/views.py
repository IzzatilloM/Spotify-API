from django.template.context_processors import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import  PageNumberPagination, LimitOffsetPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q


from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .filters import SongFilter
from .serializers import *
from .models import *



class SingerListView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='search',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Ism yoki mamlakat bo'yicha qidiruv",
            ),
            openapi.Parameter(
                name='country',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Mamlakat bo'yicha filtr",
            ),
            openapi.Parameter(
                name='ordering',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Tartiblash: name, birthdate (asc desc)",
                enum=['name', 'birthdate', '-name', '-birthdate'],
            ),
        ],
    )
    def get(self, request):
        singers = Singer.objects.all()

        country = request.GET.get('country')
        if country:
            singers = singers.filter(country__iexact=country)

        search = request.GET.get('search')
        if search:
            singers = singers.filter(
                Q(name__icontains=search) | Q(country__icontains=search)
            )

        ordering = request.GET.get('ordering')
        valid_ordering_fields = ['name', 'birthdate', '-name', '-birthdate']
        if ordering:
            if ordering not in valid_ordering_fields:
                return Response(
                    {
                        'success': False,
                        'error': "Ordering faqat: 'name', 'birthdate', '-name', '-birthdate' bo'yicha"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                singers = singers.order_by(ordering)
            except Exception as e:
                return Response(
                    {
                        'success': False,
                        'error': f"Tartiblashda xatolik: {str(e)}"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = SingerSafeSerializer(singers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Yangi qo'shiqchi qo'shish",
        request_body=SingerPostSerializer,
    )
    def post(self, request):
        serializer = SingerSafeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# class SingerAPIView(APIView):
#     def get(self, request):
#         singer = Singer.objects.all()
#         serializer =SingerPostSerializer(singer, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = SingerPostSerializer(data=request.data)
#         if serializer.is_valid():
#             Singer.objects.create(
#                 name=serializer.data['name'],
#                 birthdate=serializer.data['birthdate'],
#                 country=serializer.data['country']
#             )
#             return Response(serializer.data)
#         return Response(serializer.errors)

class SingerRetrieveUpdateDeleteAPIVIew(APIView):
    def get_object(self, pk):
        return get_object_or_404(Singer, pk=pk)

    def get(self, reuqest, pk):
        singer = self.get_object(pk)
        serializer = SingerPostSerializer(singer)
        return Response(serializer.data)

    def put(self, reuqest, pk):
        singer = get_object_or_404(Singer, pk=pk)
        serializer = SingerPostSerializer(singer, data=reuqest.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        singer = get_object_or_404(Singer, pk=pk)
        singer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# class AlbumAPIView(APIView):
#     def get(self, request):
#         album = Album.objects.all()
#         serializer = AlbumPostSerializer(album, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = AlbumPostSerializer(data=request.data)
#         if serializer.is_valid():
#             Album.objects.create(
#                 name=serializer.data['name'],
#                 image=serializer.data['image'],
#                 singer=Singer.objects.get(pk=request.data['singer'])
#             )
#             return Response(serializer.data)
#         return Response(serializer.errors)
#
# class AlbumRetrieveUpdateDeleteAPIVIew(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Album, pk=pk)
#
#     def get(self, reuqest, pk):
#         album = self.get_object(pk)
#         serializer = AlbumPostSerializer(album)
#         return Response(serializer.data)
#
#     def put(self, reuqest, pk):
#         album = get_object_or_404(Album, pk=pk)
#         serializer = AlbumPostSerializer(album, data=reuqest.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def delete(self, request, pk):
#         album = get_object_or_404(Album, pk=pk)
#         album.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class SongAPIView(APIView):
    def get(self, reuqest):
        song = Song.objects.all()
        serializer = SongSerializer(song, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            Song.objects.create(
                name=serializer.data['name'],
                duration=serializer.data['duration'],
                genre=serializer.data['genre'],
                audi=serializer.data['audio'],
                album=Album.objects.get(pk=request.data['album'])
            )
            return Response(serializer.data)
        return Response(serializer.errors)

class SongRetrieveUpdateDeleteAPIVIew(APIView):
    def get_object(self, pk):
        return get_object_or_404(Song, pk=pk)

    def get(self, reuqest, pk):
        song = self.get_object(pk)
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def put(self, reuqest, pk):
        song = get_object_or_404(Song, pk=pk)
        serializer = SongSerializer(Song, data=reuqest.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def delete(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        song.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SingerViewSet(ModelViewSet):
    queryset = Singer.objects.all()
    serializer_class = SingerPostSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return SingerSafeSerializer
        return self.serializer_class

    def get_serializer_class(self):
        if self.action == 'add_albums':
            return AlbumPostSerializer
        return self.serializer_class

    @action(detail=True, methods=['get'])
    def albums(self, request, pk):
        singer = get_object_or_404(Singer, pk=pk)
        albums = singer.album_set.all()
        serializer = AlbumPostSerializer(albums, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='add-albums')
    def add_albums(self, request, pk):
        singer = get_object_or_404(Singer, pk=pk)
        serializer = AlbumPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            album = serializer.instance
            singer.album_set.add(album)
            response = {
                'success':True,
                'data':serializer.data,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlbumViewSet(ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumPostSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return AlbumSafeSerializer
        return self.serializer_class

    @action(detail=True, methods=['GET'])
    def songs(self, request, pk):
        album = get_object_or_404(Album, pk=pk)
        songs = Song.objects.filter(album=album)
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data)


class SongsViewSet(ModelViewSet):
    serializer_class = SongSerializer
    queryset = Song.objects.all()
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ('name', )
    ordering_fields = ('duration',)
    filterset_fields = ('genre', 'album')
    filterset_class = SongFilter


    @action(detail=True, methods=['GET'])
    def singer(self, request, pk):
        song = get_object_or_404(Song, pk=pk)
        singer = song.album.singer
        serializer = SingerPostSerializer(singer)
        return Response(serializer.data)

