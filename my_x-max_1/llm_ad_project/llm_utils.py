# llm_utils.py
from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_llm(prompt: str,
            model: str = "gpt-4o-mini",
            temperature: float = 0.7,
            max_retries: int = 3,
            retry_delay: float = 2.0) -> str:
    """기본 LLM 호출 함수입니다."""
    for attempt in range(1, max_retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"[오류] 시도 {attempt}/{max_retries}: {e}")
            if attempt == max_retries:
                return "AI 응답을 가져오는 데 실패했습니다."
            time.sleep(retry_delay)
