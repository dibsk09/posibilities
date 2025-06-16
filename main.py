import streamlit as st
import math

# 계산 함수 정의
def factorial(n):
    return math.factorial(n)

def nCr(n, r):
    if r > n:
        return 0
    return factorial(n) // (factorial(r) * factorial(n - r))

def nPr(n, r):
    if r > n:
        return 0
    return factorial(n) // factorial(n - r)

def nHr(n, r):
    return nCr(n + r - 1, r)

def repeat_permutation(n, r):
    return n ** r

# Streamlit 앱 시작
st.title("🎲 경우의 수 계산기")

st.markdown("**아래 질문에 답하고, n과 r을 입력하세요.**")

col1, col2 = st.columns(2)

with col1:
    order = st.selectbox("순서를 고려하는가?", options=["O", "X"])
with col2:
    repeat = st.selectbox("중복을 허용하는가?", options=["O", "X"])

n = st.number_input("전체 항목 개수 n", min_value=0, step=1)
r = st.number_input("선택할 항목 개수 r", min_value=0, step=1)

if st.button("계산하기"):
    if order == "X" and repeat == "X":
        result = nCr(n, r)
        formula = "조합 (nCr)"
    elif order == "O" and repeat == "X":
        result = nPr(n, r)
        formula = "순열 (nPr)"
    elif order == "X" and repeat == "O":
        result = nHr(n, r)
        formula = "중복 조합 (nHr)"
    elif order == "O" and repeat == "O":
        result = repeat_permutation(n, r)
        formula = "중복 순열 (n^r)"
    else:
        result = None
        formula = "알 수 없음"

    st.markdown(f"### ✅ 선택된 계산식: **{formula}**")
    st.markdown(f"**n = {n}, r = {r}**")
    st.success(f"🔢 결과: {result}")
