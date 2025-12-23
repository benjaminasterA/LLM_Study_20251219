# llm_ad_project/
#  ├── main.py              # 광고 생성기 실행 파일
#  ├── llm_utils.py         # LLM 호출 함수 모듈
#  └── prompt_templates.py  # 프롬프트 템플릿 모음

# prompt_templates.py

# --- 1. 생성기(Generator)용 템플릿 ---
# 2. 컨텍스트 관리 (Context Management)
# ✍️ [기록]: AI에게 광고를 만들어달라고 요청할 때 사용하는 기본 틀입니다.
# main.py에서 {product}와 {message} 부분이 사용자의 입력값으로 채워집니다.
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


# --- 2. 평가기(Evaluator)용 템플릿 ---
# 2. 컨텍스트 관리 (Context Management)
# ✍️ [기록]: 생성된 광고를 AI가 스스로 평가(Self-Refletion)하기 위한 심사 기준표입니다.
# {ad_text} 부분에 앞서 생성된 광고 문구가 들어갑니다.

# 🖐 [검사] (Parsing Rule): llm_utils.py의 evaluate_ad 함수가 점수를 추출할 수 있도록,
# '총점: X' 형식을 반드시 지키라고 AI에게 강하게 지시해야 합니다.
EVALUATOR_TEMPLATE = """
당신은 광고 카피 전문 평가관입니다.

아래 광고 문구를 명확성, 설득력, 창의성 기준으로 평가하십시오.
각 기준은 1~10점으로 채점하고, 마지막에 총점을 제시하십시오.

광고 문구:
{ad_text}

출력 형식(반드시 유지):
명확성: X
설득력: X
창의성: X
총점: X
"""
