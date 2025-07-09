### Model Serializer case

from datetime import datetime
from config.custom_api_exceptions import PostConflictException, DailyPostLimitException
from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):

  class Meta:
		# 어떤 모델을 시리얼라이즈할 건지
    model = Post
		# 모델에서 어떤 필드를 가져올지
		# 전부 가져오고 싶을 때 아래처럼
    fields = "__all__"
    
  # 중복된 게시글 제목이 있다면 예외 발생
  def validate(self, data):
    if Post.objects.filter(title=data['title']).exists():
      raise PostConflictException(detail=f"A post with title: '{data['title']}' already exists.")
    
    # 14주차 과제 3 - user 당 1개의 게시글만 작성할 수 있게 제한
    user = data.get('user')
    if user:
      today = datetime.now().date()
      #이미 게시글 작성했는지
      already_posted = Post.objects.filter(
        user=user,
        created__date=today
      ).exists()
      if already_posted:
        raise DailyPostLimitException(
          detail="사용자 당 하루에 하나의 게시글만 작성할 수 있습니다."
        )

    return data

class CommentSerializer(serializers.ModelSerializer):

  class Meta:
		# 어떤 모델을 시리얼라이즈할 건지
    model = Comment
		# 모델에서 어떤 필드를 가져올지
		# 전부 가져오고 싶을 때 아래처럼
    fields = "__all__"
  
  # 14주차 과제 2 - 댓글 15자 이상  
  def validate_comment_content(self, value):
    # 최소 15자 이상인지 확인 
    if len(value.strip()) < 15:
      raise serializers.ValidationError(
        "댓글 내용은 최소 15자 이상이어야 합니다."
      )
    return value


#12주차 추가 - 이미지 업로드 api
from .models import Image
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

  