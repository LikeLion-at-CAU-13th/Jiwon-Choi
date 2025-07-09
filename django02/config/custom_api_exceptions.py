from rest_framework.exceptions import APIException

class BaseCustomAPIException(APIException):
    status_code = 500
    default_detail = "An unexpected error occurred."
    default_code = "UNEXPECTED-ERROR"

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        
        if code is None:
            code = self.default_code
        
        super().__init__(detail=detail, code=code)

class ConflictException(BaseCustomAPIException):
    status_code = 409
    default_detail = "A conflict occurred."
    default_code = "CONFLICT"

class PostConflictException(ConflictException):
    default_detail = "A conflict occurred with the post."
    default_code = "POST-CONFLICT"

# 14주차 과제 - user 당 1개의 게시글 부분
class DailyPostLimitException(APIException):
    status_code = 400 # 429가 Too Many Requests이지만 429는 서버 과부하 막기 위한 것이라 400으로 수정
    default_detail = "Only one post can be posted per user per day."
    default_code = "DAILY_POST_LIMIT"
