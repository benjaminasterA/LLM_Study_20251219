# 📦 [필수 라이브러리 설치 명령어]
# 터미널에 아래 명령어를 입력해서 필요한 도구들을 설치해주세요.
# pip install openai python-dotenv sounddevice scipy numpy playsound fpdf2

import json  # 📄 데이터를 주고받을 때 표준 형식인 JSON을 처리하는 도구입니다.
import random  # 🎲 날씨나 뉴스 예시를 랜덤으로 뽑기 위한 도구입니다.
from openai import OpenAI  # 🤖 지능형 AI(GPT)와 대화하기 위한 OpenAI 전용 도구입니다.
from dotenv import load_dotenv  # 🔐 비밀번호(.env 파일)를 안전하게 불러오는 도구입니다.
import os  # 💻 파일 경로를 찾거나 운영체제 기능을 쓰기 위한 도구입니다.
import sounddevice as sd  # 🎤 마이크로 소리를 듣고 녹음하는 도구입니다.
import scipy.io.wavfile as wav  # 🎼 녹음된 소리를 파일(.wav)로 저장하는 도구입니다.
import numpy as np  # 🧮 소리 파형(숫자)을 계산하고 분석하는 수학 도구입니다.
import time  # ⏱️ 시간을 재거나 잠시 기다리게 하는 도구입니다.
from playsound import playsound  # 🔊 MP3 파일을 스피커로 재생해주는 도구입니다.
from fpdf import FPDF  # 📑 예쁜 PDF 보고서를 만들기 위한 도구입니다.

# ------------------------------------------------------------
# 0. API 초기화 (준비 단계)
# ------------------------------------------------------------
load_dotenv()  # 📂 프로젝트 폴더의 .env 파일을 찾아 내용을 읽어옵니다.
# 🔑 환경변수에서 API 키를 꺼내와서 OpenAI AI와 연결할 준비를 합니다.
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------------------------------------
# 1. 도구(함수) 정의 - AI가 사용할 수 있는 능력들
# ------------------------------------------------------------

def get_current_weather(location, unit="celsius"):
    """ [시뮬레이션] 특정 지역의 날씨를 알려주는 척하는 함수입니다. """
    print(f"🕵️ [System] '{location}'의 날씨를 조회하고 있습니다...")  # 🔍 로그 출력
    conditions = ["맑음 ☀️", "흐림 ☁️", "비 🌧️", "눈 ❄️"]  # 🌦️ 날씨 예시
    return json.dumps({  # 📦 결과를 JSON 문자열로 포장해서 반환합니다.
        "location": location,
        "temperature": random.randint(-5, 30),  # 🌡️ -5~30도 사이 랜덤 온도
        "condition": random.choice(conditions)  # 🎲 날씨 중 하나 랜덤 선택
    })

def get_latest_news(topic="general"):
    """ [시뮬레이션] 뉴스를 검색하는 척하는 함수입니다. """
    print(f"🕵️ [System] '{topic}' 관련 뉴스를 검색하고 있습니다...")  # 🔍 로그 출력
    fake_headlines = [  # 📰 가짜 뉴스 제목들 (실제 API가 있다면 여기서 교체)
        f"속보: {topic} 시장, 예상을 뛰어넘는 성장 기록",
        f"전문가들이 말하는 {topic}의 미래와 전망",
        f"전 세계가 주목하는 {topic}의 혁신적인 변화",
        f"{topic} 관련 새로운 기술 표준 발표 임박"
    ]
    return json.dumps({  # 📦 뉴스 결과를 반환합니다.
        "topic": topic,
        "headlines": random.sample(fake_headlines, 3)  # 🎰 3개만 뽑아서 줌
    })

