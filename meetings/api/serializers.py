from django.contrib.auth.models import User, Group
from rest_framework import serializers as ser


class UserSerializer(ser.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'groups')


class GroupSerializer(ser.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class AuthenticationSerializer(ser.Serializer):
    username = ser.CharField(required=True)
    password = ser.CharField(required=True)

    def validate(self, data):
        return data
