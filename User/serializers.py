from rest_framework import serializers
from User import models
from Authentication import security_tools as st
from rest_framework.validators import UniqueValidator
import hashlib

MINIMUM_PASSWORD_LENGTH = 4

class UserViewSerializer(serializers.Serializer):
    email = serializers.EmailField()
    user_name = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    joining_date = serializers.DateTimeField()
"""
This is the format for creating new user using the serializer below.
{
    "email": "y@gmail.com",
    "user_name": "Username",
    "password" : "thisisanewpass",
    "first_name": "Fname",
    "last_name": "Lname"
}
password is converted to SHA256 before saving to database
"""
class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=100)
    user_name = serializers.CharField(
        max_length=100,
        validators=[UniqueValidator(queryset=models.User.objects.all(), message='Username already exists!')]
    )
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    
    def validate(self, data):

        if len(data['password']) < MINIMUM_PASSWORD_LENGTH:
            raise serializers.ValidationError()
        if len(data['user_name']) < 4:
            raise serializers.ValidationError()
        if len(data['first_name']) < 1:
            raise serializers.ValidationError()  
        if len(data['last_name']) < 1:
            raise serializers.ValidationError()  
        return data

    def create(self, validated_data):
        new_user = models.User()
        new_user.email = validated_data['email']
        new_user.user_name = validated_data['user_name']
        new_user.password_SHA256 = st.encrypt_string(validated_data['password'])
        new_user.first_name = validated_data['first_name']
        new_user.last_name = validated_data['last_name']
        new_user.save()
        return new_user


