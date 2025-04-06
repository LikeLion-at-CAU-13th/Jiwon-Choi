from django.shortcuts import render
from django.http import JsonResponse # 데이터를 JSON에 담기 위해서 사용
from django.shortcuts import get_object_or_404 # 추가

#4주? 추가4개
from django.views.decorators.http import require_http_methods # 4주? 추가
from .models import * # 4주? 추가

# 5주 추가
import json

# Create your views here.

def django_review(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "250323 2nd session review"
        })
    
def index(request):
    return render(request, 'index.html')


#4주에 추가한 부분들

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

# 5주 추가
# 1. Post 부분... create.
# import json

# 함수 데코레이터, 특정 http method만 허용
# 원래는 "POST"만 있었고, READ 기능을 위해 "GET"을 추가했음
@require_http_methods(["POST", "GET"])
def post_list(request):
    
    if request.method == "POST":
    
        # byte -> 문자열 -> python 딕셔너리
        body = json.loads(request.body.decode('utf-8'))
    
		    # 프론트에게서 user id를 넘겨받는다고 가정.
		    # 외래키 필드의 경우, 객체 자체를 전달해줘야하기 때문에
        # id를 기반으로 user 객체를 조회해서 가져옵니다 !
        user_id = body.get('user')
        user = get_object_or_404(User, pk=user_id)

	    # 새로운 데이터를 DB에 생성
        new_post = Post.objects.create(
            title = body['title'],
            content = body['content'],
            status = body['status'],
            user = user
        )
    
	    # Json 형태 반환 데이터 생성
        new_post_json = {
            "id": new_post.id,
            "title" : new_post.title,
            "content": new_post.content,
            "status": new_post.status,
            "user": new_post.user.id
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 생성 성공',
            'data': new_post_json
        })
    
    # 2. GET 부분 추가 코드
    # 게시글 전체 조회
    if request.method == "GET":
        post_all = Post.objects.all()
    
		# 각 데이터를 Json 형식으로 변환하여 리스트에 저장
        post_json_all = []
        
        for post in post_all:
            post_json = {
                "id": post.id,
                "title" : post.title,
                "content": post.content,
                "status": post.status,
                "user": post.user.id
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '게시글 목록 조회 성공',
            'data': post_json_all
        })
    


# 3. 단일 post 조회 - post id가 필요함
@require_http_methods(["GET"])
    # 매개변수로 id 받는다
def post_detail(request, post_id):

    # post_id에 해당하는 단일 게시글 조회
    if request.method == "GET":
        # ORM이 찾아서 리턴함
        post = get_object_or_404(Post, pk=post_id)

        post_json = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "status": post.status,
            "user": post.user.id,
        }
        
        return JsonResponse({
            'status': 200,
            'message': '게시글 단일 조회 성공',
            'data': post_json
        })
    