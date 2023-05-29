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
    host = models.ForeignKey("users.User", 
                             on_delete=models.CASCADE,
                             related_name="experiences")
    price = models.PositiveIntegerField()
    address = models.CharField(max_length=250)
    start = models.TimeField()    # DateFeild, DateTimeField, TimeField
    end = models.TimeField()      # 필드 생성 시간(created at) 아니고 여기선 체험 프로그램의 시작 및 종료 시간 말하는거야!
    
    perks = models.ManyToManyField("experiences.Perk",
                                   related_name="experiences")

    category = models.ForeignKey("categories.Category", 
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL,
                                 related_name="experiences")

    def __str__(self):
        return self.name
    
    def rating(experience):   # room=self
        count = experience.reviews.count()
        if count==0:
            return 0
        else:
            total_rating = 0
            # print(room.reviews.all().values("rating"))   # <QuerySet [{‘rating’: 5}, {‘rating’: 3}, … >
            for review in experience.reviews.all().values("rating"):
                total_rating += review["rating"]
            return round(total_rating/count, 1)


class Perk(CommonModel):
    """
    What is included on an Experience
    """
    name = models.CharField(max_length=100)
    details = models.CharField(max_length=250, null=True, blank=True)  # null=True는 default=""로 줄 수도 있음
    explanation = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name
