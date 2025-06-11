
import streamlit as st
import math

# 페이지 설정
st.set_page_config(
    page_title="경우의 수 계산기",
    page_icon="🔢",
    layout="centered"
)

# 제목
st.title("🔢 경우의 수 계산기")
st.markdown("선택 조건에 따라 경우의 수를 계산해 드립니다! 🧠")

# --- 사용자 입력 섹션 ---
st.markdown("### 📥 조건을 선택하세요:")

n = st.number_input("전체 항목 수 (n)", min_value=1, step=1)
r = st.number_input("선택할 항목 수 (r)", min_value=1, step=1)

col1, col2 = st.columns(2)

with col1:
    duplication = st.selectbox("중복 선택", ["불가능", "가능"])

with col2:
    order = st.selectbox("순서 고려", ["고려하지 않음", "고려함"])

# 계산 함수들
def permutation(n, r):
    return math.factorial(n) // math.factorial(n - r)

def combination(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

def repetition_combination(n, r):
    return combination(n + r - 1, r)

# 계산 처리
if st.button("🔍 경우의 수 계산하기"):
    result = None
    case_type = ""
    expression = ""

    try:
        if duplication == "불가능" and order == "고려하지 않음":
            result = combination(n, r)
            case_type = "조합"
            expression = f"{n}C{r}"

        elif duplication == "불가능" and order == "고려함":
            result = permutation(n, r)
            case_type = "순열"
            expression = f"{n}P{r}"

        elif duplication == "가능" and order == "고려하지 않음":
            result = repetition_combination(n, r)
            case_type = "중복조합"
            expression = f"{n}Hr{r}"

        elif duplication == "가능" and order == "고려함":
            result = n ** r
            case_type = "중복순열"
            expression = f"{n}^{r}"

        # 출력
        st.markdown("### 🎯 계산 결과")
        st.info(f"📘 유형: `{case_type}`\n\n🧮 수식: `{expression}`")
        st.success(f"✅ 결과: **{result:,}** 가지 경우")
        st.balloons()

    except Exception as e:
        st.error("❌ 유효한 입력이 아닙니다. n ≥ r 조건을 확인하세요.")
