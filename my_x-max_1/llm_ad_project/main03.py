# main.py
from llm_utils import ask_llm
from prompt_templates import AD_TEMPLATE

def main():
    print("=== 광고 콘텐츠 생성기 v2 ===")

    product = input("제품/서비스 이름을 입력하세요: ").strip()
    message = input("핵심 메시지를 한 줄로 입력하세요: ").strip()

    prompt = AD_TEMPLATE.format(product=product, message=message)
    ad_text = ask_llm(prompt, temperature=0.8)

    print("\n[생성된 광고 문구]")
    print(ad_text)

if __name__ == "__main__":
    main()
