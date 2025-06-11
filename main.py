import streamlit as st
import math
import re

# 🌐 페이지 설정
st.set_page_config(
    page_title="경우의 수 계산기 (문장 기반)",
    page_icon="🔣",
    layout="centered"
)

st.title("🔣 문장 기반 경우의 수 계산기")
st.markdown("자연어 문장을 입력하면 경우의 수를 자동으로 분석하고 계산해 드립니다! 🧠")
st.markdown("예: `10개의 대상 중 순서를 고려하여 3개의 자리로 중복을 허용하여 뽑는 경우의 수`")

# 📥 사용자 입력
user_input = st.text_input("📝 경우의 수 문장을 입력하세요:")

# 📐 계산 함수들
def permutation(n, r):
    return math.factorial(n) // math.factorial(n - r)

def combination(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

def repetition_combination(n, r):
    return combination(n + r - 1, r)

def analyze_sentence(text):
    # 숫자 추출
    nums = list(map(int, re.findall(r'\d+', text)))
    if len(nums) < 2:
        return None, "❗ 대상 수(n)와 선택 수(r)를 모두 포함한 문장을 입력해주세요."

    n, r = nums[0], nums[1]

    # 조건 파악
    is_ordered = "순서를 고려" in text
    is_repetition = "중복을 허용" in text

    # 분석 결과
    if is_ordered and is_repetition:
        case_type = "중복순열"
        expression = f"{n}^{r}"
        result = n ** r
        explanation = f"{n}개의 대상 중 중복을 허용하고 순서를 고려하여 {r}개를 선택하는 경우입니다."
    elif is_ordered and not is_repetition:
        case_type = "순열"
        expression = f"{n}P{r}"
        result = permutation(n, r)
        explanation = f"{n}개의 대상 중 중복 없이 순서를 고려하여 {r}개를 선택하는 경우입니다."
    elif not is_ordered and is_repetition:
        case_type = "중복조합"
        expression = f"{n}Hr{r}"
        result = repetition_combination(n, r)
        explanation = f"{n}개의 대상 중 중복을 허용하고 순서를 고려하지 않고 {r}개를 선택하는 경우입니다."
    elif not is_ordered and not is_repetition:
        case_type = "조합"
        expression = f"{n}C{r}"
        result = combination(n, r)
        explanation = f"{n}개의 대상 중 중복 없이 순서를 고려하지 않고 {r}개를 선택하는 경우입니다."
    else:
        return None, "❗ 조건을 정확히 인식하지 못했습니다."

    return {
        "case_type": case_type,
        "expression": expression,
        "result": result,
        "explanation": explanation,
        "n": n,
        "r": r
    }, None

# 📊 출력
if user_input:
    analysis, error = analyze_sentence(user_input)

    if error:
        st.warning(error)
    else:
        st.markdown("---")
        st.markdown("### 📘 문제 해석")
        st.info(analysis["explanation"])

        st.markdown("### 🔍 계산 결과")
        st.write(f"**유형:** `{analysis['case_type']}`")
        st.write(f"**수식:** `{analysis['expression']}`")
        st.success(f"👉 결과: **{analysis['result']:,}** 가지 경우의 수")
        st.balloons()
