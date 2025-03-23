from django.urls import path
from posts.views import *

urlpatterns = [
    #경로를 지정하지 않은 것(공백)이 django_review 함수를 바라보게 설정
    path('', django_review, name = 'django_review'),
    #예를 들어, 'books' 경로로 접근하면 book_list를 호출하려면
    #path("books/", book_list),
    path('page', index, name='my-page'),
]