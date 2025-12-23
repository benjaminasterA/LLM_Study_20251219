# pip install openai python-dotenv sounddevice scipy numpy playsound fpdf

import json  # JSON(제이슨) 데이터를 처리하기 위한 내장 모듈입니다. 📄
import random  # 난수(Random Number) 생성을 위한 내장 모듈입니다. 🎲
from openai import OpenAI  # OpenAI(오픈에이아이) API 사용을 위한 클라이언트입니다. 🤖
from dotenv import load_dotenv  # 환경변수 파일(.env)을 로드하기 위한 라이브러리입니다. 🔐
import os  # 운영체제(Operating System) 기능 사용을 위한 모듈입니다. 💻
import sounddevice as sd  # 오디오 녹음 및 재생을 위한 사운드디바이스(SoundDevice) 라이브러리입니다. 🎤
import scipy.io.wavfile as wav  # WAV(웨이브) 파일 저장을 위한 사이파이(SciPy) 모듈입니다. 🎼
import numpy as np  # 수치 계산 및 배열 처리를 위한 넘파이(NumPy) 라이브러리입니다. 🧮
import time  # 시간(Time) 지연 및 측정을 위한 모듈입니다. ⏱️
from playsound import playsound  # MP3 파일 재생을 위한 플레이사운드(Playsound) 라이브러리입니다. 🔊
from fpdf import FPDF  # PDF(피디에프) 문서 생성을 위한 FPDF 라이브러리입니다. 📑

# ------------------------------------------------------------
# API 초기화
# ------------------------------------------------------------
load_dotenv()  # .env 파일에 저장된 API 키를 환경변수로 불러옵니다. 📂
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 불러온 키로 OpenAI 클라이언트(Client)를 연결합니다. 🔗

# ------------------------------------------------------------
# 1. 도구(함수) 정의
# ------------------------------------------------------------

def get_current_weather(location, unit="celsius"):  # 날씨 정보를 가져오는 함수(Function)를 정의합니다. ☀️
    """[시뮬레이션] 날씨 조회"""
    print(f"🕵️ [System] '{location}' 날씨 조회 중...")  # 시스템(System) 로그를 출력합니다. 🖨️
    conditions = ["맑음 ☀️", "흐림 ☁️", "비 🌧️", "눈 ❄️"]  # 날씨 상태(Conditions) 리스트를 만듭니다. 📋
    return json.dumps({  # 결과를 JSON 문자열(String)로 변환하여 반환합니다. 🔄
        "location": location,  # 지역(Location) 정보입니다. 📍
        "temperature": random.randint(-5, 30),  # -5도에서 30도 사이의 랜덤 온도(Temperature)입니다. 🌡️
        "condition": random.choice(conditions)  # 날씨 상태 중 하나를 무작위로 선택(Choice)합니다. 🎲
    })

def get_latest_news(topic="general"):  # 뉴스 정보를 가져오는 함수를 정의합니다. 📰
    """[시뮬레이션] 뉴스 검색"""
    print(f"🕵️ [System] '{topic}' 뉴스 검색 중...")  # 검색 중임을 알리는 로그를 출력합니다. 🔍
    fake_headlines = [  # 가짜 헤드라인(Headlines) 리스트를 만듭니다. (실제 연동 시 API 교체) 📝
        f"속보: {topic} 분야의 놀라운 성장세 기록",
        f"전 세계가 주목하는 {topic}의 미래 전망",
        f"{topic} 관련 새로운 기술 표준 발표 임박",
        f"전문가들, '{topic}' 시장에 대한 낙관적 분석 내놓아"
    ]
    return json.dumps({  # 뉴스 데이터를 JSON 형식으로 반환합니다. 📤
        "topic": topic,  # 검색 주제(Topic)입니다. 🏷️
        "headlines": random.sample(fake_headlines, 3)  # 헤드라인 중 3개를 무작위로 추출(Sample)합니다. 🎰
    })

