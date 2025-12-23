# main.py
from openai import OpenAI
from dotenv import load_dotenv
import os

# ① .env 파일 로드 및 클라이언트 생성
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    print("=== 광고 콘텐츠 생성기 v0 ===")

    # ② 사용자 입력 받기
    product = input("제품/서비스 이름을 입력하세요: ").strip()
    message = input("핵심 메시지를 한 줄로 입력하세요: ").strip()

    # ③ 프롬프트 작성
    prompt = f"""
당신은 디지털 마케팅 카피라이터입니다.
다음 정보를 바탕으로 광고 문구를 작성하시오.

제품/서비스: {product}
핵심 메시지: {message}

출력 형식:
1) 헤드라인 1문장
2) 설명 문장 1문장
3) 행동 유도 문구(CTA) 1문장
"""

    # ④ LLM 호출
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    ad_text = resp.choices[0].message.content

    # ⑤ 결과 출력
    print("\n[생성된 광고 문구]")
    print(ad_text)

if __name__ == "__main__":
    main()
