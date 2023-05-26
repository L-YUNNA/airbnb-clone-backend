from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User

class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username"
        )

class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", 
                   "is_superuser",
                   "id",
                   "is_staff",
                   "is_active",
                   "first_name",
                   "last_name",
                   "groups",
                   "user_permissions",)   
        
class PublicUserSerializer(ModelSerializer):

    total_rooms = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
            "gender",
            "is_host",
            "language",
            "total_rooms",
            "total_reviews",
        )

    def get_total_rooms(self, user):
        return user.total_rooms()
    
    def get_total_reviews(self, user):
        return user.total_reviews()

    
