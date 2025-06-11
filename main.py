import streamlit as st
import math

# --- 함수 정의 ---
def permutation(n, r):
    return math.factorial(n) // math.factorial(n - r)

def combination(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))

def repetition_combination(n, r):
    return combination(n + r - 1, r)

# --- 페이지 설정 ---
st.set_page_config(
    page_title="경우의 수 계산기 (선택 UI)",
    page_icon="🔢",
    layout="centered"
)

# --- 타이틀 ---
st.title("🔢 경우의 수 계산기")
st.markdown("**구조화된 선택 UI**를 통해 경우의 수를 계산합니다.")
st.markdown("각 항목을 선택해 주세요. 🎯")

# --- 입력 섹션 1 ---
st.markdown("### [1] 대상 개수 설정")
n = st.number_input("🎯 전체 대상 수 (n)", min_value=1, value=5, step=1)

# --- 입력 섹션 2 ---
st.markdown("### [2] 순서 고려 여부")
order = st.radio(
    "📐 순서를 어떻게 할까요?",
    ["순서를 고려하지 않고", "순서를 고려하여"]
)

# --- 입력 섹션 3 ---
st.markdown("### [3] 선택할 자리 수 설정")
r = st.number_input("📌 선택할 자리 수 (r)", min_value=1, value=3, step=1)

# --- 입력 섹션 4 ---
st.markdown("### [4] 중복 허용 여부")
duplication = st.radio(
    "🔁 중복 선택을 허용할까요?",
    ["중복을 허용하지 않고", "중복을 허용하여"]
)

# --- 계산 버튼 ---
if st.button("📊 경우의 수 계산하기"):
    case_type = ""
    expression = ""
    result = None
    explanation = ""

    try:
        # 조건 분기
        if order == "순서를 고려하여" and duplication == "중복을 허용하지 않고":
            case_type = "순열"
            expression = f"{n}P{r}"
            result = permutation(n, r)
            explanation = f"{n}개의 대상 중 **중복 없이 순서를 고려**하여 {r}개를 뽑는 경우입니다."

        elif order == "순서를 고려하여" and duplication == "중복을 허용하여":
            case_type = "중복순열"
            expression = f"{n}^{r}"
            result = n ** r
            explanation = f"{n}개의 대상 중 **중복 허용하며 순서를 고려**하여 {r}개를 뽑는 경우입니다."

        elif order == "순서를 고려하지 않고" and duplication == "중복을 허용하지 않고":
            case_type = "조합"
            expression = f"{n}C{r}"
            result = combination(n, r)
            explanation = f"{n}개의 대상 중 **중복 없이 순서를 고려하지 않고** {r}개를 뽑는 경우입니다."

        elif order == "순서를 고려하지 않고" and duplication == "중복을 허용하여":
            case_type = "중복조합"
            expression = f"{n}Hr{r}"
            result = repetition_combination(n, r)
            explanation = f"{n}개의 대상 중 **중복을 허용하고 순서를 고려하지 않고** {r}개를 뽑는 경우입니다."

        # --- 출력 ---
        st.markdown("---")
        st.markdown("### 📘 해석")
        st.info(explanation)

        st.markdown("### 📐 수식 및 결과")
        st.write(f"**유형:** `{case_type}`")
        st.latex(expression)
        st.success(f"👉 결과: **{result:,}** 가지 경우의 수")
        st.balloons()

    except Exception as e:
        st.error("❗ 유효하지 않은 입력입니다. n ≥ r 조건을 확인해주세요.")
