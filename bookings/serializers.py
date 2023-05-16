from django.utils import timezone
from rest_framework import serializers
from .models import Booking

# post 메서드를 위한 serializer (booking 생성 전용)
class CreateRoomBookingSerializer(serializers.ModelSerializer):

    # booking 모델에서 optional 필드인 데이터를 오버라이딩하여 필수값으로 변경
    check_in = serializers.DateField()
    check_out = serializers.DateField()

    class Meta:
        model = Booking
        fields = (             # post하기 위해서 user에게 받는 데이터만 작성
            "check_in",
            "check_out",
            "guests",
        )

    # serializer의 is_valid를 커스터마이징
    def validate_check_in(self, value):   # value는 check_in으로 받은 데이터 값 (DadeField이므로 date type인 값)
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value    # value가 return 되면 그 value는 검증된 것 
    
    def validate_check_out(self, value):  
        now = timezone.localtime(timezone.now()).date()
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        return value


# get 메서드를 위한 serializer, 모두가 볼 수 있는 public serializer
class PublicBookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = (
            "pk",
            "check_in",
            "check_out",
            "experience_time",
            "guests",
        )

