# llm_ad_project/
#  ├── main.py              # 광고 생성기 실행 파일
#  ├── llm_utils.py         # LLM 호출 함수 모듈
#  └── prompt_templates.py  # 프롬프트 템플릿 모음

# llm_utils.py

# llm_utils.py
from openai import OpenAI  # OpenAI의 AI 모델을 사용하기 위해 공식 라이브러리를 불러옵니다. (터미널 설치: pip install openai)
from dotenv import load_dotenv  # .env 파일에서 API 키를 가져오기 위해 불러옵니다. (터미널 설치: pip install python-dotenv)
import os  # 운영체제 기능(환경변수 등)을 사용하기 위해 불러옵니다. (기본 내장)
import time  # 재시도 시 대기 시간을 주기 위해 불러옵니다. (기본 내장)

load_dotenv()  # .env 파일에서 OPENAI_API_KEY 로드
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 클라이언트 객체 생성


def ask_llm(prompt: str,
            model: str = "gpt-4o-mini",
            temperature: float = 0.7,
            max_retries: int = 3,
            retry_delay: float = 2.0) -> str:
    """기본적인 LLM 호출 함수 (재시도 포함)."""
    
    # 🔄 [반복]: 네트워크 오류 등에 대비해 정해진 횟수만큼 재시도합니다.
    for attempt in range(1, max_retries + 1):
        try:
            # 3. 추론 요청 (Inference Request)
            # 👆 [AI 호출]: 설정된 프롬프트와 옵션으로 OpenAI 서버에 요청을 보냅니다.
            resp = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # 6. 결과 처리 (Data Processing)
            # 🤜 [결과 저장]: 응답 객체에서 텍스트 내용(.content)만 추출하여 반환합니다.
            return resp.choices[0].message.content

        except Exception as e:
            # 2. 컨텍스트 관리 (에러 로그)
            # ✍️ [기록]: 에러가 발생하면 로그를 남기고, 마지막 시도가 아니면 재시도합니다.
            print(f"[오류] 시도 {attempt}/{max_retries}: {e}")
            if attempt == max_retries:
                # 8. 최종 응답 (실패 시)
                return "AI 응답을 가져오는 데 실패했습니다."
            
            # 🔄 [반복] 대기: 서버 과부하를 막기 위해 잠시 멈춥니다.
            time.sleep(retry_delay)


def evaluate_ad(ad_text: str, template: str) -> int:
    """광고 문구 1개를 평가하여 총점을 정수로 반환."""
    
    # 2. 컨텍스트 관리
    # ✍️ [기록]: 평가용 템플릿에 실제 광고 문구를 채워 넣어 프롬프트를 완성합니다.
    # (주의: template 문자열 안에 {ad_text} 라는 구멍이 있어야 합니다)
    prompt = template.format(ad_text=ad_text)
    
    # 3. 추론 요청
    # 👆 [AI 호출]: 점수 평가는 일관성이 중요하므로 창의성(temperature)을 0.0으로 낮춰서 호출합니다.
    result = ask_llm(prompt, temperature=0.0)

    # 6. 결과 처리 (점수 파싱)
    # 🔄 [반복]: AI의 응답을 한 줄씩 읽으며 '총점'이라는 단어를 찾습니다.
    for line in result.splitlines():
        # 🖐 [검사]: 해당 줄에 "총점"이라는 키워드가 있는지 확인합니다.
        if "총점" in line:
            # 🤜 [결과 저장]: "총점: 8점" 같은 문자열에서 숫자(8)만 추출합니다.
            num = "".join(c for c in line if c.isdigit())
            # 숫자가 있으면 정수(int)로 변환해 반환하고, 없으면 0을 반환합니다.
            return int(num) if num.isdigit() else 0

    # 파싱에 실패한 경우 0점을 반환합니다.
    return 0
