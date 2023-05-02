from django.db import models

# Create your models here.
from common.models import CommonModel

class Experience(CommonModel):
    """
    Experience Model Definition
    """
    country = models.CharField(max_length=50, default="한국")
    city = models.CharField(max_length=80, default="서울")
    
    name = models.CharField(max_length=250)
    description = models.TextField()
    host = models.ForeignKey("users.User", on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()    # DateFeild, DateTimeField, TimeField
    end = models.TimeField()      # 필드 생성 시간(created at) 아니고 여기선 체험 프로그램의 시작 및 종료 시간 말하는거야!
    
    perks = models.ManyToManyField("experiences.Perk")

    category = models.ForeignKey("categories.Category", 
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)


    def __str__(self):
        return self.name


class Perk(CommonModel):
    """
    What is included on an Experience
    """
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, null=True, blank=True)  # null=True는 default=""로 줄 수도 있음
    explanation = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name
