import django_filters
from .models import CodeFile

class CodeFileFilter(django_filters.FilterSet):
    # NumberFilters for size ranges
    min_size = django_filters.NumberFilter(field_name="size", lookup_expr='gte')
    max_size = django_filters.NumberFilter(field_name="size", lookup_expr='lte')
    
    # CharFilters for string matching
    name = django_filters.CharFilter(lookup_expr='icontains')
    language = django_filters.CharFilter(lookup_expr='iexact')
    file_type = django_filters.CharFilter(lookup_expr='iexact')
    
    # Custom boolean filter for is_critical
    is_critical = django_filters.BooleanFilter(method='filter_is_critical')

    class Meta:
        model = CodeFile
        fields = ['repository', 'name', 'language', 'file_type', 'min_size', 'max_size', 'is_critical']

    def filter_is_critical(self, queryset, name, value):
        if value:
            return queryset.critical()
        return queryset
