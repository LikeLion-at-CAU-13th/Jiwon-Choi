# from django.db import models
# from accounts.models import User

# # Create your models here.
# class Post(models.Model):

#     #둘 중 하나를 고르는 것
#     # status 부분에서, 게시글의 상태를 나타낼 때 사용 
#     CHOICES = (
#         ('STORED', '보관'),
#         ('PUBLISHED', '발행')
#     )

#     #id는 autofield로 함
#     id = models.AutoField(primary_key=True)
#     # max_length 지정
#     title = models.CharField(max_length=30)
#     # max length 없는...? @@
#     content = models.TextField()
#     #status -> default를 store로 설정함
#     status = models.CharField(max_length=15, choices=CHOICES, default='STORED')
#     created = models.DateTimeField(auto_now_add=True) # 객체를 생성할 때 날짜와 시간 저장
#     updated = models.DateTimeField(auto_now=True)  # 객체를 저장할 때 날짜와 시간 갱신
#     #외래키
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')

#     # title을 리턴하게 됨.
#     def __str__(self): # 표준 파이썬 클래스 메서드, 사람이 읽을 수 있는 문자열을 반환하도록 함
#         return self.title
    




    #baseModel 활용하는 버전
from django.db import models
from accounts.models import User

# Create your models here.
# 추상 클래스 정의
class BaseModel(models.Model): # models.Model을 상속받음
    created = models.DateTimeField(auto_now_add=True) # 객체를 생성할 때 날짜와 시간 저장
    updated = models.DateTimeField(auto_now=True) # 객체를 저장할 때 날짜와 시간 갱신

    #추상 클래스를 의미한다
    class Meta:
        abstract = True


class Post(BaseModel): # BaseModel을 상속받음

    CHOICES = (
        ('STORED', '보관'),
        ('PUBLISHED', '발행')
    )

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30)
    content = models.TextField()
    status = models.CharField(max_length=15, choices=CHOICES, default='STORED')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')

    #이부분 때문에 post 목록에서 title이 미리보기로 보인다
    # 수정하면 내용도 보임
    def __str__(self):
        return self.title