def create_pdf_report(title, content):  # PDF 보고서를 생성하는 함수를 정의합니다. 📑
    """
    [NEW] 검색된 내용이나 요약본을 PDF 파일로 저장합니다.
    한글 깨짐 방지를 위해 시스템 폰트(맑은 고딕)를 사용합니다.
    """
    print(f"🖨️ [System] PDF 보고서 생성 중... (제목: {title})")  # PDF 생성 시작을 알립니다. 🚀
    
    filename = f"Report_{int(time.time())}.pdf"  # 현재 시간을 파일명(Filename)에 넣어 중복을 방지합니다. 🕒
    
    try:  # 예외 처리를 위해 트라이(Try) 블록을 시작합니다. 🛡️
        pdf = FPDF()  # PDF 객체(Object)를 생성합니다. 📄
        pdf.add_page()  # 새 페이지(Page)를 추가합니다. ➕
        
        # ⚠️ 한글 폰트 설정 (Windows '맑은 고딕' 기준)
        # Mac 사용자는 "/System/Library/Fonts/AppleGothic.ttf" 등으로 변경 필요
        font_path = "C:/Windows/Fonts/malgun.ttf"  # 윈도우(Windows)의 맑은 고딕 폰트 경로(Path)입니다. 🔤
        
        if os.path.exists(font_path):  # 폰트 파일이 실제로 존재하는지 확인(Exists)합니다. ✅
            pdf.add_font("Malgun", fname=font_path)  # PDF에 'Malgun'이라는 이름으로 폰트를 추가(Add Font)합니다. 📥
            pdf.set_font("Malgun", size=12)  # 추가한 폰트를 설정하고 크기(Size)를 12로 지정합니다. 📏
        else:  # 폰트가 없다면... (비상 상황) 🚨
            print("⚠️ 경고: 한글 폰트(malgun.ttf)를 찾을 수 없습니다. 기본 폰트를 사용합니다(한글 깨짐 가능).")
            pdf.set_font("Helvetica", size=12)  # 영문 기본 폰트인 헬베티카(Helvetica)를 사용합니다. 🔤

        # 제목 작성
        pdf.set_font_size(16)  # 제목용으로 폰트 크기를 16으로 키웁니다. ⬆️
        # 제목을 가운데(Center) 정렬하여 출력합니다. new_x/new_y는 다음 커서 위치입니다.
        pdf.cell(0, 10, text=f"Report: {title}", new_x="LMARGIN", new_y="NEXT", align='C') 
        pdf.ln(10)  # 10만큼 줄 바꿈(Line Break)을 합니다. ↩️
        
        # 본문 작성 (Multi_cell을 사용해야 줄바꿈이 자동 처리됨)
        pdf.set_font_size(11)  # 본문용으로 폰트 크기를 11로 줄입니다. ⬇️
        pdf.multi_cell(0, 8, text=content)  # 긴 텍스트를 자동으로 줄바꿈하며(Multi Cell) 출력합니다. 📝
        
        pdf.output(filename)  # 최종적으로 PDF 파일을 저장(Output)합니다. 💾
        print(f"✅ PDF 저장 완료: {filename}")  # 성공 메시지를 출력합니다. 🎉
        
        # 성공 결과를 JSON으로 반환합니다.
        return json.dumps({"status": "success", "filename": filename, "message": "PDF 파일이 성공적으로 생성되었습니다."})

    except Exception as e:  # 에러(Exception)가 발생하면 실행됩니다. 🚫
        print(f"❌ PDF 생성 실패: {e}")  # 실패 원인을 출력합니다. 💥
        return json.dumps({"status": "error", "error": str(e)})  # 에러 내용을 반환합니다. 🔙

