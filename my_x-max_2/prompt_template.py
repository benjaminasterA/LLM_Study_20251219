# youtube_script/
#  ├─ main.py
#  ├─ prompt_template.py
#  └─ .env

# prompt_template.py

def decide_keypoints(duration):
    """영상 길이에 따라 필요한 핵심 메시지 개수를 결정합니다."""
    
    # 4. 의사 결정 (Decision Making) - 내부 로직
    # 🖐 [검사]: 입력된 길이가 "1분"인지 확인합니다.
    if duration == "1분":
        return 2  # 1분이면 핵심 메시지 2개 반환
    
    # 🖐 [검사]: 입력된 길이가 "3분"인지 확인합니다.
    elif duration == "3분":
        return 3  # 3분이면 핵심 메시지 3개 반환
    
    # 🖐 [검사]: 그 외의 경우(5분 등) 확인합니다.
    else:
        return 5  # 긴 영상은 핵심 메시지 5개 반환

def build_prompt(topic, duration, style):
    """주제, 길이, 스타일을 받아 최종 프롬프트를 완성합니다."""
    
    # 2. 컨텍스트 관리 (Context Management)
    # 🖐 [검사] -> 👌 [실행]: 위에서 만든 도우미 함수를 실행하여 키포인트 개수를 받아옵니다.
    # (코드 중복을 피하기 위해 함수를 호출하여 값을 할당합니다.)
    keypoints = decide_keypoints(duration)

    # ✍️ [기록]: f-string을 사용하여 AI에게 보낼 최종 작업 지시서를 작성합니다.
    prompt = f"""
당신은 유튜브 영상 전문 작가입니다. 
아래 조건에 따라 영상 스크립트를 작성하세요.

[조건]
① 주제: {topic}
② 영상 길이: {duration}
③ 스타일: {style}

[작성 형식]
1) 도입부
2) 본문({keypoints}개의 핵심 메시지 포함)
3) 결론 및 CTA

문장은 자연스럽고 명료하게 작성합니다.
"""
    # 🤜 [결과 저장]: 완성된 프롬프트 문자열을 반환합니다.
    return prompt