def create_pdf_report(title, content):
    """ [PDF 생성] 검색한 내용을 깔끔한 PDF 파일로 만들어주는 함수입니다. """
    print(f"🖨️ [System] PDF 보고서를 생성 중입니다... (제목: {title})")  # 🚀 생성 시작 알림
    
    filename = f"Report_{int(time.time())}.pdf"  # 🕒 파일명에 시간을 넣어 겹치지 않게 함
    
    try:
        pdf = FPDF()  # 📄 빈 PDF 문서를 만듭니다.
        pdf.add_page()  # ➕ 종이 한 장을 추가합니다.
        
        # ⚠️ 한글 폰트 설정 (중요: 한글이 깨지지 않으려면 폰트가 필요함)
        # 윈도우 기본 폰트 경로입니다. 맥(Mac) 사용자는 경로 변경이 필요합니다.
        font_path = "C:/Windows/Fonts/malgun.ttf" 
        
        if os.path.exists(font_path):  # ✅ 폰트 파일이 진짜 있는지 확인
            pdf.add_font("Malgun", fname=font_path)  # 📥 폰트 등록
            pdf.set_font("Malgun", size=12)  # 🔤 폰트 선택 및 크기 설정
        else:
            print("⚠️ [경고] 한글 폰트가 없어서 기본 폰트를 씁니다. (한글 깨짐 주의)")
            pdf.set_font("Helvetica", size=12)  # 🔤 폰트가 없으면 영어 폰트 사용

        # 📌 제목 쓰기
        pdf.set_font_size(16)  # 제목이니까 글자를 키웁니다.
        # 가운데 정렬(C)로 제목을 적습니다.
        pdf.cell(0, 10, text=f"Report: {title}", new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(10) # ↩️ 한 줄 띄우기
        
        # 📝 본문 쓰기
        pdf.set_font_size(11)  # 본문 글자 크기로 줄입니다.
        pdf.multi_cell(0, 8, text=content)  # 📜 긴 글도 자동으로 줄바꿈해주는 함수 사용
        
        pdf.output(filename)  # 💾 최종 파일 저장
        print(f"✅ PDF 저장 완료: {filename}")  # 🎉 성공 메시지
        
        # 📨 AI에게 성공했다고 알려줍니다.
        return json.dumps({"status": "success", "filename": filename, "message": "파일 생성 완료"})

    except Exception as e:  # 💥 에러가 나면 프로그램이 꺼지지 않고 여기로 옴
        print(f"❌ PDF 생성 실패: {e}")
        return json.dumps({"status": "error", "error": str(e)})

# ------------------------------------------------------------
# 2. AI에게 도구 사용법 알려주기 (설명서)
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
            "description": "정보를 요약하여 PDF 파일로 저장. 검색 후 결과를 파일로 달라고 할 때 사용.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "보고서 제목"},
                    "content": {"type": "string", "description": "PDF 본문 내용"}
                },
                "required": ["title", "content"]
            }
        }
    }
]

# ------------------------------------------------------------
# 3. [핵심] 스마트 음성 녹음 (VAD 기능)
# ------------------------------------------------------------
def record_voice_smart(filename="input.wav", fs=16000, silence_threshold=150, silence_duration=1.2):
    """
    🎤 목소리가 들릴 때까지 대기하다가, 말이 시작되면 녹음하고,
       말이 끝나고 조용해지면 자동으로 녹음을 멈추는 함수입니다.
    """
    print("\n👂 듣고 있어요... 말씀해 보세요! (목소리를 감지하면 녹음 시작)")
    
    buffer = []  # 🥣 소리 데이터를 담을 바구니
    recording = True  # ⏺️ 녹음 루프 제어용 깃발
    voice_detected = False  # 🗣️ 말을 시작했는지 확인하는 깃발
    silence_start_time = None  # 🔇 침묵이 시작된 시간
    
    # 🎧 마이크를 켭니다 (InputStream)
    with sd.InputStream(samplerate=fs, channels=1, dtype="int16") as stream:
        while recording:
            # 🎵 0.1초 분량의 소리를 읽어옵니다.
            frame, _ = stream.read(int(0.1 * fs))
            
            # 🔊 소리의 크기(에너지)를 계산합니다.
            volume = np.sqrt(np.mean(frame.astype(np.float64)**2))
            
            # --- 로직: 소리 감지 및 녹음 제어 ---
            if volume > silence_threshold:  # 📢 설정한 기준보다 소리가 크다면? (말하는 중)
                if not voice_detected:
                    print("🗣️ 감지됨! 녹음 중...")  # 🚨 화면에 표시
                    voice_detected = True  # 말하기 시작했다고 표시
                
                silence_start_time = None  # 말하고 있으니 침묵 타이머 리셋
                buffer.append(frame)  # 소리를 바구니에 담음
                
            else:  # 🤫 소리가 기준보다 작다면? (조용함)
                if voice_detected:  # 🗣️ 이미 말을 시작한 상태라면?
                    if silence_start_time is None:
                        silence_start_time = time.time()  # ⏱️ 침묵 시작 시간 기록
                    
                    buffer.append(frame)  # 말이 끊기지 않게 조용한 부분도 일단 담음
                    
                    # ⏳ 조용한 시간이 설정값(1.2초)을 넘었는지 확인
                    if time.time() - silence_start_time > silence_duration:
                        print("✅ 말씀이 끝나서 녹음을 종료합니다.")
                        recording = False  # 녹음 종료!
                else:
                    # 💤 아직 말을 시작 안 했으면 아무것도 안 하고 대기 (버퍼에 안 담음)
                    pass

    # 💾 모은 소리 조각들을 합쳐서 파일로 저장합니다.
    if buffer:
        wav.write(filename, fs, np.concatenate(buffer, axis=0))
        return filename
    return None

def speech_to_text(file_path):
    """ 📝 녹음된 파일을 OpenAI Whisper에게 보내 글자로 바꿔오는 함수입니다. """
    if not os.path.exists(file_path): return ""  # 파일 없으면 패스
    try:
        with open(file_path, "rb") as f:
            # 🌪️ STT 모델(Whisper) 호출
            return client.audio.transcriptions.create(model="whisper-1", file=f, language="ko").text
    except: return ""

