from django.db import models

# Create your models here.

class House(models.Model):    # models.Model을 상속받아야 함(장고에는 이미 많은 기능이 만들어져 있음)
    """
    Model definition for Houses
    """
    name = models.CharField(max_length=140)    # name 데이터 타입 정의, CharField : 긴 텍스트는 아니지만 어느 정도 긴, 길이 제한이 있는 텍스트 
    price_per_night = models.PositiveIntegerField(verbose_name="Price",
                                                  help_text="Positive Numbers Only")      # 가격의 양수의 정수
    description = models.TextField()           # 집의 설명, TextField : charfield 보다 긴 텍스트
    address = models.CharField(max_length=140) # 주소 데이터
    pets_allowed = models.BooleanField(default=True, 
                                       verbose_name="Pets Allowed?",
                                       help_text="Does house allow pets?")

    def __str__(self):
        return self.name
    

