import math
import random
import time

import streamlit as st
from decimal import Decimal, getcontext

st.set_page_config(
    page_title='付与ポイント計算',
    page_icon='☕',
    layout='wide',
    initial_sidebar_state='collapsed',
)

getcontext().prec = 5

APP_VERSION = '02'
APP_UPDATED = '2026-09-05'

# 会員ランクの基本還元率（計算に使う値。変更しない）
diamond = 0.03
gold = 0.02
silver = 0.01
white = 0.01
beans_club = 0.7

EVENT_RATE_CHOICES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50]
EVENT_MULTIPLIER_CHOICES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]
# 商品設定の早見。Decimal(0.02) と同じリテラルを使う
PRODUCT_EVENT_RATES = [
    (2, 0.02), (3, 0.03), (4, 0.04), (5, 0.05),
    (6, 0.06), (7, 0.07), (8, 0.08), (9, 0.09),
    (10, 0.10), (15, 0.15), (20, 0.20),
    (25, 0.25), (30, 0.30), (40, 0.40), (50, 0.50),
]

st.markdown(
    """
    <style>
    @import url("https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap");
    html, body, .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stMarkdownContainer"], [data-testid="stButton"] button,
    input, textarea, select, label, p, h1, h2, h3, h4, h5, .pc, .slot-stage {
        font-family: "Yu Gothic UI", "Yu Gothic", "Hiragino Sans",
            "Hiragino Kaku Gothic ProN", "Noto Sans JP", Meiryo, sans-serif !important;
    }
    :root {
        --ink: var(--text-color, var(--textColor, #1d2939));
        --muted: color-mix(in srgb, var(--text-color, #1d2939) 62%, var(--background-color, #ffffff));
        --soft: color-mix(in srgb, var(--text-color, #1d2939) 82%, var(--background-color, #ffffff));
        --surface: var(--background-color, #ffffff);
        --surface-2: var(--secondary-background-color, #f8fafc);
        --line: color-mix(in srgb, var(--text-color, #1d2939) 16%, var(--background-color, #ffffff));
        --accent: var(--primary-color, var(--primaryColor, #1f77b4));
        --result-bg: color-mix(in srgb, var(--primary-color, #1f77b4) 14%, var(--background-color, #ffffff));
        --zero-bg: var(--secondary-background-color, #f5f5f5);
        --zero-fg: color-mix(in srgb, var(--text-color, #1d2939) 52%, var(--background-color, #ffffff));
    }
    html[data-theme="dark"],
    html[data-theme="dark"] .stApp,
    .stApp[data-theme="dark"] {
        --ink: var(--text-color, var(--textColor, #f2f4f7));
        --muted: color-mix(in srgb, var(--text-color, #f2f4f7) 72%, var(--background-color, #0e1117));
        --soft: color-mix(in srgb, var(--text-color, #f2f4f7) 88%, var(--background-color, #0e1117));
        --surface: var(--background-color, #0e1117);
        --surface-2: var(--secondary-background-color, #262730);
        --line: color-mix(in srgb, var(--text-color, #f2f4f7) 20%, var(--background-color, #0e1117));
        --accent: var(--primary-color, var(--primaryColor, #8ecbff));
        --result-bg: color-mix(in srgb, var(--primary-color, #8ecbff) 18%, var(--background-color, #0e1117));
        --zero-bg: var(--secondary-background-color, #262730);
        --zero-fg: color-mix(in srgb, var(--text-color, #f2f4f7) 58%, var(--background-color, #0e1117));
    }
    header[data-testid="stHeader"] { display: none !important; }
    .stAppDeployButton { display: none !important; }
    .block-container { padding-top: 1.6rem; padding-bottom: 2rem; max-width: 1000px; }
    h1 { font-size: 1.75rem !important; letter-spacing: 0.02em; margin-bottom: 0.1rem !important; }
    .title-row {
        display: flex; align-items: baseline; gap: 16px; flex-wrap: wrap;
        margin: 0 0 1rem;
    }
    .title-row .app-title {
        font-size: 1.75rem; font-weight: 700; letter-spacing: 0.02em;
        color: var(--ink); margin: 0; line-height: 1.3;
    }
    .ver-meta { color: var(--muted); font-size: 1rem; font-weight: 500; }
    .ver-chip {
        display: inline-block; background: var(--surface-2); color: var(--soft);
        border-radius: 999px; padding: 3px 11px; font-size: 0.92rem; font-weight: 700;
    }
    .manual-head {
        font-size: 1.28rem; font-weight: 600; color: var(--ink);
        margin: 0.15rem 0 0.65rem;
    }
    [data-testid="stTabs"] {
        margin-top: 0.15rem;
    }
    [data-testid="stTabs"] [role="tablist"] {
        gap: 6px !important;
        border-bottom: 1px solid var(--line);
        padding: 0 2px;
        align-items: flex-end !important;
    }
    [data-testid="stTab"] {
        font-size: 1.08rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        padding: 0.72rem 1.45rem !important;
        margin: 0 0 -1px 0 !important;
        background: var(--surface-2) !important;
        color: var(--muted) !important;
        border: 1px solid var(--line) !important;
        border-bottom-color: transparent !important;
        border-radius: 10px 10px 0 0 !important;
        cursor: pointer;
    }
    [data-testid="stTab"] [data-testid="stMarkdownContainer"] p {
        font-size: 1.08rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        margin: 0 !important;
        color: inherit !important;
    }
    [data-testid="stTab"]:hover {
        background: var(--surface) !important;
        color: var(--soft) !important;
    }
    [data-testid="stTab"][aria-selected="true"],
    [data-testid="stTab"][data-selected="true"] {
        background: var(--surface) !important;
        color: var(--ink) !important;
        border-bottom-color: var(--surface) !important;
        font-weight: 700 !important;
        position: relative;
        z-index: 1;
    }
    [data-testid="stTab"][aria-selected="true"] [data-testid="stMarkdownContainer"] p,
    [data-testid="stTab"][data-selected="true"] [data-testid="stMarkdownContainer"] p {
        font-weight: 700 !important;
        color: inherit !important;
    }
    [data-testid="stTab"] .react-aria-SelectionIndicator {
        display: none !important;
    }
    .hist-card {
        background: var(--surface-2); border: 1px solid var(--line);
        border-radius: 8px; padding: 10px 12px; margin-bottom: 10px;
    }
    .hist-ver { font-weight: 700; font-size: 0.9rem; color: var(--ink); }
    .hist-date { color: var(--muted); font-size: 0.78rem; font-weight: 500; margin-left: 6px; }
    .hist-card ul { margin: 6px 0 0 1.15rem; padding: 0; color: var(--soft); font-size: 0.82rem; }
    .hist-card li { margin: 3px 0; }
    .slot-stage {
        background: linear-gradient(165deg, #4a3124 0%, #2c1b12 100%);
        border-radius: 16px; padding: 16px 12px 14px; margin: 0 0 8px;
        box-shadow: 0 8px 24px rgba(44, 27, 18, 0.18);
    }
    .slot-grid {
        display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px;
    }
    .slot-label {
        color: #f3d2b3; font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.12em; text-align: center; margin-bottom: 8px;
    }
    .slot-reel {
        text-align: center; background: #fff7ed; border: 1px solid #f5d0b0;
        border-radius: 12px; padding: 18px 8px 14px; min-height: 118px;
        overflow: hidden; position: relative;
    }
    .slot-reel.spinning {
        padding: 0; min-height: 0; border-color: #e08a3a;
        box-shadow: inset 0 0 0 2px rgba(224, 138, 58, 0.2);
    }
    .slot-reel.locked { border-color: #c2410c; background: #fff; }
    .slot-window { height: 128px; overflow: hidden; position: relative; }
    .slot-window::before, .slot-window::after {
        content: ''; position: absolute; left: 0; right: 0; height: 28px;
        z-index: 1; pointer-events: none;
    }
    .slot-window::before { top: 0; background: linear-gradient(#fff7ed, transparent); }
    .slot-window::after { bottom: 0; background: linear-gradient(transparent, #fff7ed); }
    .slot-track {
        animation-name: slot-spin; animation-timing-function: linear;
        animation-iteration-count: infinite; will-change: transform;
        filter: blur(0.5px); animation-duration: 0.72s;
    }
    .slot-track.speed-origin { animation-duration: 0.72s; }
    .slot-track.speed-roast { animation-duration: 0.36s; }
    .slot-track.speed-brew { animation-duration: 0.45s; }
    .slot-track.slow { filter: blur(0.25px); }
    .slot-track.speed-origin.slow { animation-duration: 1.05s; }
    .slot-track.speed-roast.slow { animation-duration: 0.62s; }
    .slot-track.speed-brew.slow { animation-duration: 0.78s; }
    .slot-cell {
        height: 128px; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
    }
    @keyframes slot-spin {
        from { transform: translateY(0); }
        to { transform: translateY(-50%); }
    }
    .slot-emoji { font-size: 2rem; line-height: 1.2; }
    .slot-name { font-weight: 700; font-size: 1.05rem; margin-top: 8px; color: #1d2939; }
    .slot-cell .slot-name { margin-top: 6px; }
    .slot-sub { color: #9a6b3d; font-size: 0.78rem; margin-top: 2px; }
    .gacha-card {
        background: color-mix(in srgb, #c2410c 8%, var(--surface));
        border: 1px solid color-mix(in srgb, #c2410c 28%, var(--line));
        border-radius: 12px; padding: 14px 16px;
        margin-top: 12px;
    }
    .gacha-card.rare {
        border-color: color-mix(in srgb, #e8b84a 70%, var(--line));
        background: color-mix(in srgb, #e8b84a 16%, var(--surface));
    }
    .gacha-title { font-weight: 700; font-size: 1.05rem; color: var(--ink); }
    .gacha-body { color: var(--soft); font-size: 0.9rem; margin-top: 6px; line-height: 1.55; }
    .mem-stat { color: var(--muted); font-size: 0.88rem; }
    .st-key-mem_board {
        background: linear-gradient(165deg, #1f5136 0%, #143325 100%) !important;
        border-radius: 16px !important;
        padding: 12px 10px !important;
        box-shadow: 0 8px 24px rgba(20, 51, 37, 0.28);
    }
    .st-key-mem_board [data-testid="stHorizontalBlock"] { gap: 8px !important; }
    .st-key-mem_board [data-testid="stColumn"],
    .st-key-mem_board [data-testid="stColumn"] > div {
        position: relative !important;
    }
    .st-key-mem_board [data-testid="stMarkdownContainer"] { margin-bottom: 0 !important; }
    .st-key-mem_board [data-testid="stElementToolbar"] { display: none !important; }
    .pc, .pc * { pointer-events: none !important; }
    .st-key-mem_board [class*="st-key-memflip_"] {
        position: absolute !important;
        inset: 0 !important;
        z-index: 20 !important;
        min-height: 0 !important;
    }
    .st-key-mem_board [class*="st-key-memflip_"] [data-testid="stButton"],
    .st-key-mem_board [class*="st-key-memflip_"] button {
        position: absolute !important;
        inset: 0 !important;
        width: 100% !important;
        height: 100% !important;
        min-height: 0 !important;
        margin: 0 !important;
        z-index: 21 !important;
        cursor: pointer !important;
        pointer-events: auto !important;
    }
    .st-key-mem_board [class*="st-key-memflip_"] button {
        opacity: 0.01 !important;
        border: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    .st-key-mem_board [class*="st-key-memflip_"] button:disabled {
        cursor: default !important;
        pointer-events: none !important;
    }
    .st-key-mem_board [data-testid="stColumn"]:hover .pc.back {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.35);
    }
    .pc {
        aspect-ratio: 5 / 7;
        width: min(100%, 122px);
        margin: 0 auto;
        border-radius: 12px;
        position: relative;
        overflow: hidden;
        box-shadow:
            0 1px 0 rgba(255, 255, 255, 0.35) inset,
            0 2px 0 #0b1f14,
            0 8px 16px rgba(0, 0, 0, 0.32);
        transition: transform 0.12s ease, box-shadow 0.12s ease;
        user-select: none;
    }
    .pc.back {
        background:
            repeating-linear-gradient(
                45deg, #7a2e12 0 5px, #4e1a0c 5px 10px
            );
        border: 3px solid #f4ead8;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .pc-back-inner {
        width: 78%;
        height: 84%;
        border: 2px solid #e8c9a0;
        border-radius: 8px;
        background: linear-gradient(165deg, #9a4a1c 0%, #4a1c0c 100%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        color: #f8e3c8;
    }
    .pc-back-logo { font-size: 1.7rem; line-height: 1; }
    .pc-back-mark {
        margin-top: 6px;
        font-size: 0.62rem;
        font-weight: 700;
        letter-spacing: 0.14em;
    }
    .pc.face {
        background: linear-gradient(180deg, #fffefb 0%, #fff6ea 100%);
        border: 2px solid #c4a574;
    }
    .pc.matched { border-color: #d4a017; box-shadow: 0 0 0 2px rgba(232, 184, 74, 0.5); }
    .pc-index {
        position: absolute;
        top: 5px;
        left: 7px;
        font-size: 0.95rem;
        line-height: 1.1;
        color: #7a2e12;
    }
    .pc-index.br {
        top: auto;
        left: auto;
        bottom: 5px;
        right: 7px;
        transform: rotate(180deg);
    }
    .pc-suit {
        font-size: 2rem;
        text-align: center;
        padding-top: 30%;
        line-height: 1;
    }
    .pc-rank {
        text-align: center;
        font-weight: 700;
        font-size: 0.72rem;
        margin-top: 6px;
        color: #1d2939;
        letter-spacing: 0.02em;
    }
    .col-head, .rate-line, .rate-chip, .hint { white-space: nowrap; }
    h5.section-title { margin-top: 1.6rem; margin-bottom: 0.35rem; font-size: 1.05rem; }
    div[role="radiogroup"] label, div[role="radiogroup"] p { white-space: nowrap !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0.55rem 0.75rem !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div { gap: 0.4rem !important; }
    .hint { color: var(--muted); font-size: 0.9rem; }
    .out-label { color: var(--muted); font-size: 0.75rem; margin-bottom: 2px; }
    .out-value { font-size: 1.2rem; font-weight: 600; color: var(--ink); padding: 4px 0 0; }
    .col-head {
        color: var(--muted); font-size: 0.75rem; font-weight: 600;
        letter-spacing: 0.02em; padding: 0 0 6px 2px;
    }
    .cell-out {
        font-size: 1.15rem; font-weight: 600; color: var(--ink);
        padding-top: 0.55rem; white-space: nowrap;
    }
    .cell-num { color: var(--muted); font-size: 0.85rem; padding-top: 0.7rem; }
    .rate-chip {
        display: inline-block; background: var(--surface-2); color: var(--soft);
        border-radius: 999px; padding: 4px 10px; font-size: 0.85rem; font-weight: 600;
    }
    .result-card {
        background: var(--result-bg); border-left: 4px solid var(--accent);
        border-radius: 8px; padding: 10px 14px;
    }
    .result-card.zero { background: var(--zero-bg); border-left-color: var(--zero-fg); }
    .result-label { color: var(--muted); font-size: 0.95rem; margin-bottom: 6px; }
    .result-value { font-size: 1.75rem; font-weight: 700; color: var(--accent); }
    .result-card.zero .result-value { color: var(--zero-fg); }
    .result-sub { color: var(--soft); font-size: 0.85rem; margin-top: 8px; }
    table.result-table {
        width: 100%; border-collapse: collapse; font-size: 0.95rem;
        color: var(--ink);
    }
    table.result-table th {
        text-align: left; color: var(--muted); font-weight: 600;
        font-size: 0.75rem; padding: 6px 8px;
        border-bottom: 1px solid var(--line);
    }
    table.result-table td {
        padding: 7px 8px; border-bottom: 1px solid var(--line);
        vertical-align: middle;
    }
    table.result-table td.rate { color: var(--soft); }
    table.result-table td.pt {
        font-weight: 700; font-size: 1.2rem; text-align: right;
        color: var(--accent); font-variant-numeric: tabular-nums;
    }
    table.result-table tr.hl td { background: var(--result-bg); }
    table.look-table td.pt { font-size: 1.05rem; font-weight: 600; }
    div[data-testid="stMetricValue"] { font-size: 1.35rem; }
    /* 金額は手入力が主。±ボタンを消して欄を狭くする */
    div[data-testid="stNumberInput"] button { display: none !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0.6rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit のライト／ダークに合わせて、カスタム文字色を上書きする
_theme_is_dark = False
try:
    _theme_is_dark = str(getattr(st.context.theme, 'type', '') or '').lower() == 'dark'
except Exception:
    _theme_is_dark = False
if _theme_is_dark:
    st.markdown(
        """
        <style>
        :root, .stApp {
            --ink: var(--text-color, #f2f4f7);
            --muted: color-mix(in srgb, var(--text-color, #f2f4f7) 72%, var(--background-color, #0e1117));
            --soft: color-mix(in srgb, var(--text-color, #f2f4f7) 88%, var(--background-color, #0e1117));
            --surface: var(--background-color, #0e1117);
            --surface-2: var(--secondary-background-color, #262730);
            --line: color-mix(in srgb, var(--text-color, #f2f4f7) 20%, var(--background-color, #0e1117));
            --accent: var(--primary-color, #8ecbff);
            --result-bg: color-mix(in srgb, var(--primary-color, #8ecbff) 18%, var(--background-color, #0e1117));
            --zero-bg: var(--secondary-background-color, #262730);
            --zero-fg: color-mix(in srgb, var(--text-color, #f2f4f7) 58%, var(--background-color, #0e1117));
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def as_amount(value):
    """入力欄の空値を 0 として扱う（計算式には渡す前の正規化のみ）"""
    if value in (None, ''):
        return 0
    try:
        return int(Decimal(str(value)))
    except Exception:
        return 0


def calc_beans_price(tax_included):
    """ビーンズクラブ割引後価格。切り捨て。"""
    return math.floor((Decimal(tax_included) * Decimal(beans_club)))


def calc_unit_point(price_for_calc, tax, rank_per):
    """1個あたりの商品ポイント。受注設定の既存式。"""
    return math.floor(int((Decimal(price_for_calc) / Decimal(1 + tax)) * Decimal(rank_per)))


def calc_tax_excluded_order(price_for_calc, tax):
    """受注設定の税抜。既存式。"""
    return math.floor(int(Decimal(price_for_calc) / Decimal(1 + tax)))


def calc_line_points(unit_point, amount):
    """行の商品ポイント（利用ポイント按分前）"""
    return Decimal(unit_point) * Decimal(amount)


def calc_adjusted_points(price_sum, used_points, unit_point, amount):
    """利用ポイント按分後の付与。受注設定の既存式。"""
    return math.floor(
        int(
            (((Decimal(price_sum) - Decimal(used_points)) / Decimal(price_sum)) * Decimal(unit_point))
        )
        * Decimal(amount)
    )


def resolve_rank_per(rank, event_mode, multiplier, fixed_rate_percent):
    """
    適用還元率を決める。
    通常・倍率は従来どおりランク分岐。還元率指定だけ全ランク共通。
    """
    d, g, s, w = diamond, gold, silver, white
    if event_mode == '倍率' and multiplier != 1:
        d = 0.03 * multiplier
        g = 0.02 * multiplier
        s = 0.01 * multiplier
        w = 0.01 * multiplier

    if rank == 'ダイヤモンド会員':
        rank_per = d
    elif rank == 'ゴールド会員':
        rank_per = g
    else:
        rank_per = w

    if event_mode == '還元率':
        rank_per = fixed_rate_percent / 100

    return rank_per


def format_yen(value):
    return f'{int(value):,}'


def format_pt(value):
    return f'{int(value):,}'


def render_result_card(total_points, applied_label, used_points, pre_total):
    is_zero = int(total_points) <= 0
    klass = 'result-card zero' if is_zero else 'result-card'
    color_note = ''
    if used_points:
        color_note = (
            f'<div class="result-sub">利用前 {format_pt(pre_total)}pt　／　'
            f'利用 {format_pt(used_points)}pt を按分</div>'
        )
    st.markdown(
        f"""
        <div class="{klass}">
            <div class="result-label">合計ポイント付与数</div>
            <div class="result-value">{format_pt(total_points)}pt</div>
            <div class="result-sub">{applied_label}</div>
            {color_note}
        </div>
        """,
        unsafe_allow_html=True,
    )


def init_order_rows():
    if 'row_ids' not in st.session_state:
        st.session_state.row_ids = [0]
        st.session_state.next_row_id = 1
        st.session_state['tax_0'] = 0.08
        st.session_state['qty_0'] = 1
        st.session_state['beans_ok_0'] = True
    if 'fixed_rate_pct' not in st.session_state:
        st.session_state.fixed_rate_pct = 5.0


def add_order_row():
    last_id = st.session_state.row_ids[-1]
    new_id = st.session_state.next_row_id
    last_tax = st.session_state.get(f'tax_{last_id}', 0.08)
    st.session_state[f'tax_{new_id}'] = last_tax
    st.session_state[f'qty_{new_id}'] = 1
    st.session_state[f'beans_ok_{new_id}'] = True
    st.session_state.row_ids.append(new_id)
    st.session_state.next_row_id += 1


def remove_order_row(row_id):
    if len(st.session_state.row_ids) <= 1:
        return
    st.session_state.row_ids = [x for x in st.session_state.row_ids if x != row_id]


def on_beans_member_toggle():
    """会員スイッチを入れたら、商品の対象はすべてチェックする。"""
    if st.session_state.get('beans_all'):
        for row_id in st.session_state.get('row_ids', [0]):
            st.session_state[f'beans_ok_{row_id}'] = True


def apply_rate_preset():
    preset = st.session_state.get('rate_preset')
    if preset is not None:
        st.session_state.fixed_rate_pct = float(preset)


def apply_product_rate_preset():
    preset = st.session_state.get('product_rate_preset')
    if preset is not None:
        st.session_state.product_fixed_rate_pct = float(preset)


def calc_product_tab_points(tax_excluded_price, rate):
    """商品設定の付与。既存式（税抜 × 率を切り捨て）。"""
    return int(math.floor(tax_excluded_price * Decimal(rate)))


def render_result_table(rows, highlight_last=False):
    """rows: (名前, 還元率の表示, ポイント数)"""
    body = []
    last = len(rows) - 1
    for i, (name, rate_label, points) in enumerate(rows):
        klass = ' class="hl"' if highlight_last and i == last else ''
        body.append(
            f'<tr{klass}><td>{name}</td>'
            f'<td class="rate">{rate_label}</td>'
            f'<td class="pt">{format_pt(points)}pt</td></tr>'
        )
    st.markdown(
        '<table class="result-table">'
        '<thead><tr><th>対象</th><th>還元率</th><th style="text-align:right;">付与</th></tr></thead>'
        f'<tbody>{"".join(body)}</tbody></table>',
        unsafe_allow_html=True,
    )


def render_look_table(rows):
    """rows: (還元率の表示, ポイント数)"""
    body = ''.join(
        f'<tr><td class="rate">{rate_label}</td>'
        f'<td class="pt">{format_pt(points)}pt</td></tr>'
        for rate_label, points in rows
    )
    st.markdown(
        '<table class="result-table look-table">'
        '<thead><tr><th>還元率</th><th style="text-align:right;">付与</th></tr></thead>'
        f'<tbody>{body}</tbody></table>',
        unsafe_allow_html=True,
    )


def render_order_tab():
    init_order_rows()

    with st.container(border=True):
        c1, c2 = st.columns([1.4, 1.2])
        with c1:
            rank = st.selectbox(
                '会員ランク',
                ['シルバー会員', 'ゴールド会員', 'ダイヤモンド会員', 'ホワイト会員'],
            )
        with c2:
            beans_member = st.toggle(
                'ビーンズクラブ会員',
                key='beans_all',
                on_change=on_beans_member_toggle,
                help='会員のとき、下の「対象」にチェックした商品だけ税込×0.7（切り捨て）します。',
            )
        event_mode = st.radio(
            'イベント',
            options=['なし', '倍率', '還元率'],
            index=0,
            horizontal=True,
            key='event_mode',
            help='倍率はランク還元率に掛けます。還元率は全ランク共通の付与率です。',
        )

        multiplier = 1
        fixed_rate = 5.0
        if event_mode == '倍率':
            multiplier = st.pills(
                'ポイント倍率',
                options=EVENT_MULTIPLIER_CHOICES,
                default=2,
                key='multiplier_pills',
            )
            if multiplier is None:
                multiplier = 2
        elif event_mode == '還元率':
            p1, p2 = st.columns([2.4, 1])
            with p1:
                st.pills(
                    '還元率',
                    options=EVENT_RATE_CHOICES,
                    key='rate_preset',
                    on_change=apply_rate_preset,
                )
            with p2:
                fixed_rate = st.number_input(
                    '還元率（%）',
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    format='%.1f',
                    key='fixed_rate_pct',
                    help='2〜20%が目安。それ以外の数値もそのまま反映します。',
                )

    rank_per = resolve_rank_per(rank, event_mode, multiplier, fixed_rate)

    if event_mode == '倍率':
        applied_label = f'{rank}　{rank_per * 100:.2f}%（基本率 × {multiplier}倍）'
    elif event_mode == '還元率':
        applied_label = f'全会員共通　{rank_per * 100:.2f}%'
    else:
        applied_label = f'{rank}　{rank_per * 100:.2f}%'
    if beans_member:
        applied_label += '　／　ビーンズクラブ会員'

    st.markdown(
        f'<div class="rate-line">'
        f'<span class="rate-chip">適用還元率　{rank_per * 100:.2f}%</span>'
        f'<span class="hint" style="margin-left:10px;">{applied_label}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<h5 class="section-title">商品</h5>', unsafe_allow_html=True)
    if beans_member:
        st.caption('対象外の商品は「対象」のチェックを外してください。追加行の税率は直前の行を引き継ぎます。')
    else:
        st.caption('追加した行の税率は直前の行を引き継ぎます。')

    if beans_member:
        widths = [0.35, 0.9, 1.35, 0.75, 0.7, 1.0, 1.0, 1.05, 0.4]
        headers = ['', '税率', '税込', '数量', '対象', '割引後', '税抜', 'ポイント', '']
    else:
        widths = [0.4, 1.1, 1.6, 0.9, 1.2, 1.25, 0.45]
        headers = ['', '税率', '税込', '数量', '税抜', 'ポイント', '']

    head = st.columns(widths)
    for col, label in zip(head, headers):
        col.markdown(f'<div class="col-head">{label}</div>', unsafe_allow_html=True)

    lines = []
    for i, row_id in enumerate(st.session_state.row_ids, start=1):
        if f'beans_ok_{row_id}' not in st.session_state:
            st.session_state[f'beans_ok_{row_id}'] = True
        cols = st.columns(widths)
        with cols[0]:
            st.markdown(f'<div class="cell-num">{i}</div>', unsafe_allow_html=True)
        with cols[1]:
            tax = st.selectbox(
                '税率',
                [0.08, 0.1],
                format_func=lambda x: '8%' if x == 0.08 else '10%',
                key=f'tax_{row_id}',
                label_visibility='collapsed',
            )
        with cols[2]:
            price = st.text_input(
                '税込価格',
                value='',
                placeholder='例: 1100',
                key=f'price_{row_id}',
                label_visibility='collapsed',
            )
        with cols[3]:
            amount = st.number_input(
                '数量',
                min_value=0,
                step=1,
                format='%d',
                key=f'qty_{row_id}',
                label_visibility='collapsed',
            )

        item_eligible = True
        if beans_member:
            with cols[4]:
                item_eligible = st.checkbox(
                    '対象',
                    key=f'beans_ok_{row_id}',
                    help='対象外の商品はチェックを外します',
                    label_visibility='collapsed',
                )

        apply_beans = beans_member and item_eligible
        price_n = as_amount(price)
        amount_n = as_amount(amount)
        discounted = None
        tax_excluded = 0
        unit_point = 0
        line_point = Decimal(0)

        try:
            if apply_beans:
                discounted = calc_beans_price(price_n)
                unit_point = calc_unit_point(discounted, tax, rank_per)
                tax_excluded = calc_tax_excluded_order(discounted, tax)
            else:
                unit_point = calc_unit_point(price_n, tax, rank_per)
                tax_excluded = calc_tax_excluded_order(price_n, tax)
            line_point = calc_line_points(unit_point, amount_n)
        except Exception:
            discounted = None
            tax_excluded = 0
            unit_point = 0
            line_point = Decimal(0)

        if beans_member:
            with cols[5]:
                if apply_beans and discounted is not None:
                    shown = format_yen(discounted)
                else:
                    shown = '—'
                st.markdown(f'<div class="cell-out">{shown}</div>', unsafe_allow_html=True)
            with cols[6]:
                st.markdown(
                    f'<div class="cell-out">{format_yen(tax_excluded)}</div>',
                    unsafe_allow_html=True,
                )
            with cols[7]:
                st.markdown(
                    f'<div class="cell-out">{format_pt(line_point)}</div>',
                    unsafe_allow_html=True,
                )
            with cols[8]:
                st.button(
                    '×',
                    key=f'del_{row_id}',
                    disabled=len(st.session_state.row_ids) <= 1,
                    on_click=remove_order_row,
                    args=(row_id,),
                    help='この行を削除',
                )
        else:
            with cols[4]:
                st.markdown(
                    f'<div class="cell-out">{format_yen(tax_excluded)}</div>',
                    unsafe_allow_html=True,
                )
            with cols[5]:
                st.markdown(
                    f'<div class="cell-out">{format_pt(line_point)}</div>',
                    unsafe_allow_html=True,
                )
            with cols[6]:
                st.button(
                    '×',
                    key=f'del_{row_id}',
                    disabled=len(st.session_state.row_ids) <= 1,
                    on_click=remove_order_row,
                    args=(row_id,),
                    help='この行を削除',
                )

        lines.append(
            {
                'price': int(price_n),
                'amount': amount_n,
                'unit_point': unit_point,
                'line_point': line_point,
            }
        )

    add_col, count_col, _ = st.columns([1.2, 1.2, 3])
    with add_col:
        st.button(
            '商品を追加',
            on_click=add_order_row,
            use_container_width=True,
        )
    with count_col:
        st.caption(f'{len(st.session_state.row_ids)} 商品')

    st.markdown('<h5 class="section-title">付与結果</h5>', unsafe_allow_html=True)
    used_col, result_col = st.columns([1, 2])
    with used_col:
        used_points = st.number_input(
            '利用ポイント',
            min_value=0,
            step=1,
            format='%d',
            value=0,
            help='注文全体の利用ポイント。各商品の付与を税込単価比で按分します。',
        )

    pre_total = sum(int(line['line_point']) for line in lines)
    # 税込合計は従来どおり単価の足し算（数量は分母に入れない）
    price_sum = sum(line['price'] for line in lines)

    # 1行目が0ptでも按分する。分母が0のときだけ計算しない
    can_allocate = price_sum > 0
    if can_allocate:
        total_points = sum(
            int(calc_adjusted_points(price_sum, used_points, line['unit_point'], line['amount']))
            for line in lines
        )
    else:
        total_points = 0

    with result_col:
        render_result_card(total_points, applied_label, used_points, pre_total)

    if can_allocate and len(lines) > 1:
        st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
        with st.expander('商品ごとの付与（按分後）', expanded=False):
            for i, line in enumerate(lines, start=1):
                adjusted = calc_adjusted_points(
                    price_sum, used_points, line['unit_point'], line['amount']
                )
                st.write(
                    f'商品{i}　{format_pt(adjusted)}pt'
                    f'（利用前 {format_pt(line["line_point"])}pt）'
                )


def render_product_tab():
    if 'product_fixed_rate_pct' not in st.session_state:
        st.session_state.product_fixed_rate_pct = 5.0

    with st.container(border=True):
        c1, c2, c3 = st.columns([1.4, 1.1, 1.5])
        with c1:
            price = st.text_input(
                '税込金額',
                value='',
                placeholder='例: 1100',
                key='product_price',
            )
        with c2:
            tax = st.selectbox(
                '税率',
                [0.08, 0.1],
                format_func=lambda x: '8%' if x == 0.08 else '10%',
                index=0,
                key='product_tax',
            )
        with c3:
            price_n = as_amount(price)
            # 商品設定の税抜。既存式（受注設定とは切り方が異なる）
            tax_excluded_price = Decimal(math.floor(Decimal(price_n) / Decimal(1 + tax)))
            st.markdown(
                f"""
                <div class="out-label">税抜価格</div>
                <div class="out-value">{format_yen(tax_excluded_price)}</div>
                """,
                unsafe_allow_html=True,
            )

        event_mode = st.radio(
            'イベント',
            options=['なし', '倍率', '還元率'],
            index=0,
            horizontal=True,
            key='product_event_mode',
            help='倍率はランク還元率に掛けます。還元率は全ランク共通の付与率です。',
        )
        multiplier = 1
        fixed_rate = 5.0
        if event_mode == '倍率':
            multiplier = st.pills(
                'ポイント倍率',
                options=EVENT_MULTIPLIER_CHOICES,
                default=2,
                key='product_multiplier_pills',
            )
            if multiplier is None:
                multiplier = 2
        elif event_mode == '還元率':
            p1, p2 = st.columns([2.4, 1])
            with p1:
                st.pills(
                    'よく使う還元率',
                    options=EVENT_RATE_CHOICES,
                    key='product_rate_preset',
                    on_change=apply_product_rate_preset,
                )
            with p2:
                fixed_rate = st.number_input(
                    '還元率（%）',
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    format='%.1f',
                    key='product_fixed_rate_pct',
                    help='ボタンに無い率も、ここに入力すると反映します。',
                )

    w, s, g, d = white, silver, gold, diamond
    if event_mode == '倍率' and multiplier != 1:
        w = 0.01 * multiplier
        s = 0.01 * multiplier
        g = 0.02 * multiplier
        d = 0.03 * multiplier

    st.markdown('##### 付与結果')

    if event_mode == '還元率':
        common_rate = fixed_rate / 100
        points = calc_product_tab_points(tax_excluded_price, common_rate)
        render_result_card(
            points,
            f'全会員共通　{common_rate * 100:.2f}%',
            used_points=0,
            pre_total=points,
        )
    else:
        if event_mode == '倍率':
            rate_note = lambda base, rate: f'{rate * 100:.2f}%（{base}% × {multiplier}倍）'
            rows = [
                ('ホワイト会員', rate_note(1, w), calc_product_tab_points(tax_excluded_price, w)),
                ('シルバー会員', rate_note(1, s), calc_product_tab_points(tax_excluded_price, s)),
                ('ゴールド会員', rate_note(2, g), calc_product_tab_points(tax_excluded_price, g)),
                ('ダイヤモンド会員', rate_note(3, d), calc_product_tab_points(tax_excluded_price, d)),
            ]
        else:
            rows = [
                ('ホワイト会員', '1.00%', calc_product_tab_points(tax_excluded_price, w)),
                ('シルバー会員', '1.00%', calc_product_tab_points(tax_excluded_price, s)),
                ('ゴールド会員', '2.00%', calc_product_tab_points(tax_excluded_price, g)),
                ('ダイヤモンド会員', '3.00%', calc_product_tab_points(tax_excluded_price, d)),
            ]
        render_result_table(rows, highlight_last=True)

    st.markdown('##### 還元率の早見')
    look_rows = [
        (f'{label}%', calc_product_tab_points(tax_excluded_price, rate))
        for label, rate in PRODUCT_EVENT_RATES
    ]
    mid = (len(look_rows) + 1) // 2
    col_a, col_b = st.columns(2)
    with col_a:
        render_look_table(look_rows[:mid])
    with col_b:
        render_look_table(look_rows[mid:])


def render_manual_tab():
    st.markdown(
        f'<div class="manual-head">計算方法　'
        f'<span class="ver-chip">Ver.{APP_VERSION}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('''
このツールは、注文や企画の付与ポイントを手元で検算するためのものです。
端数はすべて**切り捨て**です。

---

### 画面の使い分け

| タブ | 用途 |
|---|---|
| 受注設定 | 複数商品・利用ポイント・ビーンズクラブまで含めた、その注文の付与 |
| 商品設定 | 税込1件だけで、ランク別・倍率・還元率・早見表を見る |
| 変更履歴 | このツールのバージョンごとの変更 |
| コーヒーブレイク | 産地神経衰弱と今日の一杯ルーレット |

---

### 会員ランクの基本還元率

| ランク | 通常の還元率 |
|---|---|
| ホワイト会員 | 1% |
| シルバー会員 | 1% |
| ゴールド会員 | 2% |
| ダイヤモンド会員 | 3% |

---

### イベント

**なし**  
上記の基本還元率のまま計算します。

**倍率**  
基本還元率に、選んだ倍率（2〜10、15、20）を掛けます。  
例: ゴールド 2% × 3倍 → 6%

**還元率**  
会員ランクは使いません。全会員同じ率です。  
よく使う率のボタンか、右の欄に任意の％を入れます。

---

### 受注設定の計算

1. 税込から税抜を出す（切り捨て）
2. 税抜に還元率を掛ける（切り捨て）→ 1個あたりのポイント
3. 数量を掛ける → その行の商品ポイント

```
税抜 = 切り捨て(税込 ÷ (1 + 税率))
1個のポイント = 切り捨て(税抜 × 還元率)
商品ポイント = 1個のポイント × 数量
```

税率は 8% または 10%。追加した行の税率は、直前の行を初期値にします。

#### ビーンズクラブ

上のスイッチは「この注文の人が会員か」です。

- 会員オフ … どの商品も通常価格で計算
- 会員オン … 行の「対象」にチェックがある商品だけ、税込を 0.7 倍（3割引き）してから税抜・ポイントを出します。切り捨てです
- 「対象」は最初すべてオン。対象外の商品だけチェックを外します

```
割引後 = 切り捨て(税込 × 0.7)
税抜・ポイントは、この割引後を税込の代わりに使う
```

#### 利用ポイントがあるとき

各行の「商品ポイント」は、まだポイントを使っていない数です。  
下の合計は、利用分を税込単価の比で按分して減らします。

```
税込合計 = 各行の税込単価の足し算（数量は入れない）
残率 = (税込合計 − 利用ポイント) ÷ 税込合計
各行の付与 = 切り捨て(残率 × その行の1個ポイント) × 数量
合計付与 = 各行の付与の足し算
```

1行目が 0pt でも、ほかの行があれば合計は出ます。  
税込がすべて空（合計 0）のときだけ、0pt のままです。

---

### 商品設定の計算

税込と税率だけ入れます。税抜の切り方は受注設定と少し違います。

```
税抜 = 切り捨て(税込 ÷ (1 + 税率))
付与 = 切り捨て(税抜 × 還元率)
```

イベントのなし／倍率／還元率の意味は受注設定と同じです。  
下の「還元率の早見」は、同じ税抜に 2%〜50%（ボタンと同じ率）を掛けた一覧です。  
ビーンズクラブと利用ポイントは、このタブにはありません。

---

### 計算例

税込 1,100円、税率 10%、ダイヤモンド会員、数量 1、利用なし。

```
税抜 = 切り捨て(1100 ÷ 1.1) = 1000
付与 = 切り捨て(1000 × 0.03) = 30pt
```

同じ条件で 200pt 使うと、

```
残率 = (1100 − 200) ÷ 1100
付与 = 切り捨て(残率 × 30) = 24pt
```

ビーンズクラブ対象なら、

```
割引後 = 切り捨て(1100 × 0.7) = 770
税抜・ポイントは 770 円から出す
```
''')


def render_history_tab():
    st.markdown(
        f'<div class="manual-head">変更履歴　'
        f'<span class="ver-chip">Ver.{APP_VERSION}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'''
<div class="hist-card">
  <div><span class="hist-ver">Ver.{APP_VERSION}</span><span class="hist-date">{APP_UPDATED}</span></div>
  <ul>
    <li>タブ構成（受注設定／商品設定／計算方法／変更履歴／コーヒーブレイク）</li>
    <li>商品行は必要なだけ追加</li>
    <li>イベントに「還元率」（全ランク同一）を追加。任意％も可</li>
    <li>倍率の選択肢に 15倍・20倍を追加</li>
    <li>ビーンズクラブは会員スイッチ＋行の対象チェック</li>
    <li>1行目が 0pt でも、ほかの行があれば合計を出す</li>
    <li>計算式・端数（切り捨て）は Ver.01 と同じ</li>
    <li>コーヒーブレイク（産地神経衰弱・今日の一杯ルーレット）</li>
    <li>今日の一杯ルーレットは、リールが回って順に止まる演出</li>
    <li>産地神経衰弱の札を、裏向き／表向きのカード型にした</li>
  </ul>
</div>
<div class="hist-card">
  <div><span class="hist-ver">Ver.01</span><span class="hist-date">初版</span></div>
  <ul>
    <li>サイドバーで受注設定／商品設定を切替</li>
    <li>商品は最大 10 件</li>
    <li>イベントはポイント倍率（1〜10）のみ</li>
    <li>ビーンズクラブは商品ごとに指定</li>
    <li>1行目が 0pt だと合計も 0</li>
  </ul>
</div>
        ''',
        unsafe_allow_html=True,
    )


PLAY_ORIGINS = [
    ('ケニア', '🍋', '柑橘とワインのような酸'),
    ('グアテマラ', '🍫', 'チョコレートとスパイス'),
    ('エチオピア', '🌸', '花と紅茶のような香り'),
    ('ブラジル', '🥜', 'ナッツと穏やかな甘み'),
    ('コロンビア', '🍎', 'りんごのような明るさ'),
    ('タンザニア', '🍓', 'ベリー系の酸と甘み'),
    ('インドネシア', '🌿', 'ハーブと大地のコク'),
    ('コスタリカ', '🍯', 'はちみつのような透明感'),
]
PLAY_ROASTS = [
    ('浅煎り', '◎', '酸が立つ'),
    ('中煎り', '○', 'バランス型'),
    ('中深煎り', '●', '甘みとコク'),
    ('深煎り', '◆', '苦みと余韻'),
]
PLAY_BREWS = [
    ('ハンドドリップ', '☕'),
    ('フレンチプレス', '🫖'),
    ('エスプレッソ', '🫘'),
    ('ネルドリップ', '🫖'),
    ('水出し', '🧊'),
]
PLAY_SECRETS = {
    ('ケニア', '浅煎り', 'ハンドドリップ'): ('部長の勝負豆', '朝の検算がはかどる一杯。柑橘が立つ。'),
    ('エチオピア', '浅煎り', 'ネルドリップ'): ('花の季節', '香りが先に来る。午後のひと息に。'),
    ('グアテマラ', '中煎り', 'フレンチプレス'): ('午後の定番', 'ココアっぽい。会議のあとに合う。'),
    ('ブラジル', '深煎り', 'エスプレッソ'): ('倉庫の休憩', '短く濃い。次の箱を開ける前に。'),
}


def _init_memory():
    deck = []
    for i, (name, emoji, note) in enumerate(PLAY_ORIGINS):
        for _ in range(2):
            deck.append({
                'pair': i,
                'name': name,
                'emoji': emoji,
                'note': note,
                'flipped': False,
                'matched': False,
            })
    random.shuffle(deck)
    st.session_state.play_deck = deck
    st.session_state.play_tries = 0
    st.session_state.play_matched = 0
    st.session_state.play_started = time.time()
    st.session_state.play_finished = None
    st.session_state.play_need_hide = False
    st.session_state.play_last_match = ''


def _memory_click(idx):
    deck = st.session_state.play_deck
    card = deck[idx]
    if card['matched'] or card['flipped'] or st.session_state.play_finished:
        return
    open_idxs = [i for i, c in enumerate(deck) if c['flipped'] and not c['matched']]
    if len(open_idxs) >= 2:
        return
    card['flipped'] = True
    open_idxs = [i for i, c in enumerate(deck) if c['flipped'] and not c['matched']]
    if len(open_idxs) != 2:
        return
    st.session_state.play_tries += 1
    a, b = open_idxs
    if deck[a]['pair'] == deck[b]['pair']:
        deck[a]['matched'] = True
        deck[b]['matched'] = True
        st.session_state.play_matched += 1
        st.session_state.play_last_match = f"{deck[a]['emoji']} {deck[a]['name']}　{deck[a]['note']}"
        if st.session_state.play_matched >= len(PLAY_ORIGINS):
            elapsed = int(time.time() - st.session_state.play_started)
            st.session_state.play_finished = elapsed
            best = st.session_state.get('play_best')
            if best is None or st.session_state.play_tries < best[0] or (
                st.session_state.play_tries == best[0] and elapsed < best[1]
            ):
                st.session_state.play_best = (st.session_state.play_tries, elapsed)
    else:
        st.session_state.play_need_hide = True


def _playing_card_html(card, state):
    """トランプ型の札。back / face / matched。"""
    if state == 'back':
        return (
            '<div class="pc back"><div class="pc-back-inner">'
            '<div class="pc-back-logo">☕</div>'
            '<div class="pc-back-mark">COFFEE</div>'
            '</div></div>'
        )
    klass = 'pc face matched' if state == 'matched' else 'pc face'
    return (
        f'<div class="{klass}">'
        f'<div class="pc-index">{card["emoji"]}</div>'
        f'<div class="pc-suit">{card["emoji"]}</div>'
        f'<div class="pc-rank">{card["name"]}</div>'
        f'<div class="pc-index br">{card["emoji"]}</div>'
        f'</div>'
    )


def render_memory_game():
    if 'play_deck' not in st.session_state:
        _init_memory()

    deck = st.session_state.play_deck
    if st.session_state.play_finished is None:
        elapsed = int(time.time() - st.session_state.play_started)
    else:
        elapsed = st.session_state.play_finished

    top_a, top_b, top_c = st.columns([1.2, 1, 1])
    with top_a:
        st.markdown(
            f'<div class="mem-stat">揃えた　'
            f'{st.session_state.play_matched} / {len(PLAY_ORIGINS)}</div>',
            unsafe_allow_html=True,
        )
    with top_b:
        st.markdown(
            f'<div class="mem-stat">手数　{st.session_state.play_tries}</div>',
            unsafe_allow_html=True,
        )
    with top_c:
        st.markdown(
            f'<div class="mem-stat">時間　{elapsed}秒</div>',
            unsafe_allow_html=True,
        )

    if st.session_state.play_finished is not None:
        best = st.session_state.get('play_best', (st.session_state.play_tries, elapsed))
        st.success(
            f'全部揃いました。{st.session_state.play_tries}手 / {elapsed}秒'
            f'　（自己ベスト {best[0]}手 / {best[1]}秒）'
        )
    elif st.session_state.play_last_match:
        st.caption(st.session_state.play_last_match)

    with st.container(key='mem_board'):
        for row in range(4):
            cols = st.columns(4)
            for col, idx in zip(cols, range(row * 4, row * 4 + 4)):
                card = deck[idx]
                if card['matched']:
                    state = 'matched'
                    disabled = True
                elif card['flipped']:
                    state = 'face'
                    disabled = True
                else:
                    state = 'back'
                    disabled = bool(st.session_state.play_finished)
                with col:
                    st.markdown(_playing_card_html(card, state), unsafe_allow_html=True)
                    st.button(
                        'めくる',
                        key=f'memflip_{idx}_{st.session_state.play_started}',
                        use_container_width=True,
                        disabled=disabled,
                        type='tertiary',
                        on_click=_memory_click,
                        args=(idx,),
                    )

    if st.button('もう一局', key='mem_reset'):
        _init_memory()
        st.rerun()

    if st.session_state.play_need_hide:
        time.sleep(0.7)
        for card in st.session_state.play_deck:
            if not card['matched']:
                card['flipped'] = False
        st.session_state.play_need_hide = False
        st.rerun()


def _init_roulette():
    if 'play_spin' not in st.session_state:
        st.session_state.play_spin = None
    if 'play_album' not in st.session_state:
        st.session_state.play_album = []
    if 'play_spins' not in st.session_state:
        st.session_state.play_spins = 0
    if 'play_reel_run' not in st.session_state:
        st.session_state.play_reel_run = False
        st.session_state.play_reel_stop = [True, True, True]
        st.session_state.play_reel_show = [0, 0, 0]


def _start_roulette():
    """結果を先に決め、3本のリールを回し始める。"""
    st.session_state.play_reel_run = True
    st.session_state.play_reel_stop = [False, False, False]
    st.session_state.play_spin = None
    st.session_state.play_reel_show = [
        random.randrange(len(PLAY_ORIGINS)),
        random.randrange(len(PLAY_ROASTS)),
        random.randrange(len(PLAY_BREWS)),
    ]


def _commit_roulette_result():
    """止まった3本から今日の一杯を確定する。"""
    origin = PLAY_ORIGINS[st.session_state.play_reel_show[0]]
    roast = PLAY_ROASTS[st.session_state.play_reel_show[1]]
    brew = PLAY_BREWS[st.session_state.play_reel_show[2]]
    secret = PLAY_SECRETS.get((origin[0], roast[0], brew[0]))
    st.session_state.play_spin = (origin, roast, brew, secret)
    st.session_state.play_reel_run = False
    st.session_state.play_spins += 1
    combo = f'{origin[0]} / {roast[0]} / {brew[0]}'
    if combo not in st.session_state.play_album:
        st.session_state.play_album.append(combo)


def _lock_next_roulette_reel():
    """左から1本ずつ止める。3本目で結果を確定する。"""
    stops = list(st.session_state.play_reel_stop)
    for i in range(3):
        if not stops[i]:
            stops[i] = True
            break
    st.session_state.play_reel_stop = stops
    if all(stops):
        _commit_roulette_result()


def _slot_reel_inner(items, index, spinning, speed_class='speed-origin'):
    """1本分のリールHTML。回っているときは全項目をループさせる。"""
    if spinning:
        cells = []
        for item in list(items) + list(items):
            cells.append(
                f'<div class="slot-cell">'
                f'<div class="slot-emoji">{item[1]}</div>'
                f'<div class="slot-name">{item[0]}</div>'
                f'</div>'
            )
        return (
            f'<div class="slot-reel spinning"><div class="slot-window">'
            f'<div class="slot-track {speed_class}">'
            f'{"".join(cells)}</div></div></div>'
        )
    if index is None:
        return (
            '<div class="slot-reel">'
            '<div class="slot-emoji"></div>'
            '<div class="slot-name">？</div>'
            '<div class="slot-sub">豆を挽いて回す</div></div>'
        )
    item = items[index]
    sub = item[2] if len(item) > 2 else '抽出'
    return (
        f'<div class="slot-reel locked">'
        f'<div class="slot-emoji">{item[1]}</div>'
        f'<div class="slot-name">{item[0]}</div>'
        f'<div class="slot-sub">{sub}</div></div>'
    )


def render_roulette():
    _init_roulette()
    running = st.session_state.play_reel_run
    stops = st.session_state.play_reel_stop
    shows = st.session_state.play_reel_show

    st.button(
        '豆を挽く',
        type='primary',
        key='play_spin_btn',
        disabled=running,
        on_click=_start_roulette,
        use_container_width=True,
    )

    idle = (not running) and st.session_state.play_spin is None
    slowing = running and any(stops)
    reels = [
        (PLAY_ORIGINS, shows[0], running and not stops[0], '産地', 'speed-origin'),
        (PLAY_ROASTS, shows[1], running and not stops[1], '焙煎', 'speed-roast'),
        (PLAY_BREWS, shows[2], running and not stops[2], '抽出', 'speed-brew'),
    ]
    stage_cols = []
    for items, idx, spinning, label, speed_class in reels:
        shown_idx = None if idle else idx
        if spinning and slowing:
            speed_class = f'{speed_class} slow'
        stage_cols.append(
            f'<div><div class="slot-label">{label}</div>'
            f'{_slot_reel_inner(items, shown_idx, spinning, speed_class)}</div>'
        )
    st.markdown(
        f'<div class="slot-stage"><div class="slot-grid">{"".join(stage_cols)}</div></div>',
        unsafe_allow_html=True,
    )

    spin = st.session_state.play_spin
    if spin is not None and not running:
        origin, roast, brew, secret = spin
        if secret:
            title, body = secret
            st.markdown(
                f'<div class="gacha-card rare"><div class="gacha-title">✦ {title}</div>'
                f'<div class="gacha-body">{body}</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="gacha-card"><div class="gacha-title">'
                f'今日の一杯　{origin[0]}の{roast[0]}</div>'
                f'<div class="gacha-body">{origin[2]}。{roast[2]}を、{brew[0]}で。</div></div>',
                unsafe_allow_html=True,
            )

    found = len(st.session_state.get('play_album', []))
    total = len(PLAY_ORIGINS) * len(PLAY_ROASTS) * len(PLAY_BREWS)
    st.caption(
        f'挽いた回数 {st.session_state.get("play_spins", 0)}　／　'
        f'見つけた組み合わせ {found} / {total}'
    )
    if st.session_state.get('play_album'):
        with st.expander('見つけた組み合わせ'):
            for item in reversed(st.session_state.play_album):
                mark = '✦ ' if tuple(item.split(' / ')) in PLAY_SECRETS else ''
                st.write(f'- {mark}{item}')

    if running and not all(stops):
        locked = sum(1 for stopped in stops if stopped)
        time.sleep(1.35 if locked == 0 else 0.55)
        _lock_next_roulette_reel()
        st.rerun()


def render_play_tab():
    st.markdown('<div class="manual-head">コーヒーブレイク</div>', unsafe_allow_html=True)
    mode = st.radio(
        '遊び',
        ['産地神経衰弱', '今日の一杯ルーレット'],
        horizontal=True,
        label_visibility='collapsed',
        key='play_mode',
    )
    if mode == '産地神経衰弱':
        render_memory_game()
    else:
        render_roulette()


st.markdown(
    f'''
    <div class="title-row">
      <div class="app-title">付与ポイント計算ツール</div>
      <span class="ver-meta">
        <span class="ver-chip">Ver.{APP_VERSION}</span>
        更新 {APP_UPDATED}
      </span>
    </div>
    ''',
    unsafe_allow_html=True,
)

tab_order, tab_product, tab_manual, tab_hist, tab_play = st.tabs(
    ['受注設定', '商品設定', '計算方法', '変更履歴', 'コーヒーブレイク']
)
with tab_order:
    render_order_tab()
with tab_product:
    render_product_tab()
with tab_manual:
    render_manual_tab()
with tab_hist:
    render_history_tab()
with tab_play:
    render_play_tab()

