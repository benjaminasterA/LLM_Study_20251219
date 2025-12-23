# ---------------------------------------------------------
# [Import 순서 정리]
# 1. 파이썬 내장 모듈
# 2. 서드파티 라이브러리
# ---------------------------------------------------------

# ① 파이썬 내장 모듈 (Standard Library) - 설치 불필요
import os  # 운영체제(OS) 기능을 사용하여 환경변수를 가져오기 위해 불러옵니다. 💻

# ② 서드파티 라이브러리 (Third-party Libraries) - 설치 필요
from openai import OpenAI  # OpenAI(오픈에이아이) API 사용을 위한 클라이언트입니다. (터미널 설치: pip install openai) 🤖
from dotenv import load_dotenv  # .env 파일에서 환경변수를 로드하기 위한 라이브러리입니다. (터미널 설치: pip install python-dotenv) 🔐

# ---------------------------------------------------------
# [설정 및 클라이언트 초기화]
# ---------------------------------------------------------
load_dotenv()  # .env 파일의 API 키 정보를 환경변수로 메모리에 로드합니다. 📂
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 로드된 키를 사용하여 OpenAI 클라이언트(Client)를 생성합니다. 🔗


def moderation_check(text: str) -> bool:
    """
    입력된 텍스트의 유해성을 검사합니다.
    :param text: 검사할 텍스트 문자열
    :return: 안전한 경우 True 반환, 유해한 경우 ValueError 발생
    """
    
    # 🛡️ [콘텐츠 모더레이션 체크 요청]
    # OpenAI의 최신 모더레이션 모델을 사용하여 텍스트를 분석합니다.
    check = client.moderations.create(
        model="omni-moderation-latest",  # 최신 다목적(Omni) 모더레이션 모델 사용 🚀
        input=text  # 검사할 텍스트 입력 📝
    )
    
    # 🚩 [결과 확인]
    # flagged(플래그드)가 True라면 정책 위반 내용이 포함되어 있다는 뜻입니다.
    if check.results[0].flagged:
        # 유해 콘텐츠가 감지되면 즉시 예외(Exception)를 발생시켜 진행을 중단합니다. 🛑
        # ValueError (밸류 에러): 값이 부적절할 때 사용하는 에러 타입
        raise ValueError("입력하신 내용이 부적절하여 처리할 수 없습니다.") 
    
    # 문제가 없다면 True를 반환하며 통과시킵니다. ✅
    return True