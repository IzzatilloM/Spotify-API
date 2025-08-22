from rest_framework import serializers
from .models import *
from datetime import timedelta



class SingerSafeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Singer
        fields = '__all__'

class SingerPostSerializer(serializers.ModelSerializer):
    singer = serializers.SlugRelatedField( slug_field='singer.name', read_only=True)
    class Meta:
        model = Singer
        fields = '__all__'

class AlbumPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

class AlbumSafeSerializer(serializers.ModelSerializer):
    singer = SingerPostSerializer(read_only=True)
    class Meta:
        model = Album
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


    def validate_file(self, value):
        if value and not value.name.lower().endswith('.mp3'):
            raise serializers.ValidationError(
                "Fayl faqat .mp3 formatida bo‘lishi kerak."
            )
        return value

    def validate_duration(self, value):
        if value and value > timedelta(minutes=7):
            raise serializers.ValidationError(
                "Qo‘shiq davomiyligi 7 daqiqadan oshmasligi kerak."
            )
        return value

