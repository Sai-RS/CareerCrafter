from dataclasses import fields
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import UserRole


""" class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password')

        extra_kwargs = {
            'first_name': { 'required': True, 'allow_blank': False },
            'last_name': { 'required': True, 'allow_blank': False },
            'email': { 'required': True, 'allow_blank': False },
            'password': { 'required': True, 'allow_blank': False, 'min_length': 6 },
        }"""

class SignUpSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True)  # Add role field

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'role')

        extra_kwargs = {
            'first_name': { 'required': True, 'allow_blank': False },
            'last_name': { 'required': True, 'allow_blank': False },
            'email': { 'required': True, 'allow_blank': False },
            'password': { 'required': True, 'allow_blank': False, 'min_length': 6 },
        }

    def create(self, validated_data):
        role = validated_data.pop('role')  # Extract role from validated data
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['email'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
        )
        UserRole.objects.create(user=user, role=role)  # Create user role
        return user

class UserSerializer(serializers.ModelSerializer):
    resume = serializers.CharField(source='userprofile.resume')
    role = serializers.CharField(source='userrole.role')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'resume','role')