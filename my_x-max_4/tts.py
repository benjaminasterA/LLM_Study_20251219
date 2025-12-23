# ---------------------------------------------------------
# [Import 순서 정리]
# 1. 파이썬 내장 모듈
# 2. 서드파티 라이브러리
# ---------------------------------------------------------

# ① 파이썬 내장 모듈 (Standard Library) - 설치 불필요
import os  # 운영체제(OS)의 기능(파일 경로, 환경변수 등)을 사용하기 위한 모듈입니다. 💻
import time  # 시간(Time)과 관련된 기능을 다루기 위한 모듈입니다. (파일명 생성을 위해 사용) ⏱️

# ② 서드파티 라이브러리 (Third-party Libraries) - 설치 필요
from openai import OpenAI  # OpenAI(오픈에이아이) API 사용을 위한 클라이언트입니다. (터미널 설치: pip install openai) 🤖
from dotenv import load_dotenv  # 환경변수(.env) 파일을 로드하기 위한 라이브러리입니다. (터미널 설치: pip install python-dotenv) 🔐

# ---------------------------------------------------------
# [설정 및 클라이언트 초기화]
# ---------------------------------------------------------
load_dotenv()  # .env 파일에서 API 키를 환경변수로 불러옵니다. 📂
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 불러온 키로 클라이언트 객체를 생성합니다. 🔗

def text_to_speech(text):  # 텍스트를 음성으로 변환(Text to Speech)하는 함수입니다. 🗣️
    
    # 파일명 생성: 중복을 피하기 위해 현재 시간(Time Stamp)을 파일명에 포함합니다.
    filename = f"audio_{int(time.time())}.mp3"
    
    # 🔊 OpenAI 오디오 생성 API 호출
    response = client.audio.speech.create(
        model="tts-1",  # 사용할 TTS(티티에스) 모델입니다. (속도가 빠른 tts-1 사용) 🚀
        voice="fable",  # 목소리(Voice) 성우를 선택합니다. 🎤
        # -------------------------------------------------------
        # [목소리 옵션 참고]
        # "alloy"   : (얼로이)   - 여성 / 차분하고 중립적인 톤 😐
        # "echo"    : (에코)     - 남성 / 부드럽고 차분한 톤 🌊
        # "fable"   : (페이블)   - 공통 / 영국식 억양, 에너제틱함 ✨ (현재 선택됨)
        # "onyx"    : (오닉스)   - 남성 / 깊고 중후한 톤 🗿
        # "nova"    : (노바)     - 여성 / 밝고 활기찬 톤 ☀️
        # "shimmer" : (쉬머)     - 여성 / 맑고 부드러운 톤 💎
        # -------------------------------------------------------
        input=text  # 변환할 텍스트(Input) 내용입니다. 📝
    )

    # 생성된 오디오 데이터를 파일로 저장합니다.
    response.write_to_file(filename)
    
    return filename  # 저장된 파일의 이름(Filename)을 반환합니다. ↩️