# 📦 [필수 라이브러리 설치]
# pip install openai python-dotenv sounddevice scipy numpy playsound fpdf2

import json  # 📄 데이터 처리
import random  # 🎲 랜덤 뽑기
from openai import OpenAI  # 🤖 AI 모델 연결
from dotenv import load_dotenv  # 🔐 API 키 로드
import os  # 💻 시스템 제어
import sounddevice as sd  # 🎤 녹음
import scipy.io.wavfile as wav  # 🎼 WAV 파일 저장
import numpy as np  # 🧮 수치 계산
import time  # ⏱️ 시간 제어
from datetime import datetime  # 📅 [NEW] 날짜와 시간을 기록하기 위해 추가
from playsound import playsound  # 🔊 소리 재생
from fpdf import FPDF  # 📑 PDF 생성

# ------------------------------------------------------------
# 0. 설정 및 초기화
# ------------------------------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 💾 [NEW] 대화 내용을 저장할 파일 이름
LOG_FILE = "conversation_log.txt"

# ------------------------------------------------------------
# 1. [NEW] 대화 저장 함수 (핵심 추가 기능)
# ------------------------------------------------------------
def save_conversation(user_text, ai_text):
    """
    🗣️ 사용자의 질문과 AI의 답변을 텍스트 파일에 이어붙여 저장(Append)합니다.
    """
    # 🕒 현재 날짜와 시간 구하기 (예: 2025-12-21 14:30:05)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 📝 저장할 형식 만들기
    log_content = f"[{now}]\n👤 사용자: {user_text}\n🤖 AI: {ai_text}\n" + "-"*50 + "\n"
    
    try:
        # 📂 파일을 '이어쓰기 모드(a)'로 엽니다. (utf-8 인코딩 필수)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_content)
        print(f"💾 [System] 대화 내용이 '{LOG_FILE}'에 저장되었습니다.")
    except Exception as e:
        print(f"❌ 로그 저장 실패: {e}")

# ------------------------------------------------------------
# 2. 도구(함수) 정의
# ------------------------------------------------------------
def get_current_weather(location, unit="celsius"):
    """ [시뮬레이션] 날씨 조회 """
    print(f"🕵️ [System] '{location}' 날씨 조회 중...")
    conditions = ["맑음 ☀️", "흐림 ☁️", "비 🌧️", "눈 ❄️"]
    return json.dumps({
        "location": location,
        "temperature": random.randint(-5, 30),
        "condition": random.choice(conditions)
    })

def get_latest_news(topic="general"):
    """ [시뮬레이션] 뉴스 검색 """
    print(f"🕵️ [System] '{topic}' 뉴스 검색 중...")
    fake_headlines = [
        f"속보: {topic} 시장의 놀라운 변화",
        f"{topic} 기술, 미래를 어떻게 바꿀까?",
        f"전 세계가 주목하는 {topic} 트렌드",
        f"전문가들, '{topic}'에 대한 긍정적 전망"
    ]
    return json.dumps({
        "topic": topic,
        "headlines": random.sample(fake_headlines, 3)
    })

def create_pdf_report(title, content):
    """ [PDF 생성] 보고서 만들기 """
    print(f"🖨️ [System] PDF 생성 중... (제목: {title})")
    filename = f"Report_{int(time.time())}.pdf"
    
    try:
        pdf = FPDF()
        pdf.add_page()
        # 윈도우 폰트 경로 (맥은 변경 필요)
        font_path = "C:/Windows/Fonts/malgun.ttf"
        
        if os.path.exists(font_path):
            pdf.add_font("Malgun", fname=font_path)
            pdf.set_font("Malgun", size=12)
        else:
            pdf.set_font("Helvetica", size=12)

        # 제목
        pdf.set_font_size(16)
        pdf.cell(0, 10, text=f"Report: {title}", new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(10)
        
        # 본문
        pdf.set_font_size(11)
        pdf.multi_cell(0, 8, text=content)
        
        pdf.output(filename)
        print(f"✅ PDF 저장 완료: {filename}")
        return json.dumps({"status": "success", "filename": filename})

    except Exception as e:
        print(f"❌ PDF 생성 실패: {e}")
        return json.dumps({"status": "error", "error": str(e)})

# ------------------------------------------------------------
# 3. 도구 스키마
# ------------------------------------------------------------
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "지역 날씨 조회",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_latest_news",
            "description": "뉴스 키워드 검색",
            "parameters": {
                "type": "object",
                "properties": {"topic": {"type": "string"}},
                "required": ["topic"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_pdf_report",
            "description": "정보를 PDF 파일로 저장",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["title", "content"]
            }
        }
    }
]

