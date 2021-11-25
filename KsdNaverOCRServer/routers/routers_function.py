import os
from inspect import currentframe


# router에서 공통적으로 사용하는 함수


# api summary에 함수가 위치한 파일 이름과 함주 위치 라인 수를 보여주는 함수
# api에서 사용시 summary= FUNCTION_NAME  + " : "  + get_summary_location()
# 위와 같이 사용
def get_summary_location(current_frame=currentframe):
    return f"File '{current_frame().f_back.f_locals['__name__']}', line {current_frame().f_back.f_lineno}"