# ------------------------------------------------------------
# 2. 도구 스키마 정의 (GPT에게 PDF 기능 알려주기)
# ------------------------------------------------------------
tools_schema = [  # AI가 사용할 도구들의 명세서(Schema) 리스트입니다. 📜
    {
        "type": "function",  # 도구의 타입은 함수(Function)입니다. 🔧
        "function": {
            "name": "get_current_weather",  # 함수 이름(Name)입니다. 🏷️
            "description": "지역 날씨 조회",  # 함수 설명(Description)입니다. 📖
            "parameters": {  # 필요한 매개변수(Parameters) 정의입니다. 🧱
                "type": "object",
                "properties": {"location": {"type": "string"}},  # 지역명은 문자열입니다. 🔤
                "required": ["location"]  # 지역명은 필수(Required)입니다. ✅
            }
        }
    },
    {
        "type": "function",  # 뉴스 검색 도구 정의입니다. 📰
        "function": {
            "name": "get_latest_news",
            "description": "뉴스 키워드 검색",
            "parameters": {
                "type": "object",
                "properties": {"topic": {"type": "string"}},  # 검색 주제는 문자열입니다. 🔤
                "required": ["topic"]  # 주제는 필수입니다. ✅
            }
        }
    },
    {   # 🎯 PDF 생성 도구 추가
        "type": "function",  # PDF 생성 도구 정의입니다. 📑
        "function": {
            "name": "create_pdf_report",  # 함수 이름입니다. 🏷️
            "description": "내용을 정리하여 PDF 파일로 저장합니다. 검색 후 결과를 저장할 때 사용하세요.",  # AI에게 언제 쓸지 알려줍니다. 💡
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "보고서 제목"},  # 보고서 제목입니다. 📌
                    "content": {"type": "string", "description": "PDF에 들어갈 본문 내용 (검색 결과 요약 등)"}  # 보고서 본문입니다. 📝
                },
                "required": ["title", "content"]  # 제목과 내용은 필수입니다. ✅
            }
        }
    }
]

# ------------------------------------------------------------
# 3. 음성 녹음 및 STT (기존 동일)
# ------------------------------------------------------------
def record_voice_auto(filename="input.wav", fs=16000, silence_threshold=300, min_silence_duration=1.5):  # 음성을 자동으로 감지해 녹음하는 함수입니다. 🎤
    print("\n🎤 말씀해주세요! (1.5초 침묵 시 자동 종료)\n")  # 녹음 시작 안내입니다. 🗣️
    buffer = []  # 오디오 데이터를 담을 버퍼(Buffer) 리스트입니다. 🥣
    silence_start = None  # 침묵 시작 시간을 기록할 변수입니다. 🔇
    recording = True  # 녹음 진행 상태 플래그(Flag)입니다. 🚩
    start_time = time.time()  # 녹음 시작 시간입니다. 🕒

    try:  # 녹음 도중 에러 처리를 위한 블록입니다. 🛡️
        with sd.InputStream(samplerate=fs, channels=1, dtype="int16") as stream:  # 마이크 입력 스트림(Stream)을 엽니다. 🔓
            while recording:  # 녹음 중인 동안 반복합니다. 🔄
                frame, _ = stream.read(int(0.1 * fs))  # 0.1초 분량의 오디오 프레임(Frame)을 읽습니다. 🎼
                buffer.append(frame)  # 읽은 데이터를 버퍼에 추가합니다. ➕
                volume = np.sqrt(np.mean(frame.astype(np.float64)**2))  # 소리의 크기(Volume)를 계산합니다(RMS 방식). 🔊

                if time.time() - start_time < 0.5: continue  # 처음 0.5초는 노이즈 무시를 위해 건너뜁니다. 💨

                if volume < silence_threshold:  # 소리가 임계값(Threshold)보다 작으면(침묵)... 🤫
                    if silence_start is None: silence_start = time.time()  # 침묵 시작 시간을 기록합니다. ⏱️
                    elif time.time() - silence_start > min_silence_duration:  # 침묵이 일정 시간 지속되면... 🛑
                        recording = False  # 녹음을 종료합니다. ⏹️
                else:  # 소리가 들리면... 📢
                    silence_start = None  # 침묵 타이머를 리셋합니다. 🔄

        wav.write(filename, fs, np.concatenate(buffer, axis=0))  # 버퍼의 데이터를 하나의 파일로 저장합니다. 💾
        return filename  # 저장된 파일명을 반환합니다. ↩️
    except Exception as e:  # 녹음 실패 시... ❌
        print(f"녹음 오류: {e}")
        return None

