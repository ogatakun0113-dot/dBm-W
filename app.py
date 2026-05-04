import streamlit as st
import math

# --- ページ設定 ---
st.set_page_config(page_title="dBm→W変換アプリ", layout="centered")

# --- 見た目の設定（CSS） ---
st.markdown("""
    <style>
    /* クレジット表示用のCSS */
    .credit {
        text-align: right;
        font-size: 14px;
        color: #666;
        margin-bottom: -20px;
    }
    /* 入力欄のラベルを大きく、太く、青色にする */
    .stNumberInput label {
        font-size: 32px !important;
        color: #1E90FF !important; /* ドジャーブルー */
        font-weight: 800 !important;
        line-height: 1.5;
    }
    /* 入力枠そのものを大きく、枠線を青色にする */
    div[data-baseweb="input"] {
        height: 60px !important;
        font-size: 28px !important;
        border: 3px solid #1E90FF !important;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 右上にクレジットを表示
st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)

st.title('📡 dBm → W 変換アプリ')
st.markdown("---")

# 入力欄（dBmを入力）
dbm_in = st.number_input("電力 (dBm) を入力してください", value=30.0, format="%.2f")

# 計算ロジック (50Ω系)
# 1. dBm から mW へ (P_mW = 10^(dBm/10))
mw_val = 10 ** (dbm_in / 10)

# 2. mW から W へ
w_val = mw_val / 1000

# 3. 電力(W) から 電圧(V) へ (V = sqrt(P_W * R))
v_val = math.sqrt(w_val * 50)

# 4. 電圧(V) から dBμV へ
if v_val > 0:
    dbuv_val = 20 * math.log10(v_val * 10**6)
else:
    dbuv_val = -float('inf')

# 表示
st.subheader("変換結果 (50Ω)")
c1, c2 = st.columns(2)
with c1:
    st.metric("電力 (W)", f"{w_val:,.4f}")
    st.metric("電力 (mW)", f"{mw_val:,.2f}")
with c2:
    st.metric("電圧 (V)", f"{v_val:,.4f}")
    st.metric("dBμV (50Ω)", f"{dbuv_val:.2f}")
