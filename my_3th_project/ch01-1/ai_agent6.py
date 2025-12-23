import streamlit as st  # 웹 앱 생성을 위한 스트림릿(Streamlit) 라이브러리입니다. 🌊
import os  # 운영체제(OS) 기능 사용을 위한 모듈입니다. 💻
import re  # 정규표현식(Regular Expression) 처리를 위한 모듈입니다. 🧩
import time  # 시간 지연 및 측정을 위한 모듈입니다. ⏱️
import numpy as np  # 수치 계산을 위한 넘파이(NumPy) 라이브러리입니다. 🧮
import sounddevice as sd  # 오디오 재생을 위한 사운드디바이스(SoundDevice) 라이브러리입니다. 🔊
from scipy.io.wavfile import read  # WAV 파일 읽기를 위한 사이파이(SciPy) 모듈입니다. 🎼
from openai import OpenAI  # OpenAI API 사용을 위한 클라이언트입니다. 🤖
from dotenv import load_dotenv  # 환경변수 로드를 위한 라이브러리입니다. 🔐
from streamlit_mic_recorder import mic_recorder  # 스트림릿용 마이크 녹음 위젯입니다. 🎤
from streamlit_lottie import st_lottie  # 로티(Lottie) 애니메이션 표시를 위한 라이브러리입니다. 🎬
import requests  # HTTP 요청을 위한 리퀘스트(Requests) 라이브러리입니다. 🌐
from fpdf import FPDF  # PDF 생성을 위한 FPDF 라이브러리입니다. 📑


# ---------------------------------------------------------
# 0. 초기 설정 (Initial Setup)
# ---------------------------------------------------------
load_dotenv()  # .env 파일에서 환경변수를 로드합니다. 📂
st.set_page_config(page_title="AI Karaoke Assistant", page_icon="🎤")  # 웹 페이지 제목과 아이콘을 설정합니다. ⚙️

api_key = os.getenv("OPENAI_API_KEY")  # API 키를 가져옵니다. 🔑
if not api_key:  # 키가 없으면 경고하고 중단합니다. 🛑
    st.error("❌ OPENAI_API_KEY가 없습니다.")
    st.stop()

client = OpenAI(api_key=api_key)  # OpenAI 클라이언트를 초기화합니다. 🔗


# ---------------------------------------------------------
# 1. 종료 상태 확인 (Exit Check)
# ---------------------------------------------------------
# 세션 상태(Session State)에 'exit' 플래그가 있으면 프로그램을 종료합니다.
if st.session_state.get("exit"):
    st.warning("👋 프로그램이 종료되었습니다.")  # 작별 메시지 출력 👋
    st.stop()  # 실행 중단 ⏹️


# ---------------------------------------------------------
# 2. CSS: 노래방 반전 하이라이트 (Karaoke Style)
# ---------------------------------------------------------
# HTML/CSS를 사용하여 노래방 자막 스타일을 정의합니다. (검정 배경 + 노란 글씨) 🎨
st.markdown("""
<style>
.karaoke-line {
    font-size: 24px;
    font-weight: 500;
    line-height: 1.6;
}

.karaoke-highlighted { /* 현재 읽고 있는 부분 */
    background-color: black;
    color: yellow;
    padding: 2px 4px;
    border-radius: 3px;
}

.karaoke-normal { /* 아직 읽지 않은 부분 */
    color: #cccccc;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# 3. Lottie 로더 (Animation Loader)
# ---------------------------------------------------------
def load_lottieurl(url):  # Lottie JSON 파일을 URL에서 불러오는 함수입니다. 📥
    try:
        r = requests.get(url)  # URL로 요청을 보냅니다. 📨
        r.raise_for_status()  # 오류가 있으면 예외를 발생시킵니다. 🚨
        return r.json()  # JSON 데이터를 반환합니다. 📄
    except:
        return None  # 실패 시 None 반환 🚫

# 애니메이션 파일 로드 (파도 모양, 로딩 모양)
lottie_wave = load_lottieurl("https://assets9.lottiefiles.com/packages/lf20_tutvdkg0.json") 
lottie_loading = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_j1adxtyb.json")


# ---------------------------------------------------------
# 4. 핵심 기능 함수 (Core Functions)
# ---------------------------------------------------------
def STT(audio_bytes):  # 음성을 텍스트로 변환(STT)하는 함수입니다. 👂
    """Whisper STT"""
    with open("temp_input.wav", "wb") as f:  # 임시 파일로 저장합니다. 💾
        f.write(audio_bytes)

    with open("temp_input.wav", "rb") as f:  # 파일을 읽어서 API로 보냅니다. 📤
        tr = client.audio.transcriptions.create(
            model="whisper-1",  # Whisper 모델 사용 🤫
            file=f,
            language="ko"  # 한국어로 설정 🇰🇷
        )
    return tr.text  # 변환된 텍스트 반환 📝


def ask_gpt(messages, max_tokens=150):  # GPT에게 질문하고 답변을 받는 함수입니다. 🧠
    """GPT 답변"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",  # 모델 선택 🚀
        messages=messages,  # 대화 문맥 전달 📨
        max_tokens=max_tokens  # 최대 답변 길이 제한 📏
    )
    return res.choices[0].message.content  # 답변 내용 반환 💬


def tts_generate(sentence, voice="nova"):  # 텍스트를 음성(WAV)으로 변환하는 함수입니다. 🗣️
    """TTS 문장 1개 wav 생성"""
    res = client.audio.speech.create(
        model="tts-1",  # TTS 모델 사용 🔊
        voice=voice,  # 목소리 선택 🎤
        input=sentence,  # 변환할 문장 📄
        response_format="wav"  # WAV 포맷으로 요청 🎼
    )
    with open("tts.wav", "wb") as f:  # 파일로 저장합니다. 💾
        f.write(res.content)

    fs, data = read("tts.wav")  # 샘플링 레이트(fs)와 데이터(data)를 읽어옵니다. 📊
    return fs, data


# ---------------------------------------------------------
# 5. SRT 자동 생성 (Subtitle Generation)
# ---------------------------------------------------------
def format_srt_timestamp(seconds):  # 초 단위 시간을 SRT 타임스탬프 형식으로 변환합니다. ⏰
    ms = int(seconds * 1000)
    hrs = ms // 3600000
    ms %= 3600000
    mins = ms // 60000
    ms %= 60000
    secs = ms // 1000
    ms %= 1000
    return f"{hrs:02}:{mins:02}:{secs:02},{ms:03}"  # 00:00:00,000 형식 반환 ⏳


def save_srt(sentences, durations, filename="result.srt"):  # 자막 파일(SRT)을 저장하는 함수입니다. 🎬
    with open(filename, "w", encoding="utf-8") as f:
        current = 0.0  # 현재 시간 초기화 0️⃣
        for i, (sentence, dur) in enumerate(zip(sentences, durations), 1):
            start = format_srt_timestamp(current)  # 시작 시간 계산 🏁
            end = format_srt_timestamp(current + dur)  # 종료 시간 계산 🛑

            f.write(f"{i}\n{start} --> {end}\n{sentence}\n\n")  # SRT 형식에 맞춰 쓰기 ✍️
            current += dur  # 다음 문장을 위해 시간 누적 ➕


# ---------------------------------------------------------
# 6. Karaoke 모드 (Karaoke Mode)
# ---------------------------------------------------------
def karaoke_mode(text, text_placeholder, visualizer_placeholder, voice):  # 자막과 음성을 싱크에 맞춰 재생하는 핵심 함수입니다. 🎤

    # 문장 분리 (Split Sentences)
    sentences = re.split(r'(?<=[.?!])\s+', text)  # 마침표, 물음표, 느낌표 뒤에서 자릅니다. ✂️
    sentences = [s.strip() for s in sentences if s.strip()]  # 공백 제거 및 빈 문장 제외 🧹

    with visualizer_placeholder:
        st.caption("🎶 음성 생성 중…")
        if lottie_loading:
            st_lottie(lottie_loading, height=100)  # 로딩 애니메이션 표시 ⏳

    audio_segments = []  # 오디오 데이터를 담을 리스트 🎵
    durations = []  # 재생 시간을 담을 리스트 ⏱️

    # ▶ 문장별 TTS 생성 (Batch Processing)
    for s in sentences:
        fs, data = tts_generate(s, voice)  # 음성 생성 요청 🗣️
        duration = len(data) / fs  # 데이터 길이 / 샘플링 레이트 = 재생 시간(초) 🧮

        audio_segments.append((s, fs, data))  # 결과 저장 📦
        durations.append(duration)

    visualizer_placeholder.empty()  # 로딩 애니메이션 지우기 🧹

    with visualizer_placeholder:
        st.caption("🔊 AI 음성 재생 중…")
        if lottie_wave:
            st_lottie(lottie_wave, height=70, loop=True)  # 파형 애니메이션 표시 🌊

    full_log = ""  # 전체 누적 텍스트

    # ▶ 문장 단위 Karaoke 재생 (Playback Loop)
    for (sentence, fs, data), duration in zip(audio_segments, durations):

        total_len = len(sentence)  # 문장 글자 수 📏
        sd.play(data, fs)  # 오디오 재생 시작 ▶️

        start = time.time()  # 시작 시간 기록 🕒
        while time.time() - start < duration:  # 오디오가 끝날 때까지 반복 🔄

            progress = (time.time() - start) / duration  # 진행률 계산 (0.0 ~ 1.0) 📊
            idx = min(total_len, int(total_len * progress))  # 현재 하이라이트할 글자 위치 계산 📍

            highlighted = sentence[:idx]  # 이미 읽은 부분 (노란색) 🟡
            remaining = sentence[idx:]  # 앞으로 읽을 부분 (회색) ⚪

            # HTML로 스타일 적용
            html = (
                f"{full_log} "
                f"<span class='karaoke-highlighted'>{highlighted}</span>"
                f"<span class='karaoke-normal'>{remaining}</span>"
            )

            text_placeholder.markdown(
                f"<div class='karaoke-line'>{html}</div>", unsafe_allow_html=True
            )

            time.sleep(0.05)  # 화면 갱신 주기 (0.05초) 💤

        sd.wait()  # 오디오 재생이 완전히 끝날 때까지 대기 ⏹️

        # 문장 완료 → 평문으로 기록하고 다음 문장으로 넘어감
        full_log += " " + sentence
        text_placeholder.markdown(full_log)

    visualizer_placeholder.empty()  # 애니메이션 종료 🛑

    # ▶ SRT 생성 (Create SRT File)
    save_srt(sentences, durations)


# ---------------------------------------------------------
# 7. PDF 저장 (Save as PDF)
# ---------------------------------------------------------
def save_pdf(text, filename="result.pdf"):
    pdf = FPDF()
    pdf.add_page()
    try:
        # 한글 폰트 설정 (Windows 기준) 🔤
        pdf.add_font("malgun", "", r"C:\\Windows\\Fonts\\malgun.ttf", uni=True)
        pdf.set_font("malgun", size=12)
    except:
        pdf.set_font("Arial", size=12)  # 실패 시 기본 영문 폰트 사용 🅰️

    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)  # 줄바꿈 처리하여 쓰기 📝
    pdf.output(filename)


# ---------------------------------------------------------
# 8. 전체 MP3 저장 (Save Full MP3)
# ---------------------------------------------------------
def save_mp3(text, filename="result.mp3", voice="nova"):
    try:
        res = client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text,
            response_format="mp3"
        )
        with open(filename, "wb") as f:
            f.write(res.content)
        return True
    except Exception as e:
        st.error(f"MP3 저장 오류: {e}")
        return False


# ---------------------------------------------------------
# 9. 세션 데이터 (Session State)
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # 대화 기록 초기화 🆕

if "full_text" not in st.session_state:
    st.session_state.full_text = ""  # 전체 텍스트 기록 초기화 📝


# ---------------------------------------------------------
# 10. UI 제목 (Title)
# ---------------------------------------------------------
st.title("🎤 AI Karaoke Assistant (Soomin)")  # 메인 타이틀 표시 🏷️


