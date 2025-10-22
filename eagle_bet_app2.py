import streamlit as st
import pandas as pd

st.markdown("<h2 style='font-size:30px'>🏌️‍♂️ イーグル会ベット計算機</h2>", unsafe_allow_html=True)

# プレイヤー名固定
players = ["辻", "菅井", "木村", "霜田"]

st.divider()

# 結果用データフレーム作成
categories = ["優勝", "ベスト", "ドラニヤ", "バーディ", "ストローク"]
results = pd.DataFrame(0, index=categories, columns=players)

# 優勝
st.subheader("優勝（500円）")
winner_victory = st.radio("優勝の勝者を選択", players)
for p in players:
    results.loc["優勝", p] = 500*3 if p == winner_victory else -500

# ベスト・ドラニヤ・バーディ
awards = [("ベスト", 200), ("ドラニヤ", 300), ("バーディ", 500)]
for cat, value in awards:
    st.subheader(f"{cat}（単価 {value}円）")
    inputs = [st.number_input(f"{p} の {cat} 数", min_value=0, value=0) for p in players]
    for i, p in enumerate(players):
        others_sum = sum(inputs) - inputs[i]
        results.loc[cat, p] = (inputs[i]*3 - others_sum) * value

# ストローク
st.subheader("ストローク（単価100円）")
scores = [st.number_input(f"{p} のスコア", min_value=0, value=72) for p in players]
for i, p in enumerate(players):
    diff_sum = sum(scores[i] - scores[j] for j in range(len(players)) if j != i)
    results.loc["ストローク", p] = -diff_sum * 100

# 合計
results.loc["合計"] = results.sum()

st.divider()
st.subheader("💰 計算結果")

# HTMLで表を作成
html_table = results.to_html(classes='table', border=1, justify='center')

# <th>（列名・ヘッダー）は18px、<td>（数字部分）は22px
html_table = html_table.replace(
    '<table border="1" class="dataframe table">',
    '<table border="1" class="dataframe table" style="text-align:center;">'
)

# ヘッダーサイズ
html_table = html_table.replace('<th>', '<th style="font-size:14px;">')

# 数字サイズ
html_table = html_table.replace('<td>', '<td style="font-size:20px;">')

st.markdown(html_table, unsafe_allow_html=True)







