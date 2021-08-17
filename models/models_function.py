import datetime

from pytz import timezone

# model에서 공통으로 사용하는 함수들을 모아두는곳


def get_now_time():
    return datetime.datetime.now(timezone('Asia/Seoul'))
