import logging
from datetime import datetime

class RequestLoggingMiddleware:
    #미들웨어 초기화
    def __init__(self, get_response):
        self.get_response = get_response
        #self.logger는 django.request라는 이름의 로거를 가져옴 - settings.py에서 정의한 로깅 설정에 따라 동작함
        self.logger = logging.getLogger('django.request')  # 'django.request' 로거 사용

    #요청이 들어올 때 호출되는 메서드 - request 객체를 통해 HTTP 요청정보 가져옴
    def __call__(self, request):
        #log_data 딕셔너리로 로그에 기록할 데이터 정의
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'method': request.method, #GET/POST/PATCH/DELETE-HTTP 메서드
            'path': request.path,     #요청 URL 경로
        }
        #self.logger.info() 호출해서 로그 기록
        # extra=~~를 통해 추가 데이터를 전달함. 여기선 log_data
        #INFO 레벨로 로그 기록 (요청 URL 포함)
        self.logger.info(f"Request URL: {request.path}", extra=log_data)
        # self.logger.info(request.path, extra=log_data)
        #이렇게 해도 되는데 그냥 설명도 같이 넣음...

        #get_response(request)를 호출해 요청을 다음으로 전달
        return self.get_response(request)
