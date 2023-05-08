from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = (
            "created_at",
        )
        #fields = "__all__"   # 모든 필드를 보이게 하고 싶은 경우