def speech_to_text(file_path):  # 녹음된 파일을 텍스트로 변환(STT)하는 함수입니다. 📝
    if not os.path.exists(file_path): return ""  # 파일이 없으면 빈 문자열을 반환합니다. 🚫
    try:
        with open(file_path, "rb") as f:  # 파일을 바이너리 읽기 모드(rb)로 엽니다. 📖
            # Whisper 모델을 사용하여 음성을 텍스트로 변환합니다. 🗣️ -> 🅰️
            return client.audio.transcriptions.create(model="whisper-1", file=f, language="ko").text
    except: return ""  # 변환 실패 시 빈 문자열 반환. 🤷‍♂️

# ------------------------------------------------------------
# 4. GPT 답변 생성 (도구 연쇄 호출 지원)
# ------------------------------------------------------------
def ask_gpt(question):  # 사용자의 질문을 GPT에게 전달하는 함수입니다. 🤖
    messages = [  # 대화 기록(Messages) 리스트를 초기화합니다. 📜
        {
            "role": "system",  # 시스템 역할을 설정합니다. ⚙️
            # 🎯 시스템 프롬프트 강화: 도구를 순서대로 사용하도록 유도합니다. 🧠
            "content": "당신은 정보 검색 및 문서 작성이 가능한 AI 비서입니다. 사용자가 'PDF로 저장해줘'라고 하면, 먼저 정보를 검색(news/weather)하고, 그 내용을 요약한 뒤 PDF 생성 도구를 사용하세요."
        },
        {"role": "user", "content": question}  # 사용자의 질문을 리스트에 추가합니다. 👤
    ]

    try:
        # 1차 호출: GPT가 도구 사용 여부를 판단(Decision)합니다. 🤔
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # 가성비 좋은 미니 모델을 사용합니다. 🚀
            messages=messages,  # 대화 문맥을 전달합니다. 📨
            tools=tools_schema,  # 사용 가능한 도구 목록을 보여줍니다. 🧰
            tool_choice="auto"   # 도구 사용 여부를 AI가 자동(Auto)으로 결정합니다. 🤖
        )
        
        response_message = response.choices[0].message  # AI의 응답 메시지를 가져옵니다. 📥
        tool_calls = response_message.tool_calls  # 도구 호출 요청이 있는지 확인합니다. 🧐

        if tool_calls:  # 도구를 써야 한다고 판단했다면... ✅
            print(f"🤖 GPT: {len(tool_calls)}개의 작업을 수행합니다...")  # 작업 개수를 알립니다. 🛠️
            messages.append(response_message) # 현재까지의 대화 내역에 AI의 요청을 추가합니다. ➕

            # GPT가 요청한 도구들을 순차적으로 실행(Execute)합니다. 🏃‍♂️
            for tool_call in tool_calls:
                function_name = tool_call.function.name  # 호출할 함수 이름입니다. 🏷️
                function_args = json.loads(tool_call.function.arguments)  # 함수 인자를 파싱(Parsing)합니다. 🧩
                
                tool_result = ""  # 도구 실행 결과를 담을 변수입니다. 📦
                
                if function_name == "get_current_weather":  # 날씨 함수라면... ☀️
                    tool_result = get_current_weather(function_args.get("location"))
                elif function_name == "get_latest_news":  # 뉴스 함수라면... 📰
                    tool_result = get_latest_news(function_args.get("topic"))
                elif function_name == "create_pdf_report":  # PDF 생성 함수라면... 📑
                    # PDF 생성 실행
                    tool_result = create_pdf_report(
                        function_args.get("title"), 
                        function_args.get("content")
                    )

                messages.append({  # 도구의 실행 결과를 대화 내역에 추가(Append)합니다. 📥
                    "tool_call_id": tool_call.id,  # 요청 ID와 매칭합니다. 🔗
                    "role": "tool",  # 역할은 도구(Tool)입니다. 🔧
                    "name": function_name,  # 함수 이름입니다. 🏷️
                    "content": tool_result,  # 실행 결과입니다. 📝
                })

            # 2차 호출: 도구 결과를 바탕으로 최종 답변(Final Answer)을 생성합니다. 🏁
            # PDF 생성 후 "파일을 만들었습니다"라고 말하기 위해 필요합니다.
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            final_answer = second_response.choices[0].message.content  # 최종 답변 텍스트입니다. 🗣️
            print(f"🤖 최종 답변: {final_answer}")  # 콘솔에 답변을 출력합니다. 💻
            return final_answer
        
        else:  # 도구를 쓸 필요가 없다면(일반 대화)... 💬
            return response_message.content  # 바로 답변을 반환합니다. ↩️

    except Exception as e:  # GPT 호출 중 에러 발생 시... 🚨
        print(f"GPT 오류: {e}")
        return "죄송해요, 처리 중에 문제가 생겼어요."

