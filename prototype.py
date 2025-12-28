# -*- coding: utf-8 -*-
"""
Created on Sun Dec 28 16:01:09 2025

@author: cdrab
"""

import streamlit as st
import pandas as pd
# 簡易的なデータ保持のためsession_stateを使用（再起動で消えます）

# ページ設定
st.set_page_config(page_title="Ego-Truck: 欲望のフードトラック", layout="centered")

# CSSでデザイン調整（スマホで見やすく）
st.markdown("""
    <style>
    .big-font { font-size:20px !important; font-weight:bold; }
    .progress-bar-text { color: #ff4b4b; }
    </style>
    """, unsafe_allow_html=True)

# タイトルと世界観の共有
st.title("🚚 Ego-Truck Request")
st.info("【震災復興支援】あなたの「わがまま」を教えてください。同じ欲望を持つ人が10人集まれば、フードトラックが駆けつけます。")

# データ初期化
if 'requests' not in st.session_state:
    st.session_state.requests = pd.DataFrame({
        'Menu': ['激辛ラーメン', '焼きたてメロンパン', '冷えた生ビール'],
        'Votes': [3, 7, 5],
        'User': ['匿名A', '匿名B', '匿名C']
    })
# === 追加機能: 同調圧力の解除（ガヤ機能） ===
st.divider()
st.subheader("みんなの心の声（匿名）")
# ダミーの「心の声」を表示
st.chat_message("user").write("毎日おにぎりはキツイ...甘いものが食べたい")
st.chat_message("user").write("隣の佐藤さんも『肉が食いたい』って言ってた")
st.chat_message("user").write("不謹慎かもしれないけど、炭酸ジュース飲みたい...")

st.caption("あなたも正直な気持ちを書いて大丈夫です。ここは匿名です。")
# ==========================================

# 1. 欲望入力フォーム（サイドバーまたは上部）
with st.expander("欲望を投稿する（匿名）", expanded=True):
    new_item = st.text_input("今、一番食べたいものは？（例：タピオカミルクティー）")
    if st.button("欲望を送信"):
        if new_item:
            new_data = pd.DataFrame({'Menu': [new_item], 'Votes': [1], 'User': ['あなた']})
            st.session_state.requests = pd.concat([st.session_state.requests, new_data], ignore_index=True)
            st.success(f"「{new_item}」をリクエストしました！仲間を集めましょう。")
        else:
            st.warning("メニュー名を入力してください。")

# 2. ランキングと投票機能
st.divider()
st.subheader("現在エントリー中の欲望リスト")

# データを投票数順にソート
df = st.session_state.requests.sort_values('Votes', ascending=False)

for index, row in df.iterrows():
    col1, col2, col3 = st.columns([3, 1, 2])
    
    with col1:
        st.markdown(f"### {row['Menu']}")
        # プログレスバー（目標10票）
        progress = min(row['Votes'] / 10, 1.0)
        st.progress(progress)
        st.caption(f"現在: {row['Votes']}票 / 目標: 10票")
    
    with col2:
        # 投票ボタン（ユニークキーを設定）
        if st.button("食べたい!", key=f"vote_{index}"):
            # 投票数をインクリメント
            st.session_state.requests.at[index, 'Votes'] += 1
            st.rerun()

    with col3:
        # 達成判定
        if row['Votes'] >= 10:
            st.error("🎊 招致決定！ 🎊")
            st.write("明日12時に広場へ")
        else:
            remain = 10 - row['Votes']
            st.write(f"あと {remain} 人")

    st.markdown("---")

# プロトタイピングのヒント
st.sidebar.markdown("### 管理者用パネル")
if st.sidebar.button("リセット"):
    st.session_state.requests = pd.DataFrame({
        'Menu': ['激辛ラーメン', '焼きたてメロンパン', '冷えた生ビール'],
        'Votes': [3, 7, 5],
        'User': ['匿名A', '匿名B', '匿名C']
    })
    st.rerun()