import json
import random  # 가짜 날씨/뉴스를 랜덤으로 만들기 위해 사용
from openai import OpenAI
from dotenv import load_dotenv
import os
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import time
from playsound import playsound

# ------------------------------------------------------------
# API 초기화
# ------------------------------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------------------------------------
# [NEW] 1. 도구(함수) 정의: AI가 사용할 실제 파이썬 함수들
# ------------------------------------------------------------

def get_current_weather(location, unit="celsius"):
    """
    [시뮬레이션] 특정 지역의 날씨 정보를 가져옵니다.
    실제로는 OpenWeatherMap 등의 API를 여기에 연결해야 합니다.
    """
    print(f"🕵️ [System] '{location}'의 날씨 정보를 조회 중...")
    
    # 실습을 위한 가짜 데이터 (랜덤 생성)
    weather_conditions = ["맑음 ☀️", "흐림 ☁️", "비 🌧️", "눈 ❄️", "바람 강함 💨"]
    temp = random.randint(-5, 30)
    condition = random.choice(weather_conditions)
    
    # 결과 반환 (JSON 형식 문자열)
    return json.dumps({
        "location": location,
        "temperature": temp,
        "unit": unit,
        "condition": condition,
        "description": f"{location}은(는) 현재 {condition}, 기온은 {temp}도입니다."
    })

def get_latest_news(topic="general"):
    """
    [시뮬레이션] 특정 주제의 최신 뉴스를 검색합니다.
    실제로는 Naver News API나 Google News API를 연결해야 합니다.
    """
    print(f"🕵️ [System] '{topic}' 관련 뉴스를 검색 중...")
    
    # 실습을 위한 가짜 뉴스 데이터
    fake_headlines = [
        f"속보: {topic} 관련 대규모 투자 발표",
        f"{topic} 기술의 혁신적인 발전, 전문가들 주목",
        f"서울에서 열린 {topic} 컨퍼런스 성황리에 종료",
        f"시민들이 가장 관심 있는 분야로 '{topic}' 선정"
    ]
    
    selected_news = random.sample(fake_headlines, 2)
    return json.dumps({"topic": topic, "headlines": selected_news})

# ------------------------------------------------------------
# [NEW] 2. 도구 스키마(Schema) 정의
# GPT에게 "이런 함수들이 있고, 이런 인자를 받아"라고 설명하는 명세서입니다.
# ------------------------------------------------------------
tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "특정 지역의 현재 날씨를 조회합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "서울, 부산, 뉴욕 등 도시 이름"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_latest_news",
            "description": "특정 주제에 대한 최신 뉴스 헤드라인을 검색합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "검색할 뉴스 키워드 (예: AI, 주식, 스포츠)"}
                },
                "required": ["topic"]
            }
        }
    }
]

# ------------------------------------------------------------
# 3. 기존 음성 녹음 및 STT 함수 (변동 없음)
# ------------------------------------------------------------
def record_voice_auto(filename="input.wav", fs=16000, silence_threshold=300, min_silence_duration=1.5):
    print("\n🎤 말씀해주세요! (말씀이 끝나면 자동으로 인식합니다)\n")
    buffer = []
    silence_start = None
    recording = True
    start_time = time.time()

    try:
        with sd.InputStream(samplerate=fs, channels=1, dtype="int16") as stream:
            while recording:
                frame, _ = stream.read(int(0.1 * fs))
                buffer.append(frame)
                volume = np.sqrt(np.mean(frame.astype(np.float64)**2))

                if time.time() - start_time < 0.5: continue

                if volume < silence_threshold:
                    if silence_start is None: silence_start = time.time()
                    elif time.time() - silence_start > min_silence_duration:
                        print("🛑 녹음 종료.")
                        recording = False
                else:
                    silence_start = None

        wav.write(filename, fs, np.concatenate(buffer, axis=0))
        return filename
    except Exception as e:
        print(f"녹음 오류: {e}")
        return None

def speech_to_text(file_path):
    if not os.path.exists(file_path): return ""
    try:
        with open(file_path, "rb") as f:
            return client.audio.transcriptions.create(model="whisper-1", file=f, language="ko").text
    except: return ""

# ------------------------------------------------------------
# [UPDATE] 4. GPT 답변 생성 (도구 사용 로직 추가)
# ------------------------------------------------------------
def ask_gpt(question):
    """
    GPT가 질문을 분석하고, 필요하면 도구(날씨, 뉴스)를 호출한 뒤 최종 답변을 생성합니다.
    """
    messages = [
        {"role": "system", "content": "당신은 날씨와 뉴스를 알려줄 수 있는 유능한 AI 비서입니다. 답변은 친절한 한국어 구어체로 해주세요."},
        {"role": "user", "content": question}
    ]

    try:
        # 1차 호출: GPT가 질문을 보고 도구를 쓸지 말지 결정
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools_schema,
            tool_choice="auto"  # GPT가 알아서 판단
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # GPT가 "도구를 써야 해!"라고 판단했을 경우
        if tool_calls:
            print("🤖 GPT: 도구(함수)를 사용해야겠어요!")
            
            # 대화 내역에 GPT의 판단(도구 호출 요청)을 추가
            messages.append(response_message)

            # GPT가 요청한 각 도구를 실제로 실행
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                function_response = ""
                
                # 함수 이름에 따라 실제 파이썬 함수 실행
                if function_name == "get_current_weather":
                    function_response = get_current_weather(
                        location=function_args.get("location"),
                        unit=function_args.get("unit", "celsius")
                    )
                elif function_name == "get_latest_news":
                    function_response = get_latest_news(
                        topic=function_args.get("topic")
                    )

                # 도구 실행 결과를 대화 내역에 추가 (role: tool)
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                })

            # 2차 호출: 도구 실행 결과를 바탕으로 최종 답변 생성
            print("🤔 정보를 바탕으로 답변 정리 중...")
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            final_answer = second_response.choices[0].message.content
            print(f"🤖 최종 답변: {final_answer}")
            return final_answer
        
        else:
            # 도구가 필요 없는 일반 대화일 경우
            print(f"🤖 GPT 답변: {response_message.content}")
            return response_message.content

    except Exception as e:
        print(f"GPT 오류: {e}")
        return "죄송해요, 처리 중에 문제가 생겼어요."

# ------------------------------------------------------------
# 5. TTS 및 메인 루프 (기존과 동일)
# ------------------------------------------------------------
def text_to_speech(text):
    try:
        speech = client.audio.speech.create(model="tts-1", voice="nova", input=text)
        filename = f"reply_{int(time.time())}.mp3"
        with open(filename, "wb") as f: f.write(speech.read())
        return filename
    except: return None

def ai_voice_assistant():
    print("\n🚀 스마트 AI 비서 (날씨/뉴스 기능 탑재) 시작!\n")
    while True:
        try:
            print("\n-------------------------------------------")
            for i in range(2, 0, -1):
                print(f"⏳ {i}...")
                time.sleep(1)
            
            audio_file = record_voice_auto()
            if not audio_file: continue

            user_text = speech_to_text(audio_file)
            print(f"📝 사용자: {user_text}")

            if not user_text.strip(): continue
            if "종료" in user_text:
                playsound(text_to_speech("네, 종료할게요. 좋은 하루 보내세요!"))
                break

            ai_answer = ask_gpt(user_text)
            sound_file = text_to_speech(ai_answer)
            
            if sound_file:
                playsound(sound_file)
                time.sleep(1)
                
        except KeyboardInterrupt: break
        except Exception as e: print(e); break

if __name__ == "__main__":
    ai_voice_assistant()