import streamlit as st
import pandas as pd

# タイトル（大きく）
st.markdown("<h1 style='font-size:36px'>🏌️‍♂️ イーグル会ベット計算機</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size:18px'>ゴルフのラウンド後に各賞の精算を自動で計算します。</p>", unsafe_allow_html=True)

# プレイヤー名を固定
players = ["A", "B", "C", "D"]

# 結果用データフレーム
categories = ["優勝", "ベスト", "ドラニヤ", "バーディ", "ストローク"]
results = pd.DataFrame(0, index=categories, columns=players)

# 優勝
winner_victory = st.radio("優勝の勝者", players)
for p in players:
    results.loc["優勝", p] = 500*3 if p == winner_victory else -500

# ベスト・ドラニヤ・バーディ
awards = [("ベスト", 200), ("ドラニヤ", 300), ("バーディ", 500)]
for cat, value in awards:
    st.subheader(f"{cat}（単価 {value}円）")
    inputs = [st.number_input(f"{p} の {cat} 数字", min_value=0, value=0) for p in players]
    for i, p in enumerate(players):
        others_sum = sum(inputs) - inputs[i]
        results.loc[cat, p] = (inputs[i]*3 - others_sum) * value

# ストローク
st.subheader("ストローク（単価100円）")
scores = [st.number_input(f"{p} のスコア", min_value=0, value=0) for p in players]
for i, p in enumerate(players):
    diff_sum = sum(scores[i] - scores[j] for j in range(len(players)) if j != i)
    results.loc["ストローク", p] = -diff_sum * 100  # 高スコアはマイナス

# 合計
results.loc["合計"] = results.sum()

st.divider()
st.subheader("💰 計算結果")
st.dataframe(results.style.format("{:+,}", na_rep="0").set_table_styles(
    [{'selector':'th','props':[('font-size','18px')]},
     {'selector':'td','props':[('font-size','18px')]}]
))

