# youtube_script/
#  ├─ main.py
#  ├─ prompt_template.py
#  └─ .env

# main.py

from openai import OpenAI  # OpenAI의 AI 모델을 사용하기 위해 공식 라이브러리를 불러옵니다. (터미널 설치: pip install openai)
from dotenv import load_dotenv  # .env 파일에서 API 키를 가져오기 위해 불러옵니다. (터미널 설치: pip install python-dotenv)
import os  # 운영체제 기능(환경변수 등)을 사용하기 위해 불러옵니다. (기본 내장)
# prompt_template.py 파일에서 프롬프트 생성 함수를 가져옵니다. (로컬 파일: pip 설치 불필요)
from prompt_template import build_prompt 

# 1. 환경 설정
load_dotenv()  # .env 파일의 내용을 환경변수로 로드합니다.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 클라이언트 객체를 생성합니다.

def main():
    # 프로그램 시작 안내
    # 👍 [출력]: 프로그램 제목을 화면에 표시합니다.
    print("=== 유튜브 영상 스크립트 생성기 ===")

    # [수정됨] 입력 변수 정의가 함수 호출보다 먼저 와야 합니다.
    # 1. 대화 시작 (Start Conversation)
    # 👇 [입력 대기]: 사용자가 영상 주제를 입력할 때까지 기다립니다.
    topic = input("영상 주제를 입력하세요: ")
    # 👇 [입력 대기]: 사용자가 영상 길이를 입력할 때까지 기다립니다.
    duration = input("영상 길이(1분/3분/5분): ")
    # 👇 [입력 대기]: 사용자가 영상 스타일을 입력할 때까지 기다립니다.
    style = input("영상 톤(설명형/강의형/뉴스형): ")

    # 2. 컨텍스트 및 추론 요청
    # 여기서 바로 generate_script를 호출합니다.
    script = generate_script(topic, duration, style)
    
    # 8. 최종 응답 (Final Response)
    # 👍 [출력]: 최종 생성된 스크립트를 화면에 보여줍니다.
    print("\n=== 생성된 스크립트 ===\n")
    print(script)

def generate_script(topic, duration, style):
    """주제, 길이, 스타일을 받아 전체 스크립트를 생성합니다."""
    
    # 2. 컨텍스트 관리 (Context Management)
    # ✍️ [기록]: 별도 파일(prompt_template.py)에 정의된 함수를 사용해 프롬프트를 조립합니다.
    prompt = build_prompt(topic, duration, style)

    # 3. 추론 요청 (Inference Request)
    # 👆 [AI 호출]: 완성된 프롬프트를 가지고 OpenAI API에 요청을 보냅니다.
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 사용할 모델 (비용 효율적인 gpt-4o-mini 사용)
        messages=[{"role": "user", "content": prompt}],  # 프롬프트 전달
        temperature=0.7  # 창의성 조절 (적당히 창의적)
    )
    
    # 6. 결과 처리 (Data Processing)
    # 🤜 [결과 저장]: 응답 객체에서 텍스트 내용만 추출하여 반환합니다.
    return response.choices[0].message.content

if __name__ == "__main__":  # 이 파일이 직접 실행될 때만 main() 함수를 시작합니다.
    main()