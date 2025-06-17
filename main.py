import streamlit as st
import random
import requests

# ✅ Oxford API 인증 정보
APP_ID = "your_app_id"       # <-- 여기에 본인의 App ID 입력
APP_KEY = "your_app_key"     # <-- 여기에 본인의 App Key 입력

# ✅ 단어 → 한국어 뜻 가져오는 함수 (Oxford API)
def get_korean_meaning(word):
    url = f"https://od-api.oxforddictionaries.com/api/v2/translations/en/ko/{word.lower()}?strictMatch=false"
    headers = {"app_id": APP_ID, "app_key": APP_KEY}
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

# ✅ 퀴즈 단어 (레벨별)
words_by_level = {
    1: ['apple', 'banana', 'book', 'cat', 'dog', 'fish', 'hat', 'ice', 'key', 'lion', 'man', 'nose', 'pen', 'queen', 'rain'],
    2: ['airport', 'basket', 'candle', 'doctor', 'elephant', 'father', 'garden', 'hammer', 'island', 'jungle'],
    3: ['abandon', 'benefit', 'capture', 'declare', 'efficient', 'generate', 'identity', 'justice', 'kinetic', 'landscape'],
    4: ['allegiance', 'belittle', 'contemplate', 'detrimental', 'eloquent', 'futile', 'grievance', 'hypothetical', 'intricate', 'juxtapose'],
    5: ['antediluvian', 'bifurcate', 'circumlocution', 'diaphanous', 'ephemeral', 'farrago', 'heuristic', 'idiosyncrasy', 'juxtaposition', 'kaleidoscope']
}

questions_per_level = {
    1: 5,
    2: 5,
    3: 3,
    4: 2,
    5: 1
}

# ✅ 초기화
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.q_index = 0
    st.session_state.correct = 0
    st.session_state.selected_words = random.sample(
        words_by_level[1], questions_per_level[1]
    )

level = st.session_state.level
q_index = st.session_state.q_index
selected_words = st.session_state.selected_words
total_questions = questions_per_level[level]

# ✅ 보기 생성 함수: 뜻만 보여주고 단어 4개 중 고르기
def generate_question_options(correct_word):
    correct_meaning = get_korean_meaning(correct_word)
    if not correct_meaning:
        correct_meaning = "뜻을 불러올 수 없음"

    all_words = list(set(words_by_level[level]) - {correct_word})
    wrong_words = random.sample(all_words, 3)
    options = [correct_word] + wrong_words
    random.shuffle(options)
    return correct_meaning, options, correct_word

# ✅ UI
st.title("🇰🇷 뜻 보고 영어 단어 고르기 퀴즈")
st.subheader(f"📘 {level}단계 - 문제 {q_index + 1} / {total_questions}")

if q_index < total_questions:
    current_word = selected_words[q_index]
    meaning, options, correct_answer = generate_question_options(current_word)

    user_choice = st.radio(f"다음 뜻에 맞는 영어 단어는 무엇일까요? 👉 **{meaning}**", options)

    if st.button("제출"):
        if user_choice == correct_answer:
            st.session_state.correct += 1

        st.session_state.q_index += 1
        st.experimental_rerun()
else:
    st.success(f"{level}단계 완료! 정답 수: {st.session_state.correct} / {total_questions}")
    
    if level == 5:
        st.balloons()
        st.success("🎉 퀴즈 완료! 영어 천재! 🎉")
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
