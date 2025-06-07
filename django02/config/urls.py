from django.contrib import admin
from django.urls import path, include
from posts.views import *



urlpatterns = [
    path("admin/", admin.site.urls),
    path('post/', include('posts.urls')),
    path('account/', include('accounts.urls')),
]

#    path('', include('posts.urls')),
# 아무것도 붙이지 않으면 'posts.urls'로 이동하게 됨

#12주차 swagger ui 접속 위한 url 설정
from accounts.views import *

from rest_framework import permissions #추가
from drf_yasg.views import get_schema_view #추가
from drf_yasg import openapi #추가

# Swagger 설정
schema_view = get_schema_view(
    openapi.Info(
        title="Post API",
        default_version="v1",
        description="게시글 API 문서",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Swagger 접근 가능하도록 설정
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("post/", include("posts.urls")),
    path("account/", include("accounts.urls")),
    path("account/", include("allauth.urls")),

    #Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]