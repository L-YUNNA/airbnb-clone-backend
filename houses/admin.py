from django.contrib import admin

# Register your models here.

from .models import House

@admin.register(House)  # decorator, 아래 클래스가 house model을 통제할거고, house model을 위한 admin 패널을 만든다고 알려줌
class HouseAdmin(admin.ModelAdmin):   # ModelAdmin(model을 위한 admin 패널) 클래스를 상속받음
    
    # fields = ('name', "address", 
    #           ("price_per_night", "pets_allowed"))
    list_display = (
        "name",
        "price_per_night",
        "address",
        "pets_allowed"
    )
    list_filter = ("price_per_night", "pets_allowed")  # 어떤 컬럼을 기준으로 필터링할 지 적으면 됨
    # search_fields = ("address",)   # 주소 기반 검색창, "address__startswith" 사용하면 무조건 내가 검색하는 단어로 시작하는 것만 찾아줌 (원래는 포함되면 찾아주는데)
    # list_display_links = ("name", "address")
    # list_editable = ("pets_allowed",)
    # exclude = ("price_per_night",)