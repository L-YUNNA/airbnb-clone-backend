# from django.shortcuts import render
# from django.http import JsonResponse
# from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from .models import Category
from .serializers import CategorySerializer

# Create your views here.
class Categories(APIView):

    def get(self, request):   # class안의 모든 메서드는 self를 가져야 함
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data,)
    
    def post(self, request):
        serializer = CategorySerializer(data=request.data)  # request.data는 /categories 페이지에서 form에 json 양식으로 적은 데이터
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data,)
        else:
            return Response(serializer.errors,)

class CategoryDetail(APIView):

    def get_object(self, pk):  # pk는 categories/urls.py의 <int:pk>로부터 옴
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound     # raise가 실행되면 그 뒤 모든 코드는 실행되지 않음
    
    def get(self, request, pk):   # pk 받아야하는 것 유념!
        serializer = CategorySerializer(self.get_object(pk))
        print(serializer)
        return Response(serializer.data,)

    def put(self, request, pk):
        serializer = CategorySerializer(
            self.get_object(pk),
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data,)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        self.get_object(pk).delete()
        return Response(status=HTTP_204_NO_CONTENT)




        
