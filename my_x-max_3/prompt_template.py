# sns_post/
#  ├─ main.py
#  ├─ prompt_template.py
#  └─ .env -> OPENAI_API_KEY="your_api_key_here"

# prompt_template.py

def hashtag_range(platform):
    """플랫폼별 해시태그 권장 개수(최소, 최대)를 반환하는 도우미 함수입니다."""
    
    # 4. 의사 결정 (Decision Making) - 내부 로직
    # 🖐 [검사]: 플랫폼이 인스타그램인지 확인합니다.
    if platform == "Instagram":
        return (5, 10)  # (최소 5개, 최대 10개) 튜플(Tuple) 형태로 반환합니다.
    
    # 🖐 [검사]: 플랫폼이 페이스북인지 확인합니다.
    elif platform == "Facebook":
        return (3, 5)
    
    # 🖐 [검사]: 그 외(LinkedIn 등)인 경우입니다.
    else:  # LinkedIn
        return (1, 3)

def build_prompt(platform, topic, style):
    """입력된 정보와 플랫폼별 규칙을 조합하여 최종 프롬프트를 생성합니다."""

    # 5. 도구 실행 (내부 함수 호출)
    # 👌 [실행]: 위에서 정의한 hashtag_range 함수를 호출하여 범위 값을 가져옵니다.
    # 반환된 튜플 (min, max)를 min_ht와 max_ht 변수에 각각 풀어서 담습니다. (Unpacking)
    min_ht, max_ht = hashtag_range(platform)

    # 2. 컨텍스트 관리 (Context Management)
    # ✍️ [기록]: f-string을 사용하여 AI에게 보낼 지시서를 작성합니다.
    # {min_ht}, {max_ht} 부분에 위에서 계산한 숫자가 자동으로 들어갑니다.
    return f"""
당신은 {platform} 전문 SNS 콘텐츠 기획자입니다.
다음 조건을 만족하는 소셜 미디어 포스팅 문구를 작성하십시오.

[조건]
① 주제: {topic}
② 스타일: {style}
③ 플랫폼: {platform}

[플랫폼별 규칙]
- Instagram: 감성적 표현, 문단 구분, 해시태그 {min_ht}~{max_ht}개
- Facebook: 간결한 단문 중심, 해시태그 {min_ht}~{max_ht}개
- LinkedIn: 전문가 톤, 핵심 메시지 중심, 해시태그 {min_ht}~{max_ht}개

[출력 형식]
1) 본문(자연스럽고 명확한 문장)
2) 해시태그 목록({min_ht}~{max_ht}개 범위 준수)

문장은 실제 플랫폼에서 바로 사용할 수 있도록 자연스럽게 작성하십시오.
"""