# ------------------------------------------------------------
# 5. TTS 및 메인 실행
# ------------------------------------------------------------
def text_to_speech(text):  # 텍스트를 음성으로 변환(TTS)하는 함수입니다. 🔈
    try:
        # OpenAI의 음성 모델(tts-1)을 사용하여 오디오를 생성합니다. 🎵
        speech = client.audio.speech.create(model="tts-1", voice="nova", input=text)
        filename = f"reply_{int(time.time())}.mp3"  # 저장할 파일명입니다. 📁
        with open(filename, "wb") as f: f.write(speech.read())  # 파일로 저장합니다. 💾
        return filename  # 파일명을 반환합니다. ↩️
    except: return None  # 실패 시 None 반환. 🚫

def ai_voice_assistant():  # AI 비서 메인 실행 함수입니다. 🚀
    print("\n🚀 AI 비서 (날씨/뉴스 + PDF 리포트 기능) 시작!\n")  # 시작 메시지입니다. 🎉
    while True:  # 무한 반복(Loop)으로 대화를 계속합니다. 🔄
        try:
            print("\n-------------------------------------------")
            audio_file = record_voice_auto()  # 목소리를 듣습니다. 👂
            if not audio_file: continue  # 소리가 없으면 다시 듣습니다. 👂

            user_text = speech_to_text(audio_file)  # 음성을 글자로 바꿉니다. 📝
            print(f"📝 사용자: {user_text}")  # 사용자의 말을 출력합니다. 🗣️

            if "종료" in user_text:  # '종료'라는 단어가 있으면... 🛑
                playsound(text_to_speech("감사합니다. 비서를 종료합니다."))  # 작별 인사를 합니다. 👋
                break  # 프로그램을 끝냅니다. 🔚

            ai_answer = ask_gpt(user_text)  # GPT에게 질문하고 답을 받습니다. 🧠
            sound_file = text_to_speech(ai_answer)  # 답을 목소리로 바꿉니다. 🔈
            
            if sound_file:  # 오디오 파일이 생성되었다면... ✅
                playsound(sound_file)  # 소리를 재생합니다. 🔊
                time.sleep(1)  # 재생 후 잠시 대기(Sleep)합니다. 💤
                
        except KeyboardInterrupt: break  # Ctrl+C를 누르면 강제 종료합니다. ⏹️
        except Exception as e: print(e); break  # 예상치 못한 에러 시 종료합니다. 💥

if __name__ == "__main__":  # 이 파일이 직접 실행될 때만 작동합니다. ▶️
    ai_voice_assistant()  # AI 비서를 시작합니다. 🎬