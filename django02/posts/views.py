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
# READ - "GET", UPDATE - "PATCH", DELETE - "DELETE" 
@require_http_methods(["GET", "PATCH", "DELETE"])
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
    

    # UPDATE - PATCH 부분
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        
        update_post = get_object_or_404(Post, pk=post_id)

        if 'title' in body:
            update_post.title = body['title']
        if 'content' in body:
            update_post.content = body['content']
        if 'status' in body:
            update_post.status = body['status']
    
        
        update_post.save()

        update_post_json = {
            "id": update_post.id,
            "title" : update_post.title,
            "content": update_post.content,
            "status": update_post.status,
            "user": update_post.user.id,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
    
    # DELETE 부분
    if request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=post_id)
        delete_post.delete()

        return JsonResponse({
                'status': 200,
                'message': '게시글 삭제 성공',
                'data': None
        })
    

    # 4. 과제 부분 - 특정 게시글에 포함된 모든 comment를 조회하는 api
@require_http_methods(["GET"])
def post_comments(request, post_id):

    # post_id에 해당하는 단일 게시글 조회
    if request.method == "GET":
        # 특정 post_id에 해당하는 게시글이 존재하는지 여부를 확인하기 위해
        post = get_object_or_404(Post, pk=post_id)

        # 해당 게시글에 연결된 모든 comment 조회
        # comments = Comment.objects.filter(post_id = post)
        # post_id로 필드 지정 시 ORM이 자동으로 Comment.post.id 필드를 기준으로 입력값 비교해줌
        # 위와 같이 적어도 ORM이 자동으로 변환해주지만 가독성 측면에서 아래와 같이 코드 수정함
        comments = Comment.objects.filter(post_id = post_id)

        comments_json = [
            {
                "comment_id" : comment.comment_id,
                "comment_name" : comment.comment_name,
                "comment_content": comment.comment_content,
            }
            for comment in comments
        ]

        return JsonResponse({
            'status': 200,
            'message': f'게시글 ID {post_id}에 포함된 댓글 조회 성공',
            'data': comments_json
        })
    

# 5. 과제 부분 - 카테고리별로
@require_http_methods(["GET"])
def category_posts(request, cat_id):
    # 특정 카테고리가 존재하는지 확인하는 부분
    category = get_object_or_404(Category, pk=cat_id)

    # 해당 카테고리에 속한 게시글 필터링, 그리고 최신 작성 순으로 정렬
    posts = Post.objects.filter(
        postcategory__cat_id=category  # PostCategory를 통해 카테고리 필터링
        # postcategory는 Post 모델에서 PostCategory로의 역참조 관계임
        # postcategory__cat_id=category 는 해당 카테고리(cat_id)에 연결된 모든 Post를 필터링함
    ).order_by('-created') # 최신순 정렬 (내림차순 정렬)

    # 게시글 데이터를 JSON 형식으로 변환
    posts_json_all = []
    for post in posts:
        post_json = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "status": post.status,
            "user": post.user.id,
        }
        posts_json_all.append(post_json)

    return JsonResponse({
        'status': 200,
        'message': f'카테고리 ID {cat_id}에 해당하는 게시글 조회 성공',
        'data': posts_json_all
    })