from django.conf import settings
from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import (NotFound, 
                                       ParseError, 
                                       PermissionDenied)
from .models import Perk, Experience
from . import serializers
from categories.models import Category
from bookings.models import Booking
from reviews.serializers import UserReviewSerializer
from medias.serializers import PhotoSerializer
from bookings.serializers import PublicBookingSerializer, CreateExperienceBookingSerializer

class Experiences(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(all_experiences,
                                                          many=True,
                                                          context={"request": request},)
        return Response(serializer.data)
    
    def post(self, request):
        
        serializer = serializers.ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            
            category_pk = request.data.get("category")
            if not category_pk:                                
                raise ParseError("Category is required.")       
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be 'experiences'")
            except Category.DoesNotExist:                       
                raise ParseError("Category not found.")
            
            try:
                with transaction.atomimc():
                    experience = serializer.save(host=request.user,
                                                 category=category,)    
                    perks = request.data.get("perks")  
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        experience.perks.add(perk)
                    serializer = serializers.ExperienceDetailSerializer(experience)
                    return Response(serializer.data)
            except Exception: 
                raise ParseError("Perk not found") 
            
        else:
            return Response(serializer.errors)

class ExperienceDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(experience,
                                                            context={"request":request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:         
            raise PermissionDenied
        
        serializer = serializers.ExperienceDetailSerializer(experience,
                                                            data=request.data,
                                                            partial=True,)  
        
        if serializer.is_valid():       
            category_pk = request.data.get("category") 
            if category_pk:             # PUT에서는 POST와 다르게 request.data에 category_id가 없을 수 있음 (partial update이니까..)
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.ROOMS:
                        raise ParseError("The category kind should be 'experiences'")
                except Category.DoesNotExist:        # category_id를 아예 안 줄 수는 있지만 잘못된 id를 주는 것은 안됨           
                    raise ParseError("Category not found.")
                
            try:
                with transaction.atomic():   # 호스트 로그인해서 put(수정)을 하려고 해도 owner를 수정할 일은 없음 
                    if category_pk:
                        updated_experience = serializer.save(category=category)    # 수정할 category가 없는 경우, db의 category 그대로 사용해야 함 
                    else:
                        updated_experience = serializer.save()

                    perks = request.data.get("perks")   
                    if perks:
                        updated_experience.perks.clear()
                        for perk_pk in perks:
                            perk = Perk.objects.get(pk=perk_pk)
                            updated_experience.perks.add(perk)

                    serializer = serializers.ExperienceDetailSerializer(updated_experience)
                    return Response(serializer.data)
            
            except Exception:   
                raise ParseError("Amenity not found")   
        else:
            return Response(serializer.errors)  
        
    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:     
            raise PermissionDenied
        experience.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class ExperienceReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get('page', 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        experience = self.get_object(pk)
        serializer = UserReviewSerializer(
            experience.reviews.all()[start:end],
            many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user = request.user,
                experience = self.get_object(pk),
            )
            serializer = UserReviewSerializer(review)
            return Response(serializer.data)

class ExperiencePerks(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        try:
            page = request.query_params.get('page', 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page-1)*page_size
        end = start + page_size
        
        experience = self.get_object(pk)
        serializer = serializers.PerkSerializer(
            experience.perks.all()[start:end],
            many=True
            )
        return Response(serializer.data)

class ExperiencePhotos(APIView):
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        pass

    def post(self, request, pk):
        experience = self.get_object(pk)
        if request.user != experience.host:
            raise PermissionDenied
        
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class ExperienceBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        experience = self.get_object(pk)
        now = timezone.localtime(timezone.now())  # 날짜, 시간 모두 가져옴

        bookings = Booking.objects.filter(
            experience=experience,
            kind=Booking.BookingKindChoices.EXPERIENCE,
            experience_time__gt=now,
        )
        serializer = PublicBookingSerializer(
                    bookings,
                    many=True
                )
        return Response(serializer.data)
    
    def post(self, request, pk):
        experience = self.get_object(pk)
        serializer = CreateExperienceBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                experience=experience,
                user=request.user,
                kind=Booking.BookingKindChoices.EXPERIENCE,
            )
            serializer = PublicBookingSerializer(booking)   # 여기서는 생성한 booking을 보여주는 것이므로 PublicBookingSerializer 사용
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Perks(APIView):

    def get(self, request):
        all_perks = Perk.objects.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            perk = serializer.save()
            return Response(serializers.PerkSerializer(perk).data,)
        else:
            return Response(serializer.errors)

class PerkDetail(APIView):

    def get_object(self, pk):
        try:
            return Perk.objects.get(pk=pk)
        except Perk.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)

    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk,
                                    data=request.data,
                                    partial=True,)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data,)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=HTTP_204_NO_CONTENT)