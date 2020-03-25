from django.db.models import Q
import django_filters


class RestaurantFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    name = django_filters.CharFilter(lookup_expr='icontains')
    city = django_filters.CharFilter(lookup_expr='icontains')
    state = django_filters.CharFilter()
    zip_code = django_filters.CharFilter(lookup_expr='icontains')
    dine_in = django_filters.CharFilter(method='bool_filter')
    take_out = django_filters.CharFilter(method='bool_filter')
    drive_thru = django_filters.CharFilter(method='bool_filter')
    curbside = django_filters.CharFilter(method='bool_filter')
    delivery = django_filters.CharFilter(method='bool_filter')

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
            Q(name__icontains=value) |
            Q(city__icontains=value) |
            Q(state__icontains=value) |
            Q(zip_code__icontains=value)
        )
        return queryset.filter(qs_filter)

    def bool_filter(self, queryset, name, value):
        if not value.strip():
            return queryset
        if value.strip() == 'on' and name == 'dine_in':
            return queryset.filter(dine_in=True)
        elif value.strip() == 'on' and name == 'take_out':
            return queryset.filter(take_out=True)
        elif value.strip() == 'on' and name == 'drive_thru':
            return queryset.filter(drive_thru=True)
        elif value.strip() == 'on' and name == 'curbside':
            return queryset.filter(curbside=True)
        elif value.strip() == 'on' and name == 'delivery':
            return queryset.filter(delivery=True)
        return queryset
