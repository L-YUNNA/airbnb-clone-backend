from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from . import serializers
from reviews.serializers import UserReviewSerializer, HostReviewSerializer
from reviews.models import Review
from rooms.serializers import TinyRoomSerializer, RoomListSerializer
from rooms.models import Room
from .models import User



class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(
            user,
            data = request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class Users(APIView):
    def post(self, request):
        password = request.data.get('password')
        if not password:
            raise ParseError

        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            user.set_password(password)
            user.save()

            serializer = serializers.PrivateUserSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
class PublicUser(APIView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.PublicUserSerializer(user)
        return Response(serializer.data)
    
class ChangePassword(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        
        if not old_password or not new_password:
            raise ParseError
        
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        
        else:
            raise ParseError

class LogIn(APIView):
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            raise ParseError
        
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"ok":"Welcome!"})
        else:
            return Response({"error":"wrong password"})
        
class LogOut(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"ok":"bye!"})


class UserReviews(APIView):   # 로그인 된 유저가 작성한 리뷰 보여줌

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        try:
            page = request.query_params.get('page', 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        user = self.get_object(username)
        reviews = Review.objects.filter(user=user)
        serializer = UserReviewSerializer(
            #user.reviews.all()[start:end],
            reviews[start:end],
            many=True)
        return Response(serializer.data)
    
class HostRooms(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        try:
            page = request.query_params.get('page', 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        owner = self.get_object(username)
        serializer = TinyRoomSerializer(
            owner.rooms.all()[start:end],
            many=True)
        return Response(serializer.data)

class HostReviews(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound

    def get(self, request, username):
        try:
            page = request.query_params.get('page', 1)
            page = int(page)
        except ValueError:
            page = 1

        page_size = settings.PAGE_SIZE
        start = (page - 1) * page_size
        end = start + page_size

        owner = self.get_object(username)
        # 일단 나는 해당 호스트가 가진 모든 숙소에 대한 리뷰들을 한번에 보여주는 걸 만들고 싶은데.. 어렵다.. 
        # print(dir(owner))
        # print(owner.rooms.all())
        # print(Room.objects.filter(owner=owner))

        if owner.is_host == False:
            raise ParseError("This user is not a host")
        # for user_room in Room.objects.filter(owner=owner):
        #     print(user_room.reviews.all())
        serializer = HostReviewSerializer(
            owner.reviews.all()[start:end],
            many=True)
        return Response(serializer.data)
