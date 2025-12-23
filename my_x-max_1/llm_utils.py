# llm_ad_project/
#  ├── main.py              # 광고 생성기 실행 파일
#  ├── llm_utils.py         # LLM 호출 함수 모듈
#  └── prompt_templates.py  # 프롬프트 템플릿 모음

# llm_utils.py

from openai import OpenAI  # OpenAI의 AI 모델을 사용하기 위해 공식 라이브러리를 불러옵니다. (터미널 설치: pip install openai)
from dotenv import load_dotenv  # .env 파일에서 API 키를 가져오기 위해 불러옵니다. (터미널 설치: pip install python-dotenv)
import os  # 운영체제 기능(환경변수 등)을 사용하기 위해 불러옵니다. (기본 내장)
import time  # 재시도 전 대기 시간(sleep)을 주기 위해 불러옵니다. (기본 내장)

load_dotenv()  # .env 파일의 내용을 메모리에 올립니다.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 환경변수에서 꺼낸 키로 클라이언트를 설정합니다.

def ask_llm(prompt: str,
            model: str = "gpt-4o-mini",
            temperature: float = 0.7,
            max_retries: int = 3,
            retry_delay: float = 2.0) -> str:
    """기본 LLM 호출 함수입니다. 실패 시 재시도 기능이 포함되어 있습니다."""
    
    # 🔄 [반복]: 정해진 횟수(max_retries)만큼 성공할 때까지 반복 시도합니다.
    for attempt in range(1, max_retries + 1):
        try:
            # 3. 추론 요청 (Inference Request)
            # 👆 [AI 호출]: 설정된 모델과 프롬프트로 OpenAI 서버에 요청을 보냅니다.
            resp = client.chat.completions.create(
                model=model,  # 사용할 모델 (기본값: gpt-4o-mini)
                temperature=temperature,  # 창의성 조절
                messages=[{"role": "user", "content": prompt}]  # 사용자 메시지 전달
            )
            
            # 6. 결과 처리 (Data Processing)
            # 🤜 [결과 저장]: [중요] 최신 버전에서는 딕셔너리가 아닌 객체 속성(.content)으로 접근해야 합니다.
            return resp.choices[0].message.content

        except Exception as e:
            # 2. 컨텍스트 관리 (에러 로그)
            # ✍️ [기록]: 에러가 발생하면 현재 몇 번째 시도인지와 에러 내용을 출력합니다.
            print(f"[오류] 시도 {attempt}/{max_retries}: {e}")
            
            # 4. 의사 결정 (Decision Making)
            # 🖐 [검사]: 만약 이번이 마지막 시도였는지 확인합니다.
            if attempt == max_retries:
                # 8. 최종 응답 (실패 시)
                # 👍 [출력]: 모든 시도가 실패했다면 사용자에게 실패 메시지를 반환합니다.
                return "AI 응답을 가져오는 데 실패했습니다."
            
            # 🔄 [반복] 대기: 다음 시도 전, 서버 과부하를 막기 위해 잠시 기다립니다.
            time.sleep(retry_delay)