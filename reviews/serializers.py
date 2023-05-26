from rest_framework import serializers
from users.serializers import TinyUserSerializer
from rooms.serializers import TinyRoomSerializer
from .models import Review

class UserReviewSerializer(serializers.ModelSerializer):
    
    user = TinyUserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = (
            "user",
            "payload",
            "rating",
        )

class HostReviewSerializer(serializers.ModelSerializer):
    
    user = TinyUserSerializer(read_only=True)
    room = TinyRoomSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = (
            "user",
            "room",
            "payload",
            "rating",
        )