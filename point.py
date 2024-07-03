import fractions
import streamlit as st
import numpy as np
import pandas as pd
from decimal import Decimal, getcontext
from fractions import Fraction
import math

st.title('付与ポイント計算ツール')

getcontext().prec = 5

# col01, col02, col03 = st.beta_columns(3)
# with col01:
#     price01 = st.number_input('税込金額', 0, 999999, 0)
# with col02:
#     tax01 = st.selectbox('税率', [0.08, 0.1])
# with col03:
#     taxEx01_ = int(Decimal(price01)/(Decimal(1+tax01)))
#     taxEx01 = st.number_input(label='税抜価格', value=taxEx01_)
selected_item = st.sidebar.radio('使用機能を選んでください', ['受注設定', '商品設定'])

diamond = 0.03
gold = 0.02
silver = 0.01
white = 0.01

beans_club = 0.7

if selected_item == '受注設定':
    rank = st.sidebar.selectbox('会員ランク', ['シルバー会員', 'ゴールド会員', 'ダイヤモンド会員', 'ホワイト会員'])
    point = st.sidebar.number_input('利用ポイント', value=0, key=0)
    product = st.sidebar.number_input('商品数', min_value=0, max_value=10, value=1, key=99)

    if rank == 'ダイヤモンド会員':
        rank_per = diamond
    elif rank == 'ゴールド会員':
        rank_per = gold
    else:
        rank_per = white

    st.markdown(rf'''
    <br>
    ''', unsafe_allow_html=True)

    if product == 0:
        st.write('商品数を入力してください')

    if 0 < product >= 1:
        st.write('※１行目にポイントが発生しない商品を入れないでください。')
        check01 = st.checkbox('ビーンズクラブ会員対象品', key=1001)
        col03, col01, col01_1, col01_2, col02, col04 = st.columns([2,2,2,2,2,2])
        with col03:
            tax01 = st.selectbox('税率', [0.08, 0.1], key=3)
        with col01:
            item01 = st.text_input('税込価格', value=0, key=1)
        with col01_1:
            if check01 == True:
                item01 = st.text_input('割引後価格',  math.floor((Decimal(item01) * Decimal(beans_club))), key=111)
        with col02:
            amount01 = st.text_input('数量', value=0, key=2)
        with col04:
            point01 = math.floor(int((Decimal(item01) / Decimal(1+tax01)) * Decimal(rank_per)))
            point01_ = st.text_input('商品ポイント', Decimal(point01) * Decimal(amount01), key=4)
        with col01_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item01) / Decimal(1+tax01))), key=2001)

    if 0 < product >= 2:
        check02 = st.checkbox('ビーンズクラブ会員対象品', key=1002)
        col07, col05, col05_1, col05_2, col06, col08 = st.beta_columns([2,2,2,2,2,2])
        with col05:
            item02 = st.text_input('税込価格', value=0, key=5)
        with col05_1:
            if check02 == True:
                item02 = st.text_input('割引後価格',  math.floor((Decimal(item02) * Decimal(beans_club))), key=222)
        with col06:
            amount02 = st.text_input('数量', value=0, key=6)
        with col07:
            tax02 = st.selectbox('税率', [0.08, 0.1], key=7)
        with col08:
            point02 = math.floor(int((Decimal(item02) / Decimal(1+tax02)) * Decimal(rank_per)))
            point02_ = st.text_input('商品ポイント', Decimal(point02) * Decimal(amount02), key=8)
        with col05_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item02) / Decimal(1+tax02))), key=2002)

    if 0 < product >= 3:
        check03 = st.checkbox('ビーンズクラブ会員対象品', key=1003)
        col11, col09, col09_1, col09_2, col10, col12 = st.beta_columns([2,2,2,2,2,2])
        with col09:
            item03 = st.text_input('税込価格', value=0, key=9)
        with col09_1:
            if check03 == True:
                item03 = st.text_input('割引後価格', math.floor((Decimal(item03) * Decimal(beans_club))), key=333)
        with col10:
            amount03 = st.text_input('数量', value=0, key=10)
        with col11:
            tax03 = st.selectbox('税率', [0.08, 0.1], key=11)
        with col12:
            point03 = math.floor(int((Decimal(item03) / Decimal(1+tax03)) * Decimal(rank_per)))
            point03_ = st.text_input('商品ポイント', Decimal(point03) * Decimal(amount03), key=12)
        with col09_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item03) / Decimal(1+tax03))), key=2003)

    if 0 < product >= 4:
        check04 = st.checkbox('ビーンズクラブ会員対象品', key=1004)
        col15, col13, col13_1, col13_2, col14, col16 = st.beta_columns([2,2,2,2,2,2])
        with col13:
            item04 = st.text_input('税込価格', value=0, key=13)
        with col13_1:
            if check04 == True:
                item04 = st.text_input('割引後価格',  math.floor((Decimal(item04) * Decimal(beans_club))), key=444)
        with col14:
            amount04 = st.text_input('数量', value=0, key=14)
        with col15:
            tax04 = st.selectbox('税率', [0.08, 0.1], key=15)
        with col16:
            point04 = math.floor(int((Decimal(item04) / Decimal(1+tax04)) * Decimal(rank_per)))
            point04_ = st.text_input('商品ポイント', Decimal(point04) * Decimal(amount04), key=16)
        with col13_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item04) / Decimal(1+tax04))), key=2004)

    if 0 < product >= 5:
        check05 = st.checkbox('ビーンズクラブ会員対象品', key=1005)
        col19, col17, col17_1, col17_2, col18, col20 = st.beta_columns([2,2,2,2,2,2])
        with col17:
            item05 = st.text_input('税込価格', value=0, key=17)
        with col17_1:
            if check05 == True:
                item05 = st.text_input('割引後価格',  math.floor((Decimal(item05) * Decimal(beans_club))), key=555)
        with col18:
            amount05 = st.text_input('数量', value=0, key=18)
        with col19:
            tax05 = st.selectbox('税率', [0.08, 0.1], key=19)
        with col20:
            point05 = math.floor(int((Decimal(item05) / Decimal(1+tax05)) * Decimal(rank_per)))
            point05_ = st.text_input('商品ポイント', Decimal(point05) * Decimal(amount05), key=20)
        with col17_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item05) / Decimal(1+tax05))), key=2005)

    if 0 < product >= 6:
        check06 = st.checkbox('ビーンズクラブ会員対象品', key=1006)
        col23, col21, col21_1, col21_2, col22, col24 = st.beta_columns([2,2,2,2,2,2])
        with col21:
            item06 = st.text_input('税込価格', value=0, key=21)
        with col21_1:
            if check06 == True:
                item06 = st.text_input('割引後価格',  math.floor((Decimal(item06) * Decimal(beans_club))), key=666)
        with col22:
            amount06 = st.text_input('数量', value=0, key=22)
        with col23:
            tax06 = st.selectbox('税率', [0.08, 0.1], key=23)
        with col24:
            point06 = math.floor(int((Decimal(item06) / Decimal(1+tax06)) * Decimal(rank_per)))
            point06_ = st.text_input('商品ポイント', Decimal(point06) * Decimal(amount06), key=24)
        with col21_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item06) / Decimal(1+tax06))), key=2006)

    if 0 < product >= 7:
        check07 = st.checkbox('ビーンズクラブ会員対象品', key=1007)
        col27, col25, col25_1, col25_2, col26, col28 = st.beta_columns([2,2,2,2,2,2])
        with col25:
            item07 = st.text_input('税込価格', value=0, key=25)
        with col25_1:
            if check07 == True:
                item07 = st.text_input('割引後価格',  math.floor((Decimal(item07) * Decimal(beans_club))), key=777)
        with col26:
            amount07 = st.text_input('数量', value=0, key=26)
        with col27:
            tax07 = st.selectbox('税率', [0.08, 0.1], key=27)
        with col28:
            point07 = math.floor(int((Decimal(item07) / Decimal(1+tax07)) * Decimal(rank_per)))
            point07_ = st.text_input('商品ポイント', Decimal(point07) * Decimal(amount07), key=28)
        with col25_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item07) / Decimal(1+tax07))), key=2007)

    if 0 < product >= 8:
        check08 = st.checkbox('ビーンズクラブ会員対象品', key=1008)
        col31, col29, col29_1, col29_2, col30, col32 = st.beta_columns([2,2,2,2,2,2])
        with col29:
            item08 = st.text_input('税込価格', value=0, key=29)
        with col29_1:
            if check08 == True:
                item08 = st.text_input('割引後価格',  math.floor((Decimal(item08) * Decimal(beans_club))), key=888)
        with col30:
            amount08 = st.text_input('数量', value=0, key=30)
        with col31:
            tax08 = st.selectbox('税率', [0.08, 0.1], key=31)
        with col32:
            point08 = math.floor(int((Decimal(item08) / Decimal(1+tax08)) * Decimal(rank_per)))
            point08_ = st.text_input('商品ポイント', Decimal(point08) * Decimal(amount08), key=32)
        with col29_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item08) / Decimal(1+tax08))), key=2008)

    if 0 < product >= 9:
        check09 = st.checkbox('ビーンズクラブ会員対象品', key=1009)
        col35, col33, col33_1, col33_2, col34, col36 = st.beta_columns([2,2,2,2,2,2])
        with col33:
            item09 = st.text_input('税込価格', value=0, key=33)
        with col33_1:
            if check09 == True:
                item09 = st.text_input('割引後価格',  math.floor((Decimal(item09) * Decimal(beans_club))), key=999)
        with col34:
            amount09 = st.text_input('数量', value=0, key=34)
        with col35:
            tax09 = st.selectbox('税率', [0.08, 0.1], key=35)
        with col36:
            point09 = math.floor(int((Decimal(item09) / Decimal(1+tax09)) * Decimal(rank_per)))
            point09_ = st.text_input('商品ポイント', Decimal(point09) * Decimal(amount09), key=36)
        with col33_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item09) / Decimal(1+tax09))), key=2009)

    if 0 < product >= 10:
        check10 = st.checkbox('ビーンズクラブ会員対象品', key=1010)
        col39, col37, col37_1, col37_2, col38, col40 = st.beta_columns([2,2,2,2,2,2])
        with col37:
            item10 = st.text_input('税込価格', value=0, key=37)
        with col37_1:
            if check10 == True:
                item10 = st.text_input('割引後価格',  math.floor((Decimal(item10) * Decimal(beans_club))), key=1000)
        with col38:
            amount10 = st.text_input('数量', value=0, key=38)
        with col39:
            tax10 = st.selectbox('税率', [0.08, 0.1], key=39)
        with col40:
            point10 = math.floor(int((Decimal(item10) / Decimal(1+tax10)) * Decimal(rank_per)))
            point10_ = st.text_input('商品ポイント', Decimal(point10) * Decimal(amount10), key=40)
        with col37_2:
            st.text_input('税抜価格', math.floor(int(Decimal(item10) / Decimal(1+tax10))), key=2010)


    if product > 0:
        st.markdown(rf'''
        <hr>
        ''', unsafe_allow_html=True)
        if int(product) == 1:
            if int(point01_) > 0:
                product01 = int(item01)
                point_re01 = math.floor(int((((Decimal(product01)) - Decimal(point)) / (Decimal(product01))) * Decimal(point01)) * Decimal(amount01))
                st.text_input('合計ポイント付与数', point_re01)
            else:
                st.text_input('合計ポイント付与数', '')
        if int(product) == 2:
            if int(point01_) > 0 and int(point02_) >= 0:
                product02 = int(int(item01) + int(int(item02)))
                point_re01 = math.floor(int((((Decimal(product02) - Decimal(point)) / Decimal(product02)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product02) - Decimal(point)) / Decimal(product02)) * Decimal(point02))) * Decimal(amount02))
                st.text_input('合計ポイント付与数', int(point_re01) + int(point_re02))
            else:
                st.text_input('合計ポイント付与数', '')
        if int(product) == 3:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0:
                product03 = int(int(item01)) + int(int(item02)) + int(int(item03))
                point_re01 = math.floor(int((((Decimal(product03) - Decimal(point)) / Decimal(product03)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product03) - Decimal(point)) / Decimal(product03)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product03) - Decimal(point)) / Decimal(product03)) * Decimal(point03))) * Decimal(amount03))
                st.text_input('合計ポイント付与数', int(point_re01) + int(point_re02) + int(point_re03))
            else:
                st.text_input('合計ポイント付与数', '')
        if int(product) == 4:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0 and int(point04_) >= 0:
                product04 = int(int(item01)) + int(int(item02)) + int(int(item03)) + int(int(item04))
                point_re01 = math.floor(int((((Decimal(product04) - Decimal(point)) / Decimal(product04)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product04) - Decimal(point)) / Decimal(product04)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product04) - Decimal(point)) / Decimal(product04)) * Decimal(point03))) * Decimal(amount03))
                point_re04 = math.floor(int((((Decimal(product04) - Decimal(point)) / Decimal(product04)) * Decimal(point04))) * Decimal(amount04))
                st.text_input('合計ポイント付与数', int(point_re01) + int(point_re02) + int(point_re03) + int(point_re04))
            else:
                st.text_input('合計ポイント付与数', '')
        if int(product) == 5:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0 and int(point04_) >= 0 and int(point05_) >= 0:
                product05 = int(int(item01)) + int(int(item02)) + int(int(item03)) + int(int(item04)) + int(int(item05))
                point_re01 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point03))) * Decimal(amount03))
                point_re04 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point04))) * Decimal(amount04))
                point_re05 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point05))) * Decimal(amount05))
                st.text_input('合計ポイント付与数', int(point_re01) + int(point_re02) + int(point_re03) + int(point_re04) + int(point_re05))
            else:
                st.text_input('合計ポイント付与数', '')
        if int(product) == 6:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0 and int(point04_) >= 0 and int(point05_) >= 0 and int(point06_) >= 0:
                product06 = int(int(item01)) + int(int(item02)) + int(int(item03)) + int(int(item04)) + int(int(item05)) + int(int(item06))
                point_re01 = math.floor(int((((Decimal(product06) - Decimal(point)) / Decimal(product06)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product06) - Decimal(point)) / Decimal(product06)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product06) - Decimal(point)) / Decimal(product06)) * Decimal(point03))) * Decimal(amount03))
                point_re04 = math.floor(int((((Decimal(product06) - Decimal(point)) / Decimal(product06)) * Decimal(point04))) * Decimal(amount04))
                point_re05 = math.floor(int((((Decimal(product06) - Decimal(point)) / Decimal(product06)) * Decimal(point05))) * Decimal(amount05))
                point_re06 = math.floor(int((((Decimal(product06) - Decimal(point)) / Decimal(product06)) * Decimal(point06))) * Decimal(amount06))
                st.text_input('合計ポイント付与数', int(point_re01) + int(point_re02) + int(point_re03) + int(point_re04) + int(point_re05) + int(point_re06))
            else:
                st.text_input('合計ポイント付与数', '')
        if int(product) == 7:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0 and int(point04_) >= 0 and int(point05_) >= 0 and int(point06_) >= 0 and int(point07_) >= 0:
                product07 = int(int(item01)) + int(int(item02)) + int(int(item03)) + int(int(item04)) + int(int(item05)) + int(int(item06)) + int(int(item07))
                point_re01 = math.floor(int((((Decimal(product07) - Decimal(point)) / Decimal(product07)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product07) - Decimal(point)) / Decimal(product07)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product07) - Decimal(point)) / Decimal(product07)) * Decimal(point03))) * Decimal(amount03))
                point_re04 = math.floor(int((((Decimal(product07) - Decimal(point)) / Decimal(product07)) * Decimal(point04))) * Decimal(amount04))
                point_re05 = math.floor(int((((Decimal(product07) - Decimal(point)) / Decimal(product07)) * Decimal(point05))) * Decimal(amount05))
                point_re06 = math.floor(int((((Decimal(product07) - Decimal(point)) / Decimal(product07)) * Decimal(point06))) * Decimal(amount06))
                point_re07 = math.floor(int((((Decimal(product07) - Decimal(point)) / Decimal(product07)) * Decimal(point07))) * Decimal(amount07))
                st.text_input('合計ポイント付与数', int(point_re01) + int(point_re02) + int(point_re03) + int(point_re04) + int(point_re05) + int(point_re06) + int(point_re07))
            else:
                st.text_input('合計ポイント付与数', '')
        if int(product) == 8:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0 and int(point04_) >= 0 and int(point05_) >= 0 and int(point06_) >= 0 and int(point07_) >= 0 and int(point08_) >= 0:
                product08 = int(int(item01)) + int(int(item02)) + int(int(item03)) + int(int(item04)) + int(int(item05)) + int(int(item06)) + int(int(item07)) + int(int(item08))
                point_re01 = math.floor(int((((Decimal(product08) - Decimal(point)) / Decimal(product08)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product08) - Decimal(point)) / Decimal(product08)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product08) - Decimal(point)) / Decimal(product08)) * Decimal(point03))) * Decimal(amount03))
                point_re04 = math.floor(int((((Decimal(product08) - Decimal(point)) / Decimal(product08)) * Decimal(point04))) * Decimal(amount04))
                point_re05 = math.floor(int((((Decimal(product08) - Decimal(point)) / Decimal(product08)) * Decimal(point05))) * Decimal(amount05))
                point_re06 = math.floor(int((((Decimal(product08) - Decimal(point)) / Decimal(product08)) * Decimal(point06))) * Decimal(amount06))
                point_re07 = math.floor(int((((Decimal(product08) - Decimal(point)) / Decimal(product08)) * Decimal(point07))) * Decimal(amount07))
                point_re08 = math.floor(int((((Decimal(product08) - Decimal(point)) / Decimal(product08)) * Decimal(point08))) * Decimal(amount08))
                st.text_input('合計ポイント付与数', int(point_re01) + int(point_re02) + int(point_re03) + int(point_re04) + int(point_re05) + int(point_re06) + int(point_re07) + int(point_re08))
            else:
                st.text_input('合計ポイント付与数', '')
        if int(product) == 9:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0 and int(point04_) >= 0 and int(point05_) >= 0 and int(point06_) >= 0 and int(point07_) >= 0 and int(point08_) >= 0 and int(point09_) >= 0:
                product09 = int(int(item01)) + int(int(item02)) + int(int(item03)) + int(int(item04)) + int(int(item05)) + int(int(item06)) + int(int(item07)) + int(int(item08)) + int(int(item09))
                point_re01 = math.floor(int((((Decimal(product09) - Decimal(point)) / Decimal(product09)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product09) - Decimal(point)) / Decimal(product09)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product09) - Decimal(point)) / Decimal(product09)) * Decimal(point03))) * Decimal(amount03))
                point_re04 = math.floor(int((((Decimal(product09) - Decimal(point)) / Decimal(product09)) * Decimal(point04))) * Decimal(amount04))
                point_re05 = math.floor(int((((Decimal(product09) - Decimal(point)) / Decimal(product09)) * Decimal(point05))) * Decimal(amount05))
                point_re06 = math.floor(int((((Decimal(product09) - Decimal(point)) / Decimal(product09)) * Decimal(point06))) * Decimal(amount06))
                point_re07 = math.floor(int((((Decimal(product09) - Decimal(point)) / Decimal(product09)) * Decimal(point07))) * Decimal(amount07))
                point_re08 = math.floor(int((((Decimal(product09) - Decimal(point)) / Decimal(product09)) * Decimal(point08))) * Decimal(amount08))
                point_re09 = math.floor(int((((Decimal(product09) - Decimal(point)) / Decimal(product09)) * Decimal(point09))) * Decimal(amount09))
                st.text_input('合計ポイント付与数', int(point_re01) + int(point_re02) + int(point_re03) + int(point_re04) + int(point_re05) + int(point_re06) + int(point_re07) + int(point_re08) + int(point_re09))
            else:
                st.text_input('合計ポイント付与数', '')
        if int(product) == 10:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0 and int(point04_) >= 0 and int(point05_) >= 0 and int(point06_) >= 0 and int(point07_) >= 0 and int(point08_) >= 0 and int(point09_) >= 0 and int(point10_) >= 0:
                product10 = int(int(item01)) + int(int(item02)) + int(int(item03)) + int(int(item04)) + int(int(item05)) + int(int(item06)) + int(int(item07)) + int(int(item08)) + int(int(item09)) + int(int(item10))
                point_re01 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point03))) * Decimal(amount03))
                point_re04 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point04))) * Decimal(amount04))
                point_re05 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point05))) * Decimal(amount05))
                point_re06 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point06))) * Decimal(amount06))
                point_re07 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point07))) * Decimal(amount07))
                point_re08 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point08))) * Decimal(amount08))
                point_re09 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point09))) * Decimal(amount09))
                point_re10 = math.floor(int((((Decimal(product10) - Decimal(point)) / Decimal(product10)) * Decimal(point10))) * Decimal(amount10))
                st.text_input('合計ポイント付与数', int(point_re01) + int(point_re02) + int(point_re03) + int(point_re04) + int(point_re05) + int(point_re06) + int(point_re07) + int(point_re08) + int(point_re09) + int(point_re10))
            else:
                st.text_input('合計ポイント付与数', '')

