# ------------------------------------------------------------
# 필요한 라이브러리 불러오기
# ------------------------------------------------------------
from openai import OpenAI           # OpenAI API 사용 라이브러리
from dotenv import load_dotenv      # .env 파일에서 환경변수 로드
import numpy as np                 # 코사인 유사도 계산용
import os                          # 환경 변수 접근용


# ------------------------------------------------------------
# 환경 변수 로드 및 클라이언트 초기화
# ------------------------------------------------------------
load_dotenv()                                        # .env에 저장된 API 키 불러오기
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # 클라이언트 객체 생성


# ------------------------------------------------------------
# 6. Embedding API 실습
# ------------------------------------------------------------

# 6.1 임베딩 생성 예제
text = "서울시는 대한민국의 수도입니다."  # 임베딩을 생성할 텍스트

# 임베딩 생성 요청
embedding = client.embeddings.create(
    model="text-embedding-3-small",  # 임베딩 모델
    input=text                       # 입력 텍스트
)

# 임베딩 벡터 일부(앞 10개 값) 출력
print("임베딩 일부:", embedding.data[0].embedding[:10])


# ------------------------------------------------------------
# 6.2 코사인 유사도 계산 함수 정의
# ------------------------------------------------------------
def cosine_similarity(a, b):
    """
    두 벡터 a, b의 코사인 유사도를 계산하는 함수
    값의 범위: -1 ~ 1 (1에 가까울수록 유사함)
    """
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# 임베딩 테스트용
vec1 = embedding.data[0].embedding
vec2 = embedding.data[0].embedding  # 동일 벡터이므로 유사도 1.0에 가까움

similarity = cosine_similarity(vec1, vec2)
print("코사인 유사도:", similarity)


# ------------------------------------------------------------
# 7. Whisper (음성 → 텍스트) / TTS (텍스트 → 음성)
# ------------------------------------------------------------

# Whisper 예제
# ------------------------------------------------------------
# test.mp3 파일을 읽어서 Whisper 모델로 음성을 텍스트로 변환

audio_file = open("test.mp3", "rb")  # 변환할 음성 파일

result = client.audio.transcriptions.create(
    model="whisper-1",                # Whisper 음성 인식 모델
    file=audio_file                   # 음성 파일 전달
)

# 음성에서 추출된 텍스트 출력
print("Whisper 결과:", result.text)


# ------------------------------------------------------------
# TTS(Text To Speech) 예제
# ------------------------------------------------------------
# 텍스트를 음성으로 변환하고 output.mp3 파일로 저장하는 예제

# TTS(Text to Speech) 예제 - 파일로 저장

speech = client.audio.speech.create(
    model="gpt-4o-mini-tts",    # TTS 모델
    voice="alloy",              # 사용할 음성 스타일
    input="안녕하세요. VS Code에서 음성을 생성하고 있습니다."   # 변환할 텍스트
)
# 생성된 음성 데이터를 파일(output.mp3)로 저장
with open("output.mp3", "wb") as f:
    f.write(speech.read())   # 반드시 read() 사용!

print("TTS 음성 파일 생성 완료: output.mp3")

