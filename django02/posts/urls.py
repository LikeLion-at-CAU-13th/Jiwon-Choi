from django.urls import path
from posts.views import *

urlpatterns = [
    #경로를 지정하지 않은 것(공백)이 django_review 함수를 바라보게 설정
    # path('', django_review, name = 'django_review'),
    #예를 들어, 'books' 경로로 접근하면 book_list를 호출하려면
    #path("books/", book_list),
    # path('page', index, name='my-page'),

    # 결과를 반환받기 위해 url 추가?
    # int:id는 변화할 수 있는 값들. 1번을 넣으면 1번에 해당하는 게시글이 반환되게 하는 역할을 함
    
    # path('<int:id>', get_post_detail)

    # 5주차 2개
    path('', post_list, name="post_list"),
    path('<int:post_id>/', post_detail, name='post_detail'), #Post 단일 조회
    path('<int:post_id>/comments/', post_comments, name='post_comments'), #comment 검색 부분
    path('category/<int:cat_id>/', category_posts, name='category_posts'), #category별로
]