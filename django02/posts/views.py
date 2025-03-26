from django.shortcuts import render
from django.http import JsonResponse # 데이터를 JSON에 담기 위해서 사용
from django.shortcuts import get_object_or_404 # 추가

#추가4개
from django.views.decorators.http import require_http_methods # 추가
from .models import * # 추가

# Create your views here.

def django_review(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "250323 2nd session review"
        })
    
def index(request):
    return render(request, 'index.html')


#추가한 부분들

# Create your views here.
# GET을 허용해서... @
@require_http_methods(["GET"])
# post의 내용들을 가져오게 json을 구성
def get_post_detail(reqeust, id):
    post = get_object_or_404(Post, pk=id)
    post_detail_json = {
        "id" : post.id,
        "title" : post.title,
        "content" : post.content,
        "status" : post.status,
        "user" : post.user.username,
    }
    # status와 아까 설정한 post_detail_json을 리턴하게 함
    return JsonResponse({
        "status" : 200,
        "data": post_detail_json})

#http://127.0.0.1:8000/1 postman에서 확인하기
