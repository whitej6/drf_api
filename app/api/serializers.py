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


class DeliveryAppField(serializers.RelatedField):
    """

    """
    def get_queryset(self):
        return DeliveryApp.objects.all()

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        try:
            app = DeliveryApp.objects.get(name=data)
        except DeliveryApp.DoesNotExist:
            app = DeliveryApp.objects.create(name=data)
        return app.pk


class RestaurantSerializer(serializers.ModelSerializer):
    """

    """
    user = UserSerializer(required=False)
    delivery_apps = DeliveryAppField(many=True)
    date_modified = serializers.SerializerMethodField()
    
    class Meta:
        model = Restaurant
        fields = '__all__'
        read_only_fields = ['id']
    
    def get_date_modified(self, obj):
        return obj.date_modified.strftime('%m-%d-%Y %H:%M UTC')
