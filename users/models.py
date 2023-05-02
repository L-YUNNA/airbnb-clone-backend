from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")        # ("db에 들어갈 value", "admin 패널에서 보게될 lable") 이렇게 입력 
        FEMALE = ("female", "Female")
    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")    # db에 들어갈 값은 "kr"은 밑에서 language 필드의 max_length=2이기 때문에 두글자 이상이면 안됨
        EN = ("en", "English")
    class CurrencyChoices(models.TextChoices):
        WON = "won", "korean Won"   # python에서 튜플 이렇게 괄호 없이 사용 가능
        USD = "usd", "Dollar"

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    avatar = models.ImageField(blank=True)
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    currency = models.CharField(max_length=5, choices=CurrencyChoices.choices)