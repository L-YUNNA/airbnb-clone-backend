from django.conf import settings
from django.db import transaction
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from rest_framework.exceptions import (NotFound, 
                                       NotAuthenticated, 
                                       ParseError, 
                                       PermissionDenied)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Amenity, Room
from .serializers import (AmenitySerializer, 
                          RoomListSerializer, 
                          RoomDetailSerializer,)

from categories.models import Category
from bookings.models import Booking
from bookings.serializers import PublicBookingSerializer, CreateRoomBookingSerializer
from reviews.serializers import UserReviewSerializer
from medias.serializers import PhotoSerializer


class Amenities(APIView):

    def get(self, request):
        all_amenities = Amenity.objects.all()
        serializer = AmenitySerializer(all_amenities, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AmenitySerializer(data=request.data)
        if serializer.is_valid():
            amenity = serializer.save()
            return Response(AmenitySerializer(amenity).data)
        else:
            return Response(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)

class AmenityDetail(APIView):

    def get_object(self, pk):
        try:
            return Amenity.objects.get(pk=pk)
        except Amenity.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity)
        return Response(serializer.data)

    def put(self, request, pk):
        amenity = self.get_object(pk)
        serializer = AmenitySerializer(amenity,
                                       data=request.data,
                                       partial=True,)
        if serializer.is_valid():
            updated_amenity = serializer.save()
            return Response(AmenitySerializer(updated_amenity).data,)
        else:
            return Response(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        amenity = self.get_object(pk)
        amenity.delete()
        return Response(status=HTTP_204_NO_CONTENT)
    
class Rooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_rooms = Room.objects.all()
        serializer = RoomListSerializer(all_rooms, 
                                        many=True,
                                        context={"request": request},
                                        )
        return Response(serializer.data)
    
    def post(self, request):
        # if request.user.is_authenticated:   # 인증(로그인)된 user인지 먼저 확인
        serializer = RoomDetailSerializer(data=request.data)
        if serializer.is_valid():
            
            category_pk = request.data.get("category")
            if not category_pk:                                 # 여기서는 user가 category_id 자체를 줬는지/안줬는지 확인하고 아래 except문에서는 존재하는 id인지를 확인
                raise ParseError("Category is required.")       # parseError : request가 잘못된 데이터를 가지고 있을 때, 발생 (400 bad request 라는 status code 반환)
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                    raise ParseError("The category kind should be 'rooms'")
            except Category.DoesNotExist:                       # user가 존재하지 않는 category_id 넘긴 경우
                raise ParseError("Category not found.")
            
            try:
                with transaction.atomimc():
                    room = serializer.save(owner=request.user,
                                        category=category,)     # owner 데이터는 request.user로 가져오고, save 메서드에 전달함으로써 request.data에 합쳐침 (save로부터 자동 호출된 create 메서드의 validated_data에 owner 추가됨)
                    amenities = request.data.get("amenities")   # user가 보낸 amenities pk list
                    for amenity_pk in amenities:
                        amenity = Amenity.objects.get(pk=amenity_pk)
                        room.amenities.add(amenity)
                    serializer = RoomDetailSerializer(room)
                    return Response(serializer.data)
            except Exception:   # 어떤 에러든
                raise ParseError("Amenity not found") 
            
        else:
            return Response(serializer.errors,
                            status=HTTP_400_BAD_REQUEST)
        # else:
        #     raise NotAuthenticated
    
class RoomDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        room = self.get_object(pk)
        serializer = RoomDetailSerializer(room,
                                          context={"request":request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:  # 로그인 된 유저 확인
        #     raise NotAuthenticated
        if room.owner != request.user:         # 로그인 된 유저와 방의 호스트 같은지 확인
            raise PermissionDenied
        
        serializer = RoomDetailSerializer(room,
                                          data=request.data,
                                          partial=True,)   # 일부만 변경 가능하도록 
        
        if serializer.is_valid():       # request.data에서 owner, category, amenities는 read_onl=True니까 아래와 같이 처리
            category_pk = request.data.get("category") 
            if category_pk:             # PUT에서는 POST와 다르게 request.data에 category_id가 없을 수 있음 (partial update이니까..)
                try:
                    category = Category.objects.get(pk=category_pk)
                    if category.kind == Category.CategoryKindChoices.EXPERIENCES:
                        raise ParseError("The category kind should be 'rooms'")
                except Category.DoesNotExist:        # category_id를 아예 안 줄 수는 있지만 잘못된 id를 주는 것은 안됨           
                    raise ParseError("Category not found.")
                
            try:
                with transaction.atomic():   # 호스트 로그인해서 put(수정)을 하려고 해도 owner를 수정할 일은 없음 
                    if category_pk:
                        updated_room = serializer.save(category=category)    # 수정할 category가 없는 경우, db의 category 그대로 사용해야 함 
                    else:
                        updated_room = serializer.save()

                    amenities = request.data.get("amenities")   
                    if amenities:
                        updated_room.amenities.clear()
                        for amenity_pk in amenities:
                            amenity = Amenity.objects.get(pk=amenity_pk)
                            updated_room.amenities.add(amenity)

                    serializer = RoomDetailSerializer(updated_room)
                    return Response(serializer.data)
            
            except Exception:   
                raise ParseError("Amenity not found")   
        else:
            return Response(serializer.errors)  
        
    
    def delete(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:  # 로그인 된 유저 확인
        #     raise NotAuthenticated
        if room.owner != request.user:         # 로그인 된 유저와 방의 호스트 같은지 확인
            raise PermissionDenied
        room.delete()
        return Response(status=HTTP_204_NO_CONTENT)

class RoomReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
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

        room = self.get_object(pk)
        serializer = UserReviewSerializer(
            room.reviews.all()[start:end],
            many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        serializer = UserReviewSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(
                user = request.user,
                room = self.get_object(pk),
            )
            serializer = UserReviewSerializer(review)
            return Response(serializer.data)
    
class RoomAmenities(APIView):

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
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
        
        room = self.get_object(pk)
        serializer = AmenitySerializer(room.amenities.all()[start:end],
                                       many=True)
        return Response(serializer.data)

class RoomPhotos(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound

    def post(self, request, pk):
        room = self.get_object(pk)
        # if not request.user.is_authenticated:
        #     raise NotAuthenticated
        if request.user != room.owner:
            raise PermissionDenied
        
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(room=room)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

class RoomBookings(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]  # 모두가 get 메서드 사용 가능(예약 정보 볼 수 있음)하나 post 메서드(예약생성)는 로그인 된 유저만 가능

    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        room = self.get_object(pk)
        now = timezone.localtime(timezone.now()).date()

        bookings = Booking.objects.filter(
            room=room,
            kind=Booking.BookingKindChoices.ROOM,
            check_in__gt=now,     # __gt = greater than
            )
        serializer = PublicBookingSerializer(
            bookings,
            many=True
        )
        return Response(serializer.data)
    
    def post(self, request, pk):
        room = self.get_object(pk)
        serializer = CreateRoomBookingSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(
                room=room,
                user=request.user,
                kind=Booking.BookingKindChoices.ROOM,
            )
            serializer = PublicBookingSerializer(booking)   # 여기서는 생성한 booking을 보여주는 것이므로 PublicBookingSerializer 사용
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    

