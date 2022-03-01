from rest_framework import serializers
from rest_auth.models import User
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    
    def create(self, validated_data):
        return User.objects.create(**validated_data)
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance