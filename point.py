import math

import streamlit as st
from decimal import Decimal, getcontext

st.set_page_config(
    page_title='付与ポイント計算',
    page_icon='☕',
    layout='wide',
    initial_sidebar_state='collapsed',
)

getcontext().prec = 5

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
    header[data-testid="stHeader"] { display: none !important; }
    .stAppDeployButton { display: none !important; }
    .block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1000px; }
    h1 { font-size: 1.4rem !important; letter-spacing: 0.02em; margin-bottom: 0.1rem !important; }
    .col-head, .rate-line, .rate-chip, .hint { white-space: nowrap; }
    h5.section-title { margin-top: 1.6rem; margin-bottom: 0.35rem; font-size: 1.05rem; }
    div[role="radiogroup"] label, div[role="radiogroup"] p { white-space: nowrap !important; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0.55rem 0.75rem !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] > div { gap: 0.4rem !important; }
    .hint { color: #667085; font-size: 0.9rem; }
    .out-label { color: #667085; font-size: 0.75rem; margin-bottom: 2px; }
    .out-value { font-size: 1.2rem; font-weight: 600; color: #1d2939; padding: 4px 0 0; }
    .col-head {
        color: #667085; font-size: 0.75rem; font-weight: 600;
        letter-spacing: 0.02em; padding: 0 0 6px 2px;
    }
    .cell-out {
        font-size: 1.15rem; font-weight: 600; color: #1d2939;
        padding-top: 0.55rem; white-space: nowrap;
    }
    .cell-num { color: #98a2b3; font-size: 0.85rem; padding-top: 0.7rem; }
    .rate-chip {
        display: inline-block; background: #f2f4f7; color: #344054;
        border-radius: 999px; padding: 4px 10px; font-size: 0.85rem; font-weight: 600;
    }
    .result-card {
        background: #f0f7ff; border-left: 4px solid #1f77b4;
        border-radius: 8px; padding: 10px 14px;
    }
    .result-card.zero { background: #f5f5f5; border-left-color: #999; }
    .result-label { color: #667085; font-size: 0.95rem; margin-bottom: 6px; }
    .result-value { font-size: 1.75rem; font-weight: 700; color: #1f77b4; }
    .result-card.zero .result-value { color: #999; }
    .result-sub { color: #475467; font-size: 0.85rem; margin-top: 8px; }
    table.result-table {
        width: 100%; border-collapse: collapse; font-size: 0.95rem;
    }
    table.result-table th {
        text-align: left; color: #667085; font-weight: 600;
        font-size: 0.75rem; padding: 6px 8px;
        border-bottom: 1px solid #e4e7ec;
    }
    table.result-table td {
        padding: 7px 8px; border-bottom: 1px solid #f2f4f7;
        vertical-align: middle;
    }
    table.result-table td.rate { color: #475467; }
    table.result-table td.pt {
        font-weight: 700; font-size: 1.2rem; text-align: right;
        color: #1f77b4; font-variant-numeric: tabular-nums;
    }
    table.result-table tr.hl td { background: #f0f7ff; }
    table.look-table td.pt { font-size: 1.05rem; font-weight: 600; }
    div[data-testid="stMetricValue"] { font-size: 1.35rem; }
    /* 金額は手入力が主。±ボタンを消して欄を狭くする */
    div[data-testid="stNumberInput"] button { display: none !important; }
    div[data-testid="stHorizontalBlock"] { gap: 0.6rem; }
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
    st.markdown('''
このツールは、注文や企画の付与ポイントを手元で検算するためのものです。
端数はすべて**切り捨て**です。

---

### 画面の使い分け

| タブ | 用途 |
|---|---|
| 受注設定 | 複数商品・利用ポイント・ビーンズクラブまで含めた、その注文の付与 |
| 商品設定 | 税込1件だけで、ランク別・倍率・還元率・早見表を見る |

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


st.title('付与ポイント計算ツール')

tab_order, tab_product, tab_manual = st.tabs(['受注設定', '商品設定', '計算方法'])
with tab_order:
    render_order_tab()
with tab_product:
    render_product_tab()
with tab_manual:
    render_manual_tab()

