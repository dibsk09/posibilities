import streamlit as st
import re
import math

# 🌐 페이지 설정
st.set_page_config(
    page_title="경우의 수 계산기",
    page_icon="🔢",
    layout="centered"
)

# 💎 로비 제목
st.title("🔢 경우의 수 계산기")
st.markdown("자연어 문장을 입력하면 경우의 수를 계산해 드립니다! 🧠")

# 📥 입력 창
user_input = st.text_input("예: 5명 중 3명을 순서 없이 뽑는 경우의 수는?")

# 👉 수학 함수들
def permutation(n, r):
    return math.factorial(n) // math.factorial(n - r)

def combination(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

def repetition_combination(n, r):
    return combination(n + r - 1, r)

# 🧠 자연어 해석 함수
def parse_case(text):
    # 숫자 추출
    nums = list(map(int, re.findall(r'\d+', text)))
    if len(nums) < 2:
        return None, None, None

    n, r = nums[0], nums[1]

    # 조합
    if "순서 없이" in text or "조합" in text or "뽑는" in text:
        if "중복" in text or "같은 사람" in text:
            return "중복조합", f"{n}Hr{r}", repetition_combination(n, r)
        else:
            return "조합", f"{n}C{r}", combination(n, r)

    # 순열
    if "순서 있게" in text or "줄을 세우는" in text or "배열" in text or "순열" in text:
        return "순열", f"{n}P{r}", permutation(n, r)

    return None, None, None

# 📊 결과 처리
if user_input:
    case_type, expression, result = parse_case(user_input)

    if case_type:
        st.markdown("### 🎯 해석 결과")
        st.info(f"📘 유형: `{case_type}`\n\n🧮 수식: `{expression}`")
        st.success(f"✅ 결과: **{result:,}** 가지 경우")
        st.balloons()
    else:
        st.warning("❗ 문장을 제대로 이해하지 못했어요. 예: '7명 중 3명을 순서 없이 뽑는 경우의 수' 처럼 입력해 주세요.")
