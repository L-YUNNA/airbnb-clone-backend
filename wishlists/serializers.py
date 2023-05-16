from rest_framework.serializers import ModelSerializer
from rooms.serializers import RoomListSerializer
from .models import Wishlist

class WishlistSerializer(ModelSerializer):

    rooms = RoomListSerializer(read_only=True,
                               many=True)   # user가 위시리스트 생성 시, 방에 대한 정보를 직접 주지 않아도 되므로 read_only=True
    
    class Meta:
        model = Wishlist
        fields = (
            "pk",
            "name",
            "rooms",
        )

