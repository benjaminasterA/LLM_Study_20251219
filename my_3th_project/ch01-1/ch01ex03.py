# ------------------------------------------------------------
# 필요한 라이브러리
# ------------------------------------------------------------
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
# 1. 자동 녹음 (말 끝날 때까지)
# ------------------------------------------------------------
def record_voice_auto(
    filename="input.wav",
    fs=16000,
    silence_threshold=300,      # 한국어 인식에 맞게 튜닝
    silence_duration=1.2
):
    print("\n🎤 이제 말씀해주세요! (말 끝날 때까지 자동 녹음)\n")

    buffer = []
    silence_start = None
    recording = True
    frame_duration = 0.1  # 0.1초씩 분석

    while recording:
        frame = sd.rec(int(frame_duration * fs), samplerate=fs, channels=1, dtype="int16")
        sd.wait()

        buffer.append(frame)
        volume = np.abs(frame).mean()

        # 🔊 한국어 발성 인식 강화
        if volume < silence_threshold:
            if silence_start is None:
                silence_start = time.time()
            elif time.time() - silence_start > silence_duration:
                print("🛑 말이 끝난 것 같습니다. 녹음을 종료합니다.")
                recording = False
        else:
            silence_start = None

    audio = np.concatenate(buffer, axis=0)
    wav.write(filename, fs, audio)

    print("🎧 녹음 완료:", filename)
    return filename


# ------------------------------------------------------------
# 2. Whisper — 한국어 음성 인식
# ------------------------------------------------------------
def speech_to_text(file_path):
    with open(file_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )

    text = result.text
    print("📝 인식된 한국어:", text)
    return text


# ------------------------------------------------------------
# 3. GPT — 한국어 답변 생성
# ------------------------------------------------------------
def ask_gpt(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "당신은 한국어로만 대답하는 친절한 AI 음성 비서입니다."},
            {"role": "user", "content": question}
        ]
    )

    answer = response.choices[0].message.content
    print("🤖 GPT 답변:", answer)
    return answer


# ------------------------------------------------------------
# 4. TTS로 음성 생성 (gpt-4o-mini-tts)
# ------------------------------------------------------------
def text_to_speech(text):
    output = f"reply_{int(time.time())}.mp3"

    speech = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )

    with open(output, "wb") as f:
        f.write(speech.read())

    print("🔊 음성 생성 완료:", output)
    return output


# ------------------------------------------------------------
# 5. 전체 음성 비서 루프
# ------------------------------------------------------------
def ai_voice_assistant():
    print("\n✨ AI 음성 비서가 준비되었습니다! (Ctrl+C로 종료)\n")

    while True:
        print("\n🎤 이제 곧 말씀해주세요!")

        # 🕒 3초 카운트다운
        for i in range(3, 0, -1):
            print(f"⏳ {i}초...")
            time.sleep(1)

        print("🎙 녹음 시작!")

        # 자동 녹음
        audio_file = record_voice_auto()

        # 음성 → 텍스트
        user_text = speech_to_text(audio_file)

        # GPT 답변 생성
        answer = ask_gpt(user_text)

        # 텍스트 → 음성
        sound_file = text_to_speech(answer)

        # 음성 재생
        playsound(sound_file)


# ------------------------------------------------------------
# 실행
# ------------------------------------------------------------
if __name__ == "__main__":
    ai_voice_assistant()
