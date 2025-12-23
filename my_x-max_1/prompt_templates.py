# llm_ad_project/
#  ├── main.py              # 광고 생성기 실행 파일
#  ├── llm_utils.py         # LLM 호출 함수 모듈
#  └── prompt_templates.py  # 프롬프트 템플릿 모음

# prompt_templates.py

# 2. 컨텍스트 관리 (Context Management)
# ✍️ [기록]: 광고 생성을 위한 기본 틀(Template)을 상수 변수로 정의합니다. (외부 라이브러리 불필요)
# 나중에 main.py에서 .format(product=..., message=...)을 통해 {괄호} 부분이 실제 내용으로 바뀝니다.
AD_TEMPLATE = """
당신은 디지털 마케팅 카피라이터입니다.
다음 정보를 바탕으로 광고 문구를 작성하시오.

제품/서비스: {product}
핵심 메시지: {message}

출력 형식:
1) 헤드라인 1문장
2) 설명 문장 1문장
3) 행동 유도 문구(CTA) 1문장
"""
