import streamlit as st
import random

# 단어 목록 (단계별)
words_by_level = {
    1: ['apple', 'banana', 'book', 'cat', 'dog', 'egg', 'fish', 'girl', 'hat', 'ice',
        'juice', 'key', 'lion', 'man', 'nose', 'orange', 'pen', 'queen', 'rain', 'sun',
        'tree', 'umbrella', 'van', 'water', 'x-ray', 'yogurt', 'zoo', 'car', 'desk', 'ear',
        'frog', 'goat', 'home', 'ink', 'jam', 'kite', 'leaf', 'milk', 'net', 'owl'],
    2: ['airport', 'basket', 'candle', 'doctor', 'elephant', 'father', 'garden', 'hammer',
        'island', 'jungle', 'kitchen', 'letter', 'mirror', 'needle', 'office', 'pencil',
        'quiet', 'rabbit', 'school', 'ticket', 'uncle', 'village', 'window', 'xylophone',
        'yawn', 'zebra', 'blanket', 'cloud', 'dream', 'engine', 'floor', 'glove', 'horse',
        'idea', 'jacket', 'kangaroo', 'ladder', 'movie', 'nurse', 'ocean', 'pocket'],
    3: ['abandon', 'benefit', 'capture', 'declare', 'efficient', 'fascinate', 'generate',
        'hesitate', 'identity', 'justice', 'kinetic', 'landscape', 'mechanism', 'narrate',
        'obstacle', 'paradox', 'quantity', 'reliable', 'subtle', 'tangible', 'ultimate',
        'valid', 'wealth', 'xenophobia', 'yield', 'zeal', 'agile', 'brisk', 'crucial',
        'diminish', 'endure', 'fluctuate', 'gratify', 'hinder', 'implement', 'jeopardy',
        'keen', 'lucrative', 'meticulous', 'notion'],
    4: ['allegiance', 'belittle', 'contemplate', 'detrimental', 'eloquent', 'futile',
        'grievance', 'hypothetical', 'intricate', 'juxtapose', 'knack', 'languish',
        'manipulate', 'negligent', 'obsolete', 'persevere', 'quaint', 'relinquish',
        'scrutinize', 'tenacious', 'unprecedented', 'vulnerable', 'withstand', 'xenial',
        'yearn', 'zealous', 'ascertain', 'bolster', 'converge', 'deviate', 'elusive',
        'frivolous', 'galvanize', 'haphazard', 'impede', 'jubilant', 'kinship', 'lament',
        'morbid', 'nostalgia'],
    5: ['antediluvian', 'bifurcate', 'circumlocution', 'diaphanous', 'ephemeral',
        'farrago', 'grandiloquent', 'heuristic', 'idiosyncrasy', 'juxtaposition',
        'kaleidoscope', 'limerence', 'magnanimous', 'nefarious', 'obfuscate',
        'perspicacious', 'quixotic', 'recalcitrant', 'sesquipedalian', 'tintinnabulation',
        'ubiquitous', 'verisimilitude', 'wanderlust', 'xenoglossy', 'yonder', 'zephyr',
        'abscond', 'blandishment', 'cacophony', 'denouement', 'effervescent', 'flummox',
        'garrulous', 'harangue', 'insidious', 'jejune', 'kowtow', 'lachrymose', 'maelstrom',
        'nadir', 'obsequious']
}

questions_per_level = {1: 10, 2: 7, 3: 5, 4: 2, 5: 1}

# 초기화
if 'level' not in st.session_state:
    st.session_state.level = 1
    st.session_state.q_index = 0
    st.session_state.correct = 0
    st.session_state.selected_words = random.sample(words_by_level[1], questions_per_level[1])

level = st.session_state.level
q_index = st.session_state.q_index
selected_words = st.session_state.selected_words
total_questions = questions_per_level[level]

# 뜻 생성기 (정답은 "단어의 뜻", 오답은 다른 단어들의 뜻처럼 보임)
def generate_meanings(correct_word):
    # 오답 후보 3개 선택
    fake_words = random.sample(
        [w for w in words_by_level[level] if w != correct_word],
        3
    )

    # 뜻 목록 구성
    options_dict = {
        f"{correct_word}의 뜻": correct_word,
        f"{fake_words[0]}의 뜻": fake_words[0],
        f"{fake_words[1]}의 뜻": fake_words[1],
        f"{fake_words[2]}의 뜻": fake_words[2]
    }

    options = list(options_dict.keys())
    correct_answer = f"{correct_word}의 뜻"
    random.shuffle(options)
    return options, correct_answer

# 문제 표시
st.title("📘 영어 단어 뜻 맞추기")
st.subheader(f"{level}단계 - 문제 {q_index + 1} / {total_questions}")

if q_index < total_questions:
    current_word = selected_words[q_index]
    options, correct_answer = generate_meanings(current_word)

    user_answer = st.radio(f"다음 단어의 뜻을 고르세요: **{current_word}**", options)

    if st.button("제출"):
        if user_answer == correct_answer:
            st.session_state.correct += 1

        st.session_state.q_index += 1
        st.experimental_rerun()
else:
    st.success(f"{level}단계 완료! 맞은 개수: {st.session_state.correct} / {total_questions}")

    if level == 5:
        st.balloons()
        st.success("🎉 영어짱!!! 🎉")
    else:
        if st.button("다음 단계로 이동"):
            st.session_state.level += 1
            st.session_state.q_index = 0
            st.session_state.correct = 0
            st.session_state.selected_words = random.sample(
                words_by_level[st.session_state.level],
                questions_per_level[st.session_state.level]
            )
            st.experimental_rerun()
