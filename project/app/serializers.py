
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password


class user_serializer(serializers.ModelSerializer):

    class Meta:
        model = user_info
        fields = ('name', 'email','password')

    def create(self, validated_data):
        password = make_password(validated_data.pop('password'))
        user_register = user_info.objects.create(password=password,
                                                  **validated_data)
        return user_register  
    
class post_serializer(serializers.ModelSerializer):

    class Meta:
        model = post_info
        fields = ('title', 'discription','content')

class like_serializer(serializers.ModelSerializer):

    class Meta:
        model = Liked_Saved
        fields = "__all__" 