import django_filters
from .models import *

class SongFilter(django_filters.FilterSet):
    min_duration = django_filters.NumberFilter(field_name="duration", lookup_expr='gte')
    max_duration = django_filters.NumberFilter(field_name="duration", lookup_expr='lte')

    class Meta:
        model = Song
        fields = ['name', 'min_duration', 'max_duration']