# ------------------------------------------------------------
# 4. 스마트 녹음 (VAD)
# ------------------------------------------------------------
def record_voice_smart(filename="input.wav", fs=16000, silence_threshold=150, silence_duration=1.2):
    """ 🎤 말할 때만 녹음하는 똑똑한 귀 """
    print("\n👂 듣고 있어요... (말씀하시면 녹음 시작)")
    
    buffer = []
    recording = True
    voice_detected = False
    silence_start_time = None
    
    with sd.InputStream(samplerate=fs, channels=1, dtype="int16") as stream:
        while recording:
            frame, _ = stream.read(int(0.1 * fs))
            volume = np.sqrt(np.mean(frame.astype(np.float64)**2))
            
            if volume > silence_threshold:
                if not voice_detected:
                    print("🗣️ 감지됨! 녹음 중...")
                    voice_detected = True
                silence_start_time = None
                buffer.append(frame)
                
            else:
                if voice_detected:
                    if silence_start_time is None: silence_start_time = time.time()
                    buffer.append(frame)
                    
                    if time.time() - silence_start_time > silence_duration:
                        print("✅ 녹음 종료.")
                        recording = False

    if buffer:
        wav.write(filename, fs, np.concatenate(buffer, axis=0))
        return filename
    return None

def speech_to_text(file_path):
    """ 📝 음성 -> 텍스트 변환 """
    if not os.path.exists(file_path): return ""
    try:
        with open(file_path, "rb") as f:
            return client.audio.transcriptions.create(model="whisper-1", file=f, language="ko").text
    except: return ""

# ------------------------------------------------------------
# 5. GPT 뇌 (생각 + 도구 실행)
# ------------------------------------------------------------
def ask_gpt(question):
    messages = [
        {"role": "system", "content": "당신은 AI 비서입니다. PDF 저장을 요청받으면 검색 후 요약하여 문서를 만드세요."},
        {"role": "user", "content": question}
    ]

    try:
        # 1차 생각
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools_schema,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # 도구 사용이 필요하면
        if tool_calls:
            print(f"🤖 GPT: {len(tool_calls)}가지 작업을 수행합니다...")
            messages.append(response_message)

            for tool_call in tool_calls:
                fname = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                result = ""
                
                if fname == "get_current_weather":
                    result = get_current_weather(args.get("location"))
                elif fname == "get_latest_news":
                    result = get_latest_news(args.get("topic"))
                elif fname == "create_pdf_report":
                    result = create_pdf_report(args.get("title"), args.get("content"))

                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": fname,
                    "content": result
                })

            # 최종 답변 생성
            second_response = client.chat.completions.create(
                model="gpt-4o-mini", messages=messages
            )
            return second_response.choices[0].message.content
        
        else:
            return response_message.content

    except Exception as e:
        print(f"❌ GPT 오류: {e}")
        return "오류가 발생했습니다."

# ------------------------------------------------------------
# 6. 메인 실행 (저장 기능 포함)
# ------------------------------------------------------------
def text_to_speech(text):
    """ 🔊 텍스트 -> 음성 변환 """
    try:
        speech = client.audio.speech.create(model="tts-1", voice="nova", input=text)
        filename = f"reply_{int(time.time())}.mp3"
        with open(filename, "wb") as f: f.write(speech.read())
        return filename
    except: return None

def ai_voice_assistant():
    print("\n🚀 [AI 비서] 가동 시작 (대화 내용 자동 저장 중...)\n")
    
    while True:
        try:
            print("\n" + "="*40)
            # 1. 듣기
            audio_file = record_voice_smart()
            if not audio_file: continue

            # 2. 적기
            user_text = speech_to_text(audio_file)
            print(f"📝 사용자: {user_text}")

            if "종료" in user_text:
                print("👋 비서를 종료합니다.")
                # 종료 전에도 로그 저장
                save_conversation(user_text, "비서 종료")
                break

            # 3. 생각하기 (말이 있을 때만)
            if user_text.strip():
                ai_answer = ask_gpt(user_text)
                print(f"🤖 AI: {ai_answer}")

                # 🌟 [핵심] 대화 내용 파일로 저장
                save_conversation(user_text, ai_answer)

                # 4. 말하기
                sound_file = text_to_speech(ai_answer)
                if sound_file:
                    playsound(sound_file)
                    time.sleep(0.5)
                    os.remove(sound_file) # 임시 파일 삭제

        except KeyboardInterrupt:
            print("\n강제 종료")
            break
        except Exception as e:
            print(f"⚠️ 오류: {e}")

if __name__ == "__main__":
    ai_voice_assistant()