# ------------------------------------------------------------
# 필요한 라이브러리 (playsound 사용, simpleaudio/pydub 제거)
# ------------------------------------------------------------
from openai import OpenAI
from dotenv import load_dotenv
import os
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import time
from playsound import playsound # 🎯 playsound로 대체

# ------------------------------------------------------------
# API 초기화
# ------------------------------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------------------------------------
# 1. 자동 녹음 (말 끝날 때까지 개선 버전)
# ------------------------------------------------------------
def record_voice_auto(
    filename="input.wav",
    fs=16000,
    silence_threshold=300, # 소음이 많은 환경을 고려하여 임계값 설정
    min_silence_duration=1.5,  # 무음 감지 시간 단축 (더 빠르게 종료)
    frame_duration=0.1  # 0.1초씩 더 자주 분석 (민감도 향상)
):
    """사용자의 음성 입력이 끝날 때까지 자동으로 녹음합니다."""
    print("\n🎤 이제 말씀해주세요! (말 끝난 후 1.5초 무음 시 자동 종료)\n")

    buffer = []
    silence_start = None
    recording = True
    start_time = time.time()

    try:
        # 스트림을 열어 연속적으로 오디오를 가져옴
        with sd.InputStream(samplerate=fs, channels=1, dtype="int16") as stream:
            while recording:
                frame, overflowed = stream.read(int(frame_duration * fs))

                if overflowed:
                    print("⚠️ 오디오 오버플로우 발생!")

                buffer.append(frame)
                # RMS(Root Mean Square)로 볼륨 계산
                volume = np.sqrt(np.mean(frame.astype(np.float64)**2))

                # 녹음 시작 직후 0.5초 동안은 무음 무시
                if time.time() - start_time < 0.5:
                    continue

                # 볼륨 체크 및 무음 감지
                if volume < silence_threshold:
                    if silence_start is None:
                        silence_start = time.time()
                    elif time.time() - silence_start > min_silence_duration:
                        print(f"🛑 연속 {min_silence_duration:.1f}초 무음 감지, 녹음을 종료합니다.")
                        recording = False
                else:
                    silence_start = None # 말이 계속되면 무음 초기화

        audio = np.concatenate(buffer, axis=0)
        # 16000Hz, PCM 16-bit 형식의 WAV 파일로 저장 (Whisper 권장 포맷)
        wav.write(filename, fs, audio)
        print("🎧 녹음 완료:", filename)
        return filename
    
    except Exception as e:
        print(f"❌ 녹음 중 치명적인 오류 발생: {e}")
        print("💡 마이크 장치 설정이나 권한을 확인해주세요.")
        return None

# ------------------------------------------------------------
# 2. Whisper로 한국어 음성 인식 (language="ko" 명시)
# ------------------------------------------------------------
def speech_to_text(file_path):
    """음성 파일을 텍스트로 변환합니다. 한국어 인식을 명시합니다."""
    if not file_path or not os.path.exists(file_path):
        return ""
    
    try:
        with open(file_path, "rb") as f:
            print("👂 음성 파일 텍스트 변환 중...")
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                language="ko" # 🎯 한국어 인식률 향상을 위해 명시적으로 "ko" 설정
            )
        text = result.text
        print("📝 인식된 한국어:", text)
        return text
    except Exception as e:
        print(f"❌ Whisper 변환 중 오류 발생: {e}")
        return ""


# ------------------------------------------------------------
# 3. GPT로 질문 → 한국어 답변 생성
# ------------------------------------------------------------
def ask_gpt(question):
    """GPT 모델을 사용하여 답변을 생성합니다."""
    if not question.strip():
        return "말씀을 듣지 못했습니다. 다시 말씀해 주시겠어요?"

    try:
        print(f"🤔 '{question[:15]}...'에 대한 답변 생성 중...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 한국어로만 명확하고 간결하게 대답하는 친절한 AI 음성 비서입니다."},
                {"role": "user", "content": question}
            ]
        )
        answer = response.choices[0].message.content
        print("🤖 GPT 답변:", answer)
        return answer
    except Exception as e:
        print(f"❌ GPT 답변 생성 중 오류 발생: {e}")
        return "죄송합니다. 답변을 생성하는 데 문제가 발생했습니다."


# ------------------------------------------------------------
# 4. TTS로 음성 생성
# ------------------------------------------------------------
def text_to_speech(text):
    """텍스트를 음성 파일(.mp3)로 변환합니다."""
    output = f"reply_{int(time.time())}.mp3"
    
    try:
        print("🔊 답변을 음성으로 변환 중...")
        speech = client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice="nova", # 🎯 "alloy" -> "echo" 로 변경! (저음 여성)
            input=text
        )

        with open(output, "wb") as f:
            f.write(speech.read())
        
        print("✅ 음성 파일 생성 완료:", output)
        return output
    except Exception as e:
        print(f"❌ TTS 음성 변환 중 오류 발생: {e}")
        return None

# ------------------------------------------------------------
# 5. 전체 AI 음성 비서 루프
# ------------------------------------------------------------
def ai_voice_assistant():
    print("\n✨ AI 음성 비서가 준비되었습니다! (Ctrl+C로 언제든지 종료 가능)\n")

    while True:
        try:
            print("\n-------------------------------------------")
            print("🔊 다음 질문을 준비하세요...")
            for i in range(3, 0, -1):
                print(f"⏳ {i}초 뒤 녹음 시작...")
                time.sleep(1)
            print("🎙 녹음 시작!")

            # 1️⃣ 자동 녹음
            audio_file = record_voice_auto()

            if not audio_file:
                continue

            # 2️⃣ 음성 → 텍스트
            user_text = speech_to_text(audio_file)

            if not user_text.strip():
                print("❌ 인식된 텍스트가 없습니다. 다시 말씀해주세요.")
                continue
                
            # 종료 명령어 체크
            if "종료" in user_text or "끝내" in user_text or "exit" in user_text.lower():
                final_message = "AI 음성 비서를 종료합니다. 다음에 또 뵙겠습니다!"
                print(final_message)
                sound_file = text_to_speech(final_message)
                if sound_file:
                    playsound(sound_file) # playsound로 재생
                break

            # 3️⃣ GPT 처리
            answer = ask_gpt(user_text)

            # 4️⃣ 텍스트 → 음성
            sound_file = text_to_speech(answer)

            # 5️⃣ 음성 재생
            if sound_file:
                print("🎶 음성 답변 재생 중...")
                # 🎯 playsound 호출 (재생이 완료될 때까지 블로킹될 수도 있고 아닐 수도 있음)
                playsound(sound_file) 
                # playsound가 비동기적으로 작동할 경우 다음 녹음이 시작될 때 겹칠 수 있으므로,
                # 짧은 대기 시간을 추가하여 안정성을 높입니다.
                time.sleep(1)

        except KeyboardInterrupt:
            print("\n\n👋 사용자 요청으로 AI 음성 비서를 종료합니다.")
            break
        except Exception as e:
            print(f"\n致命적 오류 발생: {e}")
            break


# ------------------------------------------------------------
# 실행
# ------------------------------------------------------------
if __name__ == "__main__":
    ai_voice_assistant()