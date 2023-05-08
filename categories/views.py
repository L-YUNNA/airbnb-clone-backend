# from django.shortcuts import render
# from django.http import JsonResponse
# from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from .models import Category
from .serializers import CategorySerializer

# Create your views here.
@api_view(["GET", "POST"])
def categories(request):         # urls.py에서 호출된 함수에는 request 객체가 모두 주어짐
    if request.method == "GET":
        all_categories = Category.objects.all()
        serializer = CategorySerializer(all_categories, many=True)
        return Response(serializer.data,)
    
    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)  # request.data는 /categories 페이지에서 form에 json 양식으로 적은 데이터
        if serializer.is_valid():
            new_category = serializer.save()
            return Response(CategorySerializer(new_category).data,)
        else:
            return Response(serializer.errors,)


@api_view(["GET", "PUT", "DELETE"])
def category(request, pk):  # pk는 categories/urls.py의 <int:pk>로부터 옴
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        raise NotFound     # raise가 실행되면 그 뒤 모든 코드는 실행되지 않음

    if request.method == "GET":
        serializer = CategorySerializer(category)
        return Response(serializer.data,)
    
    elif request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            updated_category = serializer.save()
            return Response(CategorySerializer(updated_category).data,)
        else:
            return Response(serializer.errors)
    
    elif request.method == "DELETE":
        category.delete()
        return Response(status=HTTP_204_NO_CONTENT)

        
