from openai import OpenAI
from dotenv import load_dotenv
import os
import csv

# ------------------------------------------------------------
# 1) 자치구 코드 매핑
#    - 서울 생활인구 CSV에서 "행정동코드" 앞 5자리가 구를 구분하는 기준입니다.
#    - 예: 11110 → 종로구, 11140 → 중구
# ------------------------------------------------------------
GU_CODE_PREFIX = {
    "종로구": "11110",
    "중구": "11140",
    "용산구": "11170",
    "성동구": "11200",
    "광진구": "11215",
    "동대문구": "11230",
    "중랑구": "11260",
    "성북구": "11290",
    "강북구": "11305",
    "도봉구": "11320",
    "노원구": "11350",
}


# ------------------------------------------------------------
# 2) CSV에서 특정 구의 생활인구 합계를 계산하는 함수
#    - CSV 파일 구조는 서울열린데이터광장 "생활인구" 데이터를 기준으로 만들어졌습니다.
#    - 행정동코드 앞 5자리(prefix)로 구 구분
#    - "생활인구합계" 열의 값들을 모두 더해 최종 구별 인구를 계산합니다.
# ------------------------------------------------------------
def load_population_by_gu(csv_path: str, gu_name: str) -> float:
    """행정동코드 앞 5자리 기준으로 특정 구의 생활인구 합계를 계산합니다."""

    # 해당 구의 코드 prefix 찾기
    prefix = GU_CODE_PREFIX.get(gu_name)
    if prefix is None:
        raise ValueError(f"{gu_name}은(는) 지원되지 않는 구 이름입니다.")

    total = 0.0

    # CSV는 euc-kr 인코딩인 경우가 일반적
    with open(csv_path, "r", encoding="euc-kr") as f:
        reader = csv.DictReader(f)

        for row in reader:
            code = row["행정동코드"].strip()

            # 코드가 prefix로 시작하면 해당 구에 속한 동
            if code.startswith(prefix):

                # 생활인구합계(문자열)을 float으로 변환
                val = row["생활인구합계"].strip()

                # '*' 처럼 비공개 데이터는 float 변환 실패 → 건너뛰기
                try:
                    total += float(val)
                except ValueError:
                    continue

    return total


# ------------------------------------------------------------
# 3) Assistant에게 질문하고 답변을 받아 출력하는 함수
#    - Assistants API 기반 (deprecated이지만 여전히 동작)
#    - 구별 생활인구 값을 전달하고, GPT가 분석 설명하도록 요청
# ------------------------------------------------------------
def ask_about_gu(client: OpenAI, assistant_id: str, gu_name: str):

    # 1) CSV에서 해당 구의 생활인구 합계 계산
    population = load_population_by_gu("seoul_population.csv", gu_name)

    # 2) Thread 생성 (대화 공간 만들기)
    thread = client.beta.threads.create()

    # 3) 사용자 메시지 구성
    user_message = (
        f"다음은 서울시 {gu_name}의 생활인구 합계입니다.\n\n"
        f"- 구 이름: {gu_name}\n"
        f"- 생활인구 합계: {population:,.0f}명\n\n"
        "이 수치를 바탕으로, 이 구의 인구 규모를 설명해 주세요. "
        "서울의 다른 구들과 비교했을 때 대략 어느 정도 수준인지도 함께 설명해 주세요."
    )

    # 4) 사용자 메시지를 Thread에 입력
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message,
    )

    # 5) Assistant 실행 + 완료될 때까지 대기
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

    # 6) Assistant의 답변 메시지 조회
    messages = client.beta.threads.messages.list(thread_id=thread.id)

    # 가장 마지막 assistant 메시지를 찾아 출력
    for msg in reversed(messages.data):
        if msg.role == "assistant":
            for c in msg.content:
                if c.type == "text":
                    print("\n[assistant]")
                    print(c.text.value)
            break


# ------------------------------------------------------------
# 4) 메인 실행부
# ------------------------------------------------------------
if __name__ == "__main__":

    # .env 파일에서 API KEY 불러오기
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # 1) Assistant 생성
    assistant = client.beta.assistants.create(
        name="서울시 인구 전문가",
        instructions=(
            "당신은 서울시 각 구의 생활인구 통계를 이해하기 쉽게 설명해 주는 전문가입니다. "
            "사용자가 전달하는 숫자 데이터를 바탕으로 한국어로 자세히 설명해 주세요."
        ),
        model="gpt-4.1-mini",
    )

    print("생성된 Assistant id:", assistant.id)

    # 2) 종로구 인구를 GPT에게 설명 요청
    ask_about_gu(client, assistant.id, "종로구")

