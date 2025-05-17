from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.utils import timezone
from datetime import datetime, time

class TimeRestrictedPermission(BasePermission):
    message = "지금은 사용할 수 없는 시간입니다."

def has_permission(self, request, view):
        now = timezone.localtime().time()

        if time(22, 0) <= now or now <= time(7, 0):
            return False
        return True

class IsOwnerOrReadOnly(BasePermission):
    message = "작성자만 수정할 수 있습니다."

    def has_object_permission(self, request, view, obj):
        # print(f"request.user: {request.user} / obj.user: {obj.user}")
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user