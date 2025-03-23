from django.shortcuts import render
from django.http import JsonResponse # 데이터를 JSON에 담기 위해서 사용
from django.shortcuts import get_object_or_404 # 추가

# Create your views here.

def django_review(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "250323 2nd session review"
        })