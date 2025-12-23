# ---------------------------------------------------------
# [Import 순서 정리]
# 1. 서드파티 라이브러리 (pip install 필요)
# 2. 사용자 정의 모듈 (직접 만든 파일)
# ---------------------------------------------------------

# ① 서드파티 라이브러리 (Third-party Libraries) - 설치 필요
import streamlit as st  # 웹 앱 생성을 위한 스트림릿(Streamlit) 라이브러리입니다. (터미널 설치: pip install streamlit) 🌊

# ② 사용자 정의 모듈 (User-defined Modules) - 같은 폴더에 파일이 있어야 함
from prompt_template import * # 프롬프트(Prompt) 템플릿 함수들을 가져옵니다. 📝
from moderation_check import moderation_check  # 입력 내용의 유해성을 검사(Moderation Check)하는 모듈입니다. 🛡️
from ask_llm import create_script  # LLM(거대 언어 모델)에게 질문하고 답을 받는 함수입니다. 🤖
from tts import text_to_speech  # 텍스트를 음성으로 변환(TTS)하는 함수입니다. 🗣️


def main_ytb():  # 유튜브 스크립트 생성 메인 함수를 정의합니다. 📹
    with st.sidebar:  # 화면 왼쪽의 사이드바(Sidebar) 영역을 설정합니다. 📑
        st.title("유튜브 영상 스크립트 메이커!")  # 사이드바 제목(Title)을 표시합니다. 🏷️
        
    # 대화 이력 초기화
    # 세션 스테이트(Session State)를 사용하여 새로고침해도 데이터가 유지되도록 합니다. 💾
    if 'messages' not in st.session_state:
        st.session_state['messages'] = []  # 메시지를 담을 빈 리스트(List)를 초기화합니다. 🆕
        
    # 사용자 입력 화면
    with st.container():  # 입력 요소들을 담을 컨테이너(Container)를 만듭니다. 📦
        topic = st.text_input("유튜브 주제 입력", placeholder="예: 생성형 AI")  # 주제(Topic) 입력창입니다. ⌨️
        
        # 화면을 가로로 3등분하여 레이아웃을 잡습니다. (Column 1, 2, 3) 📊
        col1, col2, col3 = st.columns(3)
        
        with col1:  # 첫 번째 칸
            target = st.text_input("타겟 시청자", placeholder="예: 2030 직장인, 주부")  # 타겟(Target) 입력창입니다. 🎯
        with col2:  # 두 번째 칸
            # 영상 길이(Length)를 선택하는 드롭다운 메뉴입니다. ⏳
            length = st.selectbox("영상 길이", ["1분 (쇼츠)", "3분", "5분", "10분 이상"])
        with col3:  # 세 번째 칸
            # 영상의 분위기(Tone)를 선택하는 드롭다운 메뉴입니다. 🎨
            tone = st.selectbox("영상 톤", ["친근한", "전문적인", "유머러스한", "감성적인", "상업적인"])
        
    if st.button("✨ 유튜브 스크립트 생성"):  # '스크립트 생성' 버튼(Button)을 누르면 실행됩니다. 🖱️
        if not topic:  # 주제가 입력되지 않았을 경우... 🚫
            st.warning("주제를 입력해주세요!")  # 경고(Warning) 메시지를 띄웁니다. ⚠️
        else:
            # 콘텐츠 모더레이션 체크
            # 입력된 주제가 안전한지 검사(Moderation Check)합니다. 👮‍♂️
            # moderation_check(topic)
            

            with st.spinner("유튜브 영상 최적화 대본을 작성 중입니다..."):  # 작업 완료 시까지 로딩 스피너(Spinner)를 보여줍니다. 🔄
                # 프롬프트 생성
                # 입력된 정보를 바탕으로 AI에게 보낼 질문지(Prompt)를 만듭니다. 📜
                prompt = youtube_prompt(topic, length, tone, target)
                
                # 유튜브 스크립트 생성
                # LLM 함수를 호출하여 AI의 답변(Reply)을 받습니다. 🤖
                ai_reply = create_script(prompt)
            
                # 음성 파일 생성 (베스트 부분만 음성 변환, 없으면 전체 변환)
                # 답변에 '[BEST]' 태그가 있는지 확인합니다. 🔍
                if "[BEST]" in ai_reply:
                    # [BEST] 뒤에 있는 텍스트만 잘라내어(Split) 공백을 제거(Strip)합니다. ✂️
                    best_part = ai_reply.split("[BEST]")[-1].strip()
                    audio_file = text_to_speech(best_part)  # 그 부분만 TTS로 변환합니다. 🎵
                else:
                    audio_file = text_to_speech(ai_reply)  # 태그가 없으면 전체를 변환합니다. 🔊
                                
                # 모델 응답 이력에 텍스트와 음성을 한쌍으로 저장
                # 결과 텍스트와 오디오 파일을 세션에 추가(Append)합니다. ➕
                st.session_state["messages"].append(
                    {"role": "assistant", "content": ai_reply, "audio": audio_file}
                )
            
    # 텍스트와 음성 포함한 누적 결과 출력 (최근 결과를 위쪽으로 출력)
    # 최신 메시지가 위에 오도록 리스트를 역순(Reversed)으로 반복합니다. 🔄
    for msg in reversed(st.session_state["messages"]):
        with st.chat_message(msg["role"]):  # 메시지 역할(Role)에 맞는 UI를 표시합니다. 💬
            st.markdown(msg["content"])  # 텍스트 내용을 보여줍니다. 📝
            if "audio" in msg:  # 오디오 파일이 있으면... 🎧
                st.audio(msg["audio"], format="audio/mp3")  # 오디오 플레이어를 표시합니다. ▶️
            st.divider()  # 구분선(Divider)을 그립니다. ➖


if __name__ == "__main__":  # 이 파일이 직접 실행될 때만 메인 함수를 호출합니다. 🚀
    main_ytb()