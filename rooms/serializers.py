from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Amenity, Room
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from reviews.serializers import ReviewSerializer
from medias.serializers import PhotoSerializer


class AmenitySerializer(ModelSerializer):
    class Meta:
        model = Amenity
        fields = (
            "name",
            "description",
        )

class RoomListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        fields = (
            "id",   # ="pk"
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_owner",
            "photos",
        )

    def get_rating(self, room):
        return room.rating()
    
    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user
    
class RoomDetailSerializer(ModelSerializer):
    owner = TinyUserSerializer(read_only=True)
    amenities = AmenitySerializer(read_only=True, many=True)  # AmenitySerializer()클래스가 정의되지 않으면 이 클래스를 RoomDetailSerializer 클래스 위로 올리면 됨
    category = CategorySerializer(read_only=True)
    
    rating = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    photos = PhotoSerializer(read_only=True, many=True)


    class Meta:
        model = Room
        fields = "__all__"

    def get_rating(self, room):
        return room.rating()
    
    def get_is_owner(self, room):
        request = self.context['request']
        return room.owner == request.user