else:
    st.markdown(rf'''
    <br>
    ''', unsafe_allow_html=True)
    price = st.sidebar.text_input('税込金額', 0, key=1)
    tax = st.sidebar.selectbox('税率', [0.08, 0.1])

    col01, col02 = st.columns([1,1])
    with col01:
        st.text_input('ホワイト会員（1%還元）', int((Decimal(price) / Decimal(1 + tax)) * Decimal(white)), key=2)
    with col02:
        st.text_input('シルバー会員（1%還元）', int((Decimal(price) / Decimal(1 + tax)) * Decimal(silver)), key=3)
    col03, col04 = st.beta_columns([1,1])
    with col03:
        st.text_input('ゴールド会員（2%還元）', int((Decimal(price) / Decimal(1 + tax)) * Decimal(gold)), key=4)
    with col04:
        st.text_input('ダイヤモンド会員（3%還元）', int((Decimal(price) / Decimal(1 + tax)) * Decimal(diamond)), key=5)
    
    st.markdown(rf'''
    <hr>
    ''', unsafe_allow_html=True)

    st.subheader('イベント企画計算用')
    col05, col06, col07, col08 = st.beta_columns([1,1,1,1])
    with col05:
        st.text_input('2%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.02)), key=12)
    with col06:
        st.text_input('3%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.03)), key=13)
    with col07:
        st.text_input('4%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.04)), key=14)
    with col08:
        st.text_input('5%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.05)), key=15)
    col09, col10, col11, col12 = st.beta_columns([1,1,1,1])
    with col09:
        st.text_input('6%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.06)), key=16)
    with col10:
        st.text_input('7%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.07)), key=17)
    with col11:
        st.text_input('8%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.08)), key=18)
    with col12:
        st.text_input('9%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.09)), key=19)
    col13, col14, col15, col16 = st.beta_columns([1,1,1,1])
    with col13:
        st.text_input('10%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.10)), key=20)
    with col14:
        st.text_input('11%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.11)), key=21)
    with col15:
        st.text_input('12%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.12)), key=22)
    with col16:
        st.text_input('13%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.13)), key=23)
    col17, col18, col19, col20 = st.beta_columns([1,1,1,1])
    with col17:
        st.text_input('14%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.14)), key=24)
    with col18:
        st.text_input('15%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.15)), key=25)
    with col19:
        st.text_input('16%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.16)), key=26)
    with col20:
        st.text_input('17%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.17)), key=27)
    col21, col22, col23, col24 = st.beta_columns([1,1,1,1])
    with col21:
        st.text_input('18%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.18)), key=28)
    with col22:
        st.text_input('19%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.19)), key=29)
    with col23:
        st.text_input('20%還元', int((Decimal(price) / Decimal(1 + tax)) * Decimal(0.20)), key=30)
