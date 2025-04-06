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
    
class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=30)

    def __str__(self):
        return self.cat_name

class PostCategory(models.Model):
    cat_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post_id.title} - {self.cat_id.cat_name}'
    
class Comment(BaseModel):
    comment_id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete= models.CASCADE, related_name='comment')
    comment_name = models.CharField(max_length=100)
    comment_content = models.TextField()

    def __str__(self):
        return self.comment_content


