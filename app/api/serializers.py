from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import DeliveryApp, Restaurant


class DeliveryAppSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = DeliveryApp
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class UserSerializer(serializers.ModelSerializer):
    """

    """
    class Meta:
        model = get_user_model()
        fields = ['name', 'email']

class RestaurantSerializer(serializers.ModelSerializer):
    """

    """
    user = UserSerializer()
    delivery_apps = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ['id']
        