# main_adcopy.py

# ---------------------------------------------------------
# [Import 순서 및 라이브러리 설명]
# ---------------------------------------------------------
import streamlit as st  # 웹 앱 생성을 위한 스트림릿(Streamlit) 라이브러리입니다. (터미널 설치: pip install streamlit) 🌊

# 아래 모듈들은 사용자가 직접 만든 파일이므로 pip 설치가 필요 없습니다. (같은 폴더에 있어야 함)
from prompt_template import * # 프롬프트 템플릿(Prompt Template) 모듈을 가져옵니다. 📝
from moderation_check import moderation_check  # 유해성 검사(Moderation Check) 모듈을 가져옵니다. 🛡️
from ask_llm import create_script  # LLM 호출(Ask LLM) 모듈을 가져옵니다. 🤖
from tts import text_to_speech  # 텍스트 음성 변환(Text to Speech) 모듈을 가져옵니다. 🗣️

def main_adcopy():  # 광고 카피 생성 메인 함수(Function)를 정의합니다. 🎬

    with st.sidebar:  # 화면 왼쪽 사이드바(Sidebar) 영역을 설정합니다. 📑
        st.title("광고 카피 메이커!")  # 사이드바 상단에 제목(Title)을 표시합니다. 🏷️
    
    # 대화 이력(History) 초기화: 세션 스테이트(Session State)를 사용합니다.
    if 'messages' not in st.session_state:  # 만약 세션에 'messages'라는 키가 없다면... ❓
        st.session_state['messages'] = []  # 빈 리스트(List)를 생성하여 초기화합니다. 🆕
        
    # 사용자 입력 화면 구성
    with st.container():  # 입력 요소들을 깔끔하게 묶어줄 컨테이너(Container)를 만듭니다. 📦
        topic = st.text_input("제품/서비스명 입력", placeholder="예: 생성형 AI")  # 주제(Topic) 입력창입니다. ⌨️
        message = st.text_input("핵심 문구", placeholder="예: 세계 최초")  # 핵심 메시지(Message) 입력창입니다. ✍️
        target = st.text_input("타겟 소비자", placeholder="예: 2030 직장인, 주부")  # 타겟(Target) 입력창입니다. 🎯
      
    if st.button("✨ 광고 카피 생성"):  # '광고 카피 생성' 버튼(Button)을 누르면 아래 로직을 실행합니다. 🖱️
        if not topic:  # 만약 주제(Topic)가 입력되지 않았다면... 🚫
            st.warning("제품/서비스명을 입력해주세요!")  # 경고(Warning) 메시지를 띄웁니다. ⚠️
        else:
            # 🛡️ [안전 장치] 콘텐츠 모더레이션 체크 (Try-Except 구문 사용)
            try:
                moderation_check(topic)  # 입력된 주제가 유해한지 검사(Check)합니다. 👮‍♂️
            except ValueError as e:  # 만약 유해하다고 판단되어 에러(ValueError)가 발생하면... 🚨
                st.error(str(e))  # 화면에 빨간색 에러 메시지를 출력합니다. 💥
                st.stop()         # 이후 코드를 실행하지 않고 중단(Stop)합니다. 🛑

            # ⏳ [로딩 처리] AI가 작업하는 동안 스피너(Spinner)를 보여줍니다.
            with st.spinner("전문 카피 라이터가 전략을 짜는 중입니다..."):
                # 1. 프롬프트(Prompt) 생성: 입력된 정보를 바탕으로 질문지를 만듭니다. 📜
                prompt = adcopy_prompt(topic, message, target)
                
                # 2. 스크립트(Script) 생성: LLM에게 질문지를 보내고 답변을 받습니다. 🤖
                ai_reply = create_script(prompt)
                
                # 3. 음성 파일(Audio File) 생성: [BEST] 태그를 기준으로 변환 범위를 정합니다.
                if "[BEST]" in ai_reply:  # 만약 답변에 '[BEST]'라는 단어가 있다면... 🔍
                    # [BEST] 뒤에 있는 문장만 잘라내어(Split) 공백을 제거(Strip)합니다. ✂️
                    best_part = ai_reply.split("[BEST]")[-1].strip()
                    audio_file = text_to_speech(best_part)  # 그 부분만 음성으로 변환합니다. 🎵
                else:  # 태그가 없다면...
                    audio_file = text_to_speech(ai_reply)  # 전체 내용을 음성으로 변환합니다. 🔊
                
                # 4. 결과 저장: 텍스트와 오디오 파일을 세션 스테이트(Session State)에 추가(Append)합니다. 💾
                st.session_state["messages"].append(
                    {"role": "assistant", "content": ai_reply, "audio": audio_file}
                )
            
    # 📝 [출력] 누적된 대화 기록을 화면에 보여줍니다. (최신 내용이 위로 오도록 역순 출력)
    for msg in reversed(st.session_state["messages"]):  # 저장된 메시지를 거꾸로(Reversed) 가져옵니다. 🔄
        with st.chat_message(msg["role"]):  # 메시지 역할(Role)에 맞는 UI를 생성합니다. 💬
            st.markdown(msg["content"])  # 텍스트 내용을 마크다운(Markdown) 형식으로 출력합니다. 📄
            if "audio" in msg:  # 만약 오디오 데이터가 포함되어 있다면... 🎧
                st.audio(msg["audio"], format="audio/mp3")  # 오디오 플레이어를 표시합니다. ▶️
            st.divider()  # 메시지 사이에 구분선(Divider)을 그립니다. ➖

if __name__ == "__main__":  # 이 파일이 직접 실행될 때만 main_adcopy 함수를 호출합니다. 🚀
    main_adcopy()