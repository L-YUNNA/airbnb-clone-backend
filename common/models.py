from django.db import models

# Create your models here.
class CommonModel(models.Model):
    """
    Common Model Definition
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:      # 여기서 model의 동작이나 model로 무엇을 해야 하는지 커스터마이즈가 가능
        abstract = True    # 다른 모델에서 재사용하기 위한 모델이기 때문에(db에 테이블을 만들지 않도록) abstract로 줌
