from rest_framework import viewsets, mixins
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import DeliveryApp, Restaurant
from . import serializers


class DeliveryAppViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """

    """
    permission_classes = (IsAuthenticated,)
    queryset = DeliveryApp.objects.all()
    serializer_class = serializers.DeliveryAppSerializer
    authentication_classes = (BasicAuthentication,)


class RestaurantViewSet(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin):
    """

    """
    permission_classes = (IsAuthenticated,)
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer
    authentication_classes = (BasicAuthentication,)
