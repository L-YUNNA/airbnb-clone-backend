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
    
    def validate(self, data):   # 여러 fields를 동시에 validate하려면 validate라는 function 사용 (value가 아닌 모든 data를 받음)
        if data['check_out'] <= data['check_in']:
            raise serializers.ValidationError("Check in should be smaller than check out.")
        
        if Booking.objects.filter(
            check_in__lte = data["check_out"],
            check_out__gte = data["check_in"],
        ).exists():
            raise serializers.ValidationError("Those (or some) of those dates are already taken.")
        
        return data
    
class CreateExperienceBookingSerializer(serializers.ModelSerializer):

    experience_time = serializers.DateTimeField()

    class Meta:
        model = Booking
        fields = (                # post하기 위해서 user에게 받는 데이터만 작성
            "experience_time",
            "guests",
        )
    
    def validate_experience_time(self, value):   # value는 experience_time으로 받은 데이터 값
        now = timezone.localtime(timezone.now())
        if now > value:
            raise serializers.ValidationError("Can't book in the past!")
        if Booking.objects.filter(experience_time=value).exists():
            raise serializers.ValidationError("That time is already taken.")
        return value    # value가 return 되면 그 value는 검증된 것 
    

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

