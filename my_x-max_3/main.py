
# sns_post/
#  ├─ main.py
#  ├─ prompt_template.py
#  └─ .env -> OPENAI_API_KEY="your_api_key_here"

# main.py
from openai import OpenAI  # OpenAI의 AI 모델을 사용하기 위해 공식 라이브러리를 불러옵니다. (터미널 설치: pip install openai)
from dotenv import load_dotenv  # .env 파일에서 API 키를 가져오기 위해 불러옵니다. (터미널 설치: pip install python-dotenv)
import os  # 운영체제 기능(환경변수 등)을 사용하기 위해 불러옵니다. (기본 내장)
# 우리가 만든 프롬프트 템플릿 파일에서 함수를 가져옵니다. (로컬 파일: pip 설치 불필요 / prompt_template.py 필요)
from prompt_template import build_prompt

# 1. 환경 설정
load_dotenv()  # .env 파일의 내용을 환경변수로 로드합니다.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 클라이언트 객체를 생성합니다.

def normalize_platform(p):
    """사용자가 입력한 플랫폼 이름을 표준 형태(Instagram/Facebook/LinkedIn)로 변환합니다."""
    
    # 6. 데이터 처리 (전처리)
    # ✍️ [기록]: 입력값의 앞뒤 공백을 없애고 소문자로 바꿉니다.
    p = p.strip().lower()
    
    # 4. 의사 결정 (Decision Making)
    # 🖐 [검사]: 입력값이 인스타그램 관련 단어인지 확인합니다.
    if p in ["instagram", "insta", "인스타"]:
        return "Instagram"
    # 🖐 [검사]: 페이스북 관련 단어인지 확인합니다.
    elif p in ["facebook", "fb", "페북"]:
        return "Facebook"
    # 🖐 [검사]: 링크드인 관련 단어인지 확인합니다.
    elif p in ["linkedin", "linkd", "li", "링크드인"]:
        return "LinkedIn"
    # 🖐 [검사]: 맞는게 없으면 None을 반환합니다.
    else:
        return None

def main():
    # 프로그램 시작 안내
    # 👍 [출력]: 제목을 화면에 표시합니다.
    print("=== SNS 포스팅 자동 생성기 ===")

    # 1. 대화 시작
    # 👇 [입력 대기]: 사용자에게 플랫폼 이름을 입력받습니다.
    raw_platform = input("플랫폼 선택(Instagram / Facebook / LinkedIn): ")
    
    # 5. 도구 실행 (데이터 정규화)
    # 👌 [실행]: 입력받은 날것의 데이터를 깨끗한 표준 이름으로 바꿉니다.
    platform = normalize_platform(raw_platform)

    # 4. 의사 결정 (유효성 검사)
    # 🖐 [검사]: 만약 지원하지 않는 플랫폼이라면 프로그램을 종료합니다.
    if platform is None:
        print("지원하지 않는 플랫폼입니다. 프로그램을 종료합니다.")
        return  # 함수 종료

    # 👇 [입력 대기]: 포스팅 주제를 입력받습니다.
    topic = input("포스팅 주제: ").strip()
    # 👇 [입력 대기]: 글의 분위기(톤)를 입력받습니다.
    style = input("톤 선택(감성형 / 전문가형 / 친근한 톤): ").strip()

    # 3. 추론 요청 (함수 호출)
    # 👆 [AI 호출]: 포스팅 생성 함수를 실행하여 결과를 받아옵니다.
    post = generate_post(platform, topic, style)

    # 8. 최종 응답
    # 👍 [출력]: 최종 생성된 포스팅을 화면에 보여줍니다.
    print("\n=== 생성된 포스팅 ===\n")
    print(post)

def generate_post(platform, topic, style):
    """설정된 정보를 바탕으로 AI에게 포스팅 작성을 요청합니다."""
    
    # 2. 컨텍스트 관리
    # ✍️ [기록]: prompt_template.py에 있는 함수를 써서 AI에게 보낼 지시문을 만듭니다.
    prompt = build_prompt(platform, topic, style)

    # 3. 추론 요청
    # 👆 [AI 호출]: 완성된 프롬프트를 가지고 OpenAI API에 요청을 보냅니다.
    resp = client.chat.completions.create(
        model="gpt-4o-mini",  # 가성비 좋은 모델 사용
        messages=[{"role": "user", "content": prompt}],  # 프롬프트 전달
        temperature=0.7  # 창의성 설정
    )

    # 6. 결과 처리
    # 🤜 [결과 저장]: AI의 응답 텍스트만 추출해서 반환합니다.
    return resp.choices[0].message.content

if __name__ == "__main__":  # 이 파일이 직접 실행될 때만 main()을 시작합니다.
    main()
