from django.contrib import admin

# Register your models here.
from .models import Room, Amenity

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    list_display = ("name", 
                    "price", 
                    "kind", 
                    "owner",
                    "created_at",
                    "updated_at",)
    list_filter = ("country",
                   "city",
                   "price",
                   "pet_friendly",
                   "kind",
                   "amenities",
                   "created_at",
                   "updated_at",)   # amenity처럼 다른 모델로도 필터링 가능


@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    
    list_display = ("name",
                    "description",
                    "created_at",
                    "updated_at",)
    readonly_fields = ("created_at",
                       "updated_at",)
    
    