from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Perk, Experience
from medias.serializers import PhotoSerializer
from users.serializers import TinyUserSerializer
from categories.serializers import CategorySerializer
from wishlists.models import Wishlist

class PerkSerializer(ModelSerializer):
    class Meta:
        model = Perk
        fields = "__all__"

class ExperienceListSerializer(ModelSerializer):

    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Experience
        fields = (
            "id",   # ="pk"
            "name",
            "country",
            "city",
            "price",
            "rating",
            "is_host",
            "photos",
        )

    def get_rating(self, experience):
        return experience.rating()
    
    def get_is_host(self, experience):
        request = self.context['request']
        return experience.host == request.user

class ExperienceDetailSerializer(ModelSerializer):
    host = TinyUserSerializer(read_only=True)
    perks = PerkSerializer(read_only=True, many=True)   # PerkSerializer()클래스가 정의되지 않으면 이 클래스를 ExperienceDetailSerializer 클래스 위로 올리면 됨
    category = CategorySerializer(read_only=True)
    
    rating = serializers.SerializerMethodField()
    is_host = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Experience
        fields = "__all__"

    def get_rating(self, experience):  
        return experience.rating()
    
    def get_is_host(self, experience):
        request = self.context['request']
        return experience.host == request.user
    
    def get_is_liked(self, experience):  
        request = self.context['request']
        return Wishlist.objects.filter(user=request.user, 
                                       experiences__pk=experience.pk).exists()
    