# ---------------------------------------------------------
# 11. Sidebar (설정 메뉴)
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙ 설정")

    # TTS 음성 선택 드롭다운
    tts_voice = st.selectbox(
        "TTS 음성 선택",
        ["nova", "shimmer", "echo", "onyx", "fable", "alloy", "ash", "sage", "coral"]
    )

    # GPT 응답 길이 조절 슬라이더
    max_tokens = st.slider("GPT 응답 길이", 50, 300, 150)

    st.markdown("---")
    st.subheader("💾 Export (내보내기)")

    # TXT 저장 버튼
    if st.button("📝 TXT 저장"):
        with open("result.txt", "w", encoding="utf-8") as f:
            f.write(st.session_state.full_text)
        st.success("TXT 저장 완료!")

    # PDF 저장 버튼
    if st.button("📄 PDF 저장"):
        save_pdf(st.session_state.full_text)
        st.success("PDF 저장 완료!")

    # MP3 저장 및 다운로드 버튼
    if st.button("🎵 MP3 저장"):
        if save_mp3(st.session_state.full_text, "result.mp3", tts_voice):
            with open("result.mp3", "rb") as f:
                st.download_button("⬇ MP3 다운로드", f, "result.mp3")

    # SRT 저장 및 다운로드 버튼
    if st.button("🎼 SRT 저장"):
        if os.path.exists("result.srt"):
            with open("result.srt", "rb") as f:
                st.download_button("⬇ SRT 다운로드", f, "result.srt")
        else:
            st.warning("먼저 AI 음성을 생성해 SRT 파일을 만드세요.")

    st.markdown("---")

    # 🔄 전체 초기화 버튼
    if st.button("🔄 전체 초기화"):
        st.session_state.messages = []
        st.session_state.full_text = ""
        st.rerun()  # 앱 재실행 🔄

    # ⛔ 종료 버튼
    if st.button("⛔ 종료"):
        st.session_state["exit"] = True
        st.rerun()


# ---------------------------------------------------------
# 12. 기존 대화 표시 (Display Chat History)
# ---------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):  # 역할(User/Assistant)에 따라 아이콘 표시 👤🤖
        st.markdown(msg["content"])


# ---------------------------------------------------------
# 13. 입력 UI (Input Interface)
# ---------------------------------------------------------
st.divider()  # 구분선 📏
col1, col2 = st.columns([1, 5])  # 컬럼 비율 1:5 설정

with col1:
    # 마이크 녹음 버튼 위젯
    audio = mic_recorder(start_prompt="● 녹음", stop_prompt="■ 정지", key="recorder")

with col2:
    # 텍스트 입력창
    text_input = st.text_input("✍ 텍스트 입력")


# ---------------------------------------------------------
# 14. Main 처리 로직 (Main Logic)
# ---------------------------------------------------------
if audio or text_input:  # 녹음이 되거나 텍스트가 입력되면 실행 ▶️

    if audio:  # 오디오 입력이 있는 경우 🎤
        st.info("👂 음성 인식 중…")
        user_text = STT(audio["bytes"])  # STT 변환 실행
    else:  # 텍스트 입력인 경우 ⌨️
        user_text = text_input

    if user_text:  # 유효한 입력이 있다면 ✅

        st.session_state.full_text += f"\nUser: {user_text}"  # 전체 기록에 추가 ➕

        with st.chat_message("user"):  # 사용자 메시지 표시
            st.markdown(user_text)

        st.session_state.messages.append({"role": "user", "content": user_text})  # 세션에 저장 💾

        st.info("🤖 GPT 답변 생성 중…")

        # GPT에게 답변 요청 (이전 대화 내역 포함)
        ai_text = ask_gpt(
            [{"role": "system", "content": "명확하고 간결하게 답변하라."}] +
            st.session_state.messages,
            max_tokens=max_tokens
        )

        st.session_state.full_text += f"\nAI: {ai_text}"  # 전체 기록에 AI 답변 추가 ➕
        st.session_state.messages.append({"role": "assistant", "content": ai_text})  # 세션에 저장 💾

        with st.chat_message("assistant"):  # AI 메시지 영역 🤖

            visual_placeholder = st.empty()  # 애니메이션을 보여줄 빈 공간 확보 📺
            text_placeholder = st.empty()  # 자막을 보여줄 빈 공간 확보 📺

            # 노래방 모드 실행 (음성 재생 + 자막 하이라이트) 🎤
            karaoke_mode(ai_text, text_placeholder, visual_placeholder, voice=tts_voice)
