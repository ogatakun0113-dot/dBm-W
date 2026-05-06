import streamlit as st
import math

# --- ページ設定 ---
st.set_page_config(page_title="W ⇄ dBm 変換アプリ", layout="centered")

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
    /* 入力欄のラベルスタイル */
    .stNumberInput label {
        font-size: 28px !important;
        color: #1E90FF !important;
        font-weight: 800 !important;
        line-height: 1.5;
    }
    /* 入力枠のサイズとスタイル */
    div[data-baseweb="input"] {
        height: 60px !important;
        font-size: 28px !important;
        border: 3px solid #1E90FF !important;
        border-radius: 10px;
    }
    /* 結果表示ボックス */
    .result-box {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #1E90FF;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 右上にクレジットを表示
st.markdown('<p class="credit">開発/制作：緒方</p>', unsafe_allow_html=True)

st.title('📡 W ⇄ dBm 相互変換アプリ')
st.markdown("---")

# --- インピーダンス設定セクション ---
st.subheader("⚙️ インピーダンス設定")
impedance = st.radio("使用するインピーダンスを選択してください", [50, 75], index=0, horizontal=True, format_func=lambda x: f"{x} Ω")

# --- 入力切替セクション ---
mode = st.radio("入力する単位を選択してください", ["dBm を入力", "W (ワット) を入力"], horizontal=True)

dbm_val = 0.0
w_val = 0.0
mw_val = 0.0

if mode == "dBm を入力":
    dbm_in = st.number_input("電力 (dBm)", value=30.0, format="%.2f", step=1.0)
    dbm_val = dbm_in
    # dBm -> mW -> W (抵抗に関わらず一定)
    mw_val = 10 ** (dbm_in / 10)
    w_val = mw_val / 1000
else:
    w_in = st.number_input("電力 (W)", value=1.0, format="%.4f", step=0.1)
    w_val = w_in
    if w_in > 0:
        # W -> mW -> dBm (抵抗に関わらず一定)
        mw_val = w_in * 1000
        dbm_val = 10 * math.log10(mw_val)
    else:
        mw_val = 0.0
        dbm_val = -float('inf')

# --- 追加計算 (選択されたインピーダンスを使用) ---
# 電圧 (V) = sqrt(P_W * R)
v_val = math.sqrt(w_val * impedance)

# 電圧レベル (dBμV)
if v_val > 0:
    dbuv_val = 20 * math.log10(v_val * 10**6)
else:
    dbuv_val = -float('inf')

# --- 表示セクション ---
st.markdown('<div class="result-box">', unsafe_allow_html=True)
st.subheader(f"📊 変換結果 ({impedance}Ω系)")

col1, col2 = st.columns(2)
with col1:
    st.metric("電力 (dBm)", f"{dbm_val:.2f} dBm")
    st.metric("電力 (W)", f"{w_val:,.4f} W")

with col2:
    st.metric("電圧 (V)", f"{v_val:,.4f} V")
    st.metric("電圧レベル (dBμV)", f"{dbuv_val:.2f} dBμV")

st.write(f"電力 (mW): **{mw_val:,.2f} mW**")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")
# ヒントに各インピーダンスでの特性を表示
if impedance == 50:
    st.caption("💡 50Ω系: 0dBm (1mW) ≒ 107dBμV (0.224V) です。")
else:
    st.caption("💡 75Ω系: 0dBm (1mW) ≒ 108.75dBμV (0.274V) です。")
st.caption("※30dBm = 1W / 0dBm = 1mW は共通です。")
