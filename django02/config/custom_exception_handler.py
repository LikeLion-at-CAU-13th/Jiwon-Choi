from rest_framework.views import exception_handler
from rest_framework.exceptions import ErrorDetail

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data = _create_unified_response(response)

    return response

def _create_unified_response(response):
    error_detail = _extract_error_detail(response.data)

    result = {
        'success': False,
        'error': {
            'code': error_detail.get('code', 'DRF-API-ERROR'),
            'message': error_detail.get('message', 'An error occurred.'),
            'status_code': response.status_code,
        }
    }
    # 14주차 과제 1 - 필드값 전달 X 시 어떤 필드에 어떤 문제가 있는지 알 수 있게
    if 'errors' in error_detail:
        result['error']['errors'] = error_detail['errors']
    # if 'field_details' in error_detail:
    #     result['error']['field_details'] = error_detail['field_details']
    return result

def _extract_error_detail(error_data):
    print(f"Extracting error detail from: {error_data}")
    # 14주차 과제 1 - 필드값 전달 X 시 어떤 필드에 ~ 
    # 필드별 에러 메시지 수집하는 부분!
    if isinstance(error_data, dict):
        field_errors = []
        for field, messages in error_data.items():

            if isinstance(messages, list):
                for msg in messages:
                    #DRF가 반환한 ErrorDetail 객체 처리
                    if isinstance(msg, ErrorDetail):
                        field_errors.append({
                            "field": field,
                            "message": str(msg),
                            "code": getattr(msg, 'code', 'validation_error')
                        })
                    else : #메시지가 단순 문자열인 경우
                        field_errors.append({
                            "field": field,
                            "message": str(msg),
                            "code": "validation_error"
                        })
            else : #메시지가 리스트가 아니라 단일 값(문자열 등등)인 경우 바로 dict로 변환해 추가
                field_errors.append({
                    "field": field,
                    "message": str(messages),
                    "code": "validation_error"
                })

        if field_errors: # 필드별 에러가 하나라도 있다면
            return {
                'message': f"{len(field_errors)} validation errors occurred",
                'code': 'validation_error',
                'errors': field_errors#, # 위에서 만든 것
                # 'field_details': error_data # 원본 error_data 전체를 담은 dict 반환
            }

    
    if isinstance(error_data, str):
        return {
            'message': error_data,
            'code': 'api_error'
        }
    
    if isinstance(error_data, list) and error_data:
        first_error = error_data[0]
        if isinstance(first_error, str):
            return {
                'message': first_error, 
                'code': 'validation_error'
            }
        elif isinstance(first_error, dict):
            return _extract_error_detail(first_error)
        
    if isinstance(error_data, ErrorDetail):
        return {
            'message': str(error_data),
            'code': getattr(error_data, 'code', 'unknown_error')
        }
    
    if isinstance(error_data, dict):
        if 'message' in error_data and 'code' in error_data:
            return error_data
        
        if 'detail' in error_data:
            return {
                'message': str(error_data['detail']),
                'code': getattr(error_data['detail'], 'code', 'unknown_error')
            }
        
        field_errors = []
        for field, messages in error_data.items():
            if isinstance(messages, list) and messages:
                field_errors.append(f"{field}: {messages[0]}")
            else:
                field_errors.append(f"{field}: {str(messages)}")
        
        if field_errors:
            return {
                'message': f"{len(field_errors)} validation errors occurred",
                'code': 'validation_error',
                'errors': field_errors #,
                # 'field_details': error_data
            }
    
    return {
        'message': str(error_data),
        'code': 'unknown_error'
    }
