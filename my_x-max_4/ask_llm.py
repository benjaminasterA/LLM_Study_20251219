# ---------------------------------------------------------
# [Import 순서 정리]
# 1. 파이썬 내장 모듈
# 2. 서드파티 라이브러리
# ---------------------------------------------------------

# ① 파이썬 내장 모듈 (Standard Library) - 설치 불필요
import os  # 운영체제(Operating System) 기능을 사용하여 환경변수를 가져오기 위해 불러옵니다. 💻

# ② 서드파티 라이브러리 (Third-party Libraries) - 설치 필요
from openai import OpenAI  # OpenAI(오픈에이아이) API 사용을 위한 클라이언트입니다. (터미널 설치: pip install openai) 🤖
from dotenv import load_dotenv  # .env 파일에서 환경변수를 로드하기 위한 라이브러리입니다. (터미널 설치: pip install python-dotenv) 🔐

# ---------------------------------------------------------
# [설정 및 클라이언트 초기화]
# ---------------------------------------------------------
load_dotenv()  # .env 파일의 API 키 정보를 환경변수로 메모리에 로드합니다. 📂
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 로드된 키를 사용하여 OpenAI 클라이언트(Client)를 생성합니다. 🔗

# ---------------------------------------------------------
# [시스템 프롬프트 설정]
# AI에게 부여할 역할(Persona)과 제약사항을 정의합니다.
# ---------------------------------------------------------
system_prompt = '''
당신은 전문 콘텐츠 크리에이터이자 마케팅 전문가입니다.
현재 날짜는 2025년 12월이므로 과거 연도(2024 이전)를 언급하지 마십시오.
모든 콘텐츠는 2025년 12월의 트렌드, 소비자 행동, 플랫폼 알고리즘, 언어 사용을 반영해야 합니다.
'''

def create_script(prompt: str) -> str:  # 프롬프트를 입력받아 완성된 스크립트 문자열을 반환하는 함수입니다. ✍️
    
    # 📡 [API 호출]: LLM에게 요청을 보냅니다.
    response = client.chat.completions.create(
        model="gpt-4o",  # 사용할 AI 모델(Model)입니다. (최신 모델인 gpt-4o 사용) 🚀
        messages=[  # 대화의 문맥(Context)을 구성하는 메시지 리스트입니다. 📜
            {"role": "system", "content": system_prompt},  # 시스템(System): AI의 역할과 규칙을 설정합니다. ⚙️
            {"role": "user", "content": prompt}  # 사용자(User): 실제로 요청할 광고 주제나 내용을 전달합니다. 👤
        ],
        temperature=0.7  # 창의성(Temperature) 지수입니다. (0.0은 정적, 1.0은 매우 창의적. 0.7은 마케팅에 적절한 균형값) 🌡️
    )
    
    # 🎁 [결과 처리]: 응답 객체에서 텍스트 내용만 추출하여 반환합니다.
    return response.choices[0].message.content