# ------------------------------------------------------------
# 4. GPT 두뇌 (생각하고 도구 쓰기)
# ------------------------------------------------------------
def ask_gpt(question):
    """ 🧠 사용자의 질문을 GPT에게 전달하고, 도구가 필요하면 쓰고, 최종 답을 주는 함수입니다. """
    
    # 📜 대화의 문맥(기록)을 만듭니다.
    messages = [
        {
            "role": "system",
            # 🎯 AI에게 정체성과 일하는 순서를 알려줍니다.
            "content": "당신은 유능한 AI 비서입니다. 사용자가 'PDF 저장'을 요청하면 [검색 -> 요약 -> PDF 생성] 순서로 도구를 사용하세요. 답변은 친절하고 자연스러운 한국어로 하세요."
        },
        {"role": "user", "content": question}
    ]

    try:
        # 1️⃣ GPT에게 1차 질문 (도구를 쓸지 말지 결정)
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 🚀 빠르고 똑똑한 모델
            messages=messages,
            tools=tools_schema,  # 🧰 사용 가능한 도구 목록 전달
            tool_choice="auto"   # 🤖 알아서 판단해라
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # 🛠️ GPT가 "도구를 써야겠어요!"라고 했다면?
        if tool_calls:
            print(f"🤖 GPT: {len(tool_calls)}가지 작업을 수행하겠습니다...")
            messages.append(response_message)  # 대화 흐름에 추가

            # 🏃‍♂️ GPT가 시킨 도구들을 하나씩 실행합니다.
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                tool_result = ""
                
                # 어떤 도구인지 확인하고 실행
                if function_name == "get_current_weather":
                    tool_result = get_current_weather(function_args.get("location"))
                elif function_name == "get_latest_news":
                    tool_result = get_latest_news(function_args.get("topic"))
                elif function_name == "create_pdf_report":
                    tool_result = create_pdf_report(
                        function_args.get("title"), 
                        function_args.get("content")
                    )

                # 📥 도구 실행 결과를 대화 목록에 추가해줍니다.
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": tool_result,
                })

            # 2️⃣ 도구 결과를 다 보고 최종 답변 생성
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            return second_response.choices[0].message.content
        
        else:
            # 💬 도구가 필요 없으면 그냥 답변 반환
            return response_message.content

    except Exception as e:
        print(f"❌ GPT 오류: {e}")
        return "죄송해요, 생각하는 중에 문제가 생겼어요."

# ------------------------------------------------------------
# 5. 말하기 및 메인 실행
# ------------------------------------------------------------
def text_to_speech(text):
    """ 🔊 AI의 텍스트 답변을 목소리 파일(MP3)로 바꿔주는 함수입니다. """
    try:
        # 🗣️ OpenAI TTS 사용 (목소리: nova)
        speech = client.audio.speech.create(model="tts-1", voice="nova", input=text)
        filename = f"reply_{int(time.time())}.mp3"
        with open(filename, "wb") as f:
            f.write(speech.read())
        return filename
    except: return None

def ai_voice_assistant():
    """ 🚀 프로그램의 시작점 (메인 루프) """
    print("\n🚀 [AI 음성 비서]가 실행되었습니다. (뉴스/날씨/PDF 기능 탑재)\n")
    
    while True:  # ♾️ 무한 반복 (계속 대화)
        try:
            print("\n" + "="*40)
            
            # 1. 🎤 듣기 (스마트 녹음)
            audio_file = record_voice_smart()
            if not audio_file: continue  # 녹음된 게 없으면 다시 대기

            # 2. 📝 받아적기 (STT)
            user_text = speech_to_text(audio_file)
            print(f"📝 사용자: {user_text}")

            # 👋 종료 명령어 확인
            if "종료" in user_text:
                print("👋 비서를 종료합니다.")
                bye_sound = text_to_speech("네, 이용해 주셔서 감사합니다. 안녕히 가세요.")
                playsound(bye_sound)
                break  # 루프 탈출

            # 3. 🧠 생각하고 답하기 (GPT + Tools)
            if user_text.strip():  # 말이 비어있지 않다면
                ai_answer = ask_gpt(user_text)
                print(f"🤖 AI: {ai_answer}")

                # 4. 🔊 말하기 (TTS)
                sound_file = text_to_speech(ai_answer)
                if sound_file:
                    playsound(sound_file)
                    time.sleep(0.5)
                    os.remove(sound_file) # 🧹 다 들은 파일 삭제 (깔끔하게)

        except KeyboardInterrupt:
            print("\n강제 종료합니다.")
            break
        except Exception as e:
            print(f"⚠️ 오류 발생: {e}")
            # 오류가 나도 꺼지지 않고 다시 듣기 모드로

if __name__ == "__main__":
    ai_voice_assistant()  # 🎬 큐! 액션!