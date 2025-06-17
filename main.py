import streamlit as st
import random
import requests

# ✅ Oxford Dictionaries API 설정
APP_ID = "your_app_id"  # 여기에 발급받은 App ID 입력
APP_KEY = "your_app_key"  # 여기에 발급받은 App Key 입력

# ✅ Oxford API로 단어의 한국어 뜻 가져오기
def get_korean_meaning(word):
    url = f"https://od-api.oxforddictionaries.com/api/v2/translations/en/ko/{word.lower()}?strictMatch=false"
    headers = {
        "app_id": APP_ID,
        "app_key": APP_KEY
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            meaning = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['translations'][0]['text']
            return meaning
        except Exception:
            return None
    else:
        return None

# ✅ 오답 후보로 쓸 랜덤 한국어 단어 모음
fake_korean_meanings = [
    "식물", "컴퓨터", "아빠", "바다", "텔레비전", "우산", "병원", "사탕", "음악", "산책",
    "강", "비행기", "의자", "시계", "고양이", "치킨", "학교", "달력", "피자", "냉장고"
]

# ✅ 레벨별 단어 리스트
words_by_level = {
    1: ['apple', 'banana', 'book', 'cat', 'dog', 'fish', 'girl', 'hat', 'ice', 'key'],
    2: ['airport', 'basket', 'candle', 'doctor', 'elephant', 'father', 'garden', 'hammer', 'island', 'jungle'],
    3: ['abandon', 'benefit', 'capture', 'declare', 'efficient', 'fascinate', 'generate', 'identity', 'justice', 'kinetic'],
    4: ['allegiance', 'belittle', 'contemplate', 'detrimental', 'eloquent', 'futile', 'grievance', 'hypothetical', 'intricate', 'juxtapose'],
    5: ['antediluvian', 'bifurcate', 'circumlocution', 'diaphanous', 'ephemeral', 'farrago', 'grandiloquent', 'heuristic', 'idiosyncrasy', 'juxtaposition']
}

questions_per_level = {
    1: 5,
    2: 5,
    3: 3,
    4: 2,
    5: 1
}

# ✅ 세션 상태 초기화
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.q_index = 0
    st.session_state.correct = 0
    st.session_state.selected_words = random.sample(
        words_by_level[1], questions_per_level[1]
    )

# ✅ 현재 상태
level = st.session_state.level
q_index = st.session_state.q_index
selected_words = st.session_state.selected_words
total_questions = questions_per_level[level]

# ✅ 보기 생성 함수
def generate_options(correct_word):
    correct_meaning = get_korean_meaning(correct_word)
    if not correct_meaning:
        correct_meaning = "정답 뜻 없음"

    wrong_meanings = random.sample(
        [m for m in fake_korean_meanings if m != correct_meaning],
        3
    )
    options = [correct_meaning] + wrong_meanings
    random.shuffle(options)
    return options, correct_meaning

# ✅ UI 출력
st.title("🇬🇧 영어 단어 → 뜻 퀴즈")
st.subheader(f"📘 {level}단계 - 문제 {q_index + 1} / {total_questions}")

if q_index < total_questions:
    current_word = selected_words[q_index]
    options, correct_answer = generate_options(current_word)

    user_answer = st.radio(f"👉 다음 단어의 뜻을 고르세요: **{current_word}**", options)

    if st.button("제출"):
        if user_answer == correct_answer:
            st.session_state.correct += 1

        st.session_state.q_index += 1
        st.experimental_rerun()
else:
    st.success(f"✅ {level}단계 완료! 맞은 개수: {st.session_state.correct} / {total_questions}")

    if level == 5:
        st.balloons()
        st.success("🎉 영어 마스터! 5단계까지 전부 완료했습니다! 🎉")
    else:
        if st.button("📚 다음 단계로 이동"):
            st.session_state.level += 1
            st.session_state.q_index = 0
            st.session_state.correct = 0
            st.session_state.selected_words = random.sample(
                words_by_level[st.session_state.level],
                questions_per_level[st.session_state.level]
            )
            st.experimental_rerun()
