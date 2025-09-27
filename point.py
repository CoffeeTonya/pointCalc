import fractions
import streamlit as st
import numpy as np
import pandas as pd
from decimal import Decimal, getcontext
from fractions import Fraction
import math

st.title('付与ポイント計算ツール')

getcontext().prec = 5

# col01, col02, col03 = st.columns(3)
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
    multiplier = st.sidebar.selectbox('イベント ポイント倍率', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], index=0)

    if multiplier != 1:
        diamond = 0.03*multiplier
        gold = 0.02*multiplier
        silver = 0.01*multiplier
        white = 0.01*multiplier

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
                discounted_price = math.floor((Decimal(item01) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col02:
            amount01 = st.text_input('数量', value=0, key=2)
        with col04:
            if check01 == True:
                # 割引後価格から計算
                discounted_price = math.floor((Decimal(item01) * Decimal(beans_club)))
                point01 = math.floor(int((Decimal(discounted_price) / Decimal(1+tax01)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point01 = math.floor(int((Decimal(item01) / Decimal(1+tax01)) * Decimal(rank_per)))
            point01_ = Decimal(point01) * Decimal(amount01)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point01_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col01_2:
            try:
                if check01 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price = math.floor((Decimal(item01) * Decimal(beans_club)))
                    tax_excluded_price = math.floor(int(Decimal(discounted_price) / Decimal(1+tax01)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price = math.floor(int(Decimal(item01) / Decimal(1+tax01)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)

    if 0 < product >= 2:
        check02 = st.checkbox('ビーンズクラブ会員対象品', key=1002)
        col07, col05, col05_1, col05_2, col06, col08 = st.columns([2,2,2,2,2,2])
        with col05:
            item02 = st.text_input('税込価格', value=0, key=5)
        with col05_1:
            if check02 == True:
                discounted_price02 = math.floor((Decimal(item02) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price02:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col06:
            amount02 = st.text_input('数量', value=0, key=6)
        with col07:
            tax02 = st.selectbox('税率', [0.08, 0.1], key=7)
        with col08:
            if check02 == True:
                # 割引後価格から計算
                discounted_price02 = math.floor((Decimal(item02) * Decimal(beans_club)))
                point02 = math.floor(int((Decimal(discounted_price02) / Decimal(1+tax02)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point02 = math.floor(int((Decimal(item02) / Decimal(1+tax02)) * Decimal(rank_per)))
            point02_ = Decimal(point02) * Decimal(amount02)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point02_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col05_2:
            try:
                if check02 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price02 = math.floor((Decimal(item02) * Decimal(beans_club)))
                    tax_excluded_price02 = math.floor(int(Decimal(discounted_price02) / Decimal(1+tax02)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price02 = math.floor(int(Decimal(item02) / Decimal(1+tax02)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price02:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)

    if 0 < product >= 3:
        check03 = st.checkbox('ビーンズクラブ会員対象品', key=1003)
        col11, col09, col09_1, col09_2, col10, col12 = st.columns([2,2,2,2,2,2])
        with col09:
            item03 = st.text_input('税込価格', value=0, key=9)
        with col09_1:
            if check03 == True:
                discounted_price03 = math.floor((Decimal(item03) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price03:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col10:
            amount03 = st.text_input('数量', value=0, key=10)
        with col11:
            tax03 = st.selectbox('税率', [0.08, 0.1], key=11)
        with col12:
            if check03 == True:
                # 割引後価格から計算
                discounted_price03 = math.floor((Decimal(item03) * Decimal(beans_club)))
                point03 = math.floor(int((Decimal(discounted_price03) / Decimal(1+tax03)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point03 = math.floor(int((Decimal(item03) / Decimal(1+tax03)) * Decimal(rank_per)))
            point03_ = Decimal(point03) * Decimal(amount03)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point03_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col09_2:
            try:
                if check03 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price03 = math.floor((Decimal(item03) * Decimal(beans_club)))
                    tax_excluded_price03 = math.floor(int(Decimal(discounted_price03) / Decimal(1+tax03)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price03 = math.floor(int(Decimal(item03) / Decimal(1+tax03)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price03:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)

    if 0 < product >= 4:
        check04 = st.checkbox('ビーンズクラブ会員対象品', key=1004)
        col15, col13, col13_1, col13_2, col14, col16 = st.columns([2,2,2,2,2,2])
        with col13:
            item04 = st.text_input('税込価格', value=0, key=13)
        with col13_1:
            if check04 == True:
                discounted_price04 = math.floor((Decimal(item04) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price04:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col14:
            amount04 = st.text_input('数量', value=0, key=14)
        with col15:
            tax04 = st.selectbox('税率', [0.08, 0.1], key=15)
        with col16:
            if check04 == True:
                # 割引後価格から計算
                discounted_price04 = math.floor((Decimal(item04) * Decimal(beans_club)))
                point04 = math.floor(int((Decimal(discounted_price04) / Decimal(1+tax04)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point04 = math.floor(int((Decimal(item04) / Decimal(1+tax04)) * Decimal(rank_per)))
            point04_ = Decimal(point04) * Decimal(amount04)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point04_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col13_2:
            try:
                if check04 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price04 = math.floor((Decimal(item04) * Decimal(beans_club)))
                    tax_excluded_price04 = math.floor(int(Decimal(discounted_price04) / Decimal(1+tax04)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price04 = math.floor(int(Decimal(item04) / Decimal(1+tax04)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price04:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)

    if 0 < product >= 5:
        check05 = st.checkbox('ビーンズクラブ会員対象品', key=1005)
        col19, col17, col17_1, col17_2, col18, col20 = st.columns([2,2,2,2,2,2])
        with col17:
            item05 = st.text_input('税込価格', value=0, key=17)
        with col17_1:
            if check05 == True:
                discounted_price05 = math.floor((Decimal(item05) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price05:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col18:
            amount05 = st.text_input('数量', value=0, key=18)
        with col19:
            tax05 = st.selectbox('税率', [0.08, 0.1], key=19)
        with col20:
            if check05 == True:
                # 割引後価格から計算
                discounted_price05 = math.floor((Decimal(item05) * Decimal(beans_club)))
                point05 = math.floor(int((Decimal(discounted_price05) / Decimal(1+tax05)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point05 = math.floor(int((Decimal(item05) / Decimal(1+tax05)) * Decimal(rank_per)))
            point05_ = Decimal(point05) * Decimal(amount05)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point05_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col17_2:
            try:
                if check05 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price05 = math.floor((Decimal(item05) * Decimal(beans_club)))
                    tax_excluded_price05 = math.floor(int(Decimal(discounted_price05) / Decimal(1+tax05)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price05 = math.floor(int(Decimal(item05) / Decimal(1+tax05)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price05:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)

    if 0 < product >= 6:
        check06 = st.checkbox('ビーンズクラブ会員対象品', key=1006)
        col23, col21, col21_1, col21_2, col22, col24 = st.columns([2,2,2,2,2,2])
        with col21:
            item06 = st.text_input('税込価格', value=0, key=21)
        with col21_1:
            if check06 == True:
                discounted_price06 = math.floor((Decimal(item06) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price06:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col22:
            amount06 = st.text_input('数量', value=0, key=22)
        with col23:
            tax06 = st.selectbox('税率', [0.08, 0.1], key=23)
        with col24:
            if check06 == True:
                # 割引後価格から計算
                discounted_price06 = math.floor((Decimal(item06) * Decimal(beans_club)))
                point06 = math.floor(int((Decimal(discounted_price06) / Decimal(1+tax06)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point06 = math.floor(int((Decimal(item06) / Decimal(1+tax06)) * Decimal(rank_per)))
            point06_ = Decimal(point06) * Decimal(amount06)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point06_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col21_2:
            try:
                if check06 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price06 = math.floor((Decimal(item06) * Decimal(beans_club)))
                    tax_excluded_price06 = math.floor(int(Decimal(discounted_price06) / Decimal(1+tax06)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price06 = math.floor(int(Decimal(item06) / Decimal(1+tax06)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price06:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)

    if 0 < product >= 7:
        check07 = st.checkbox('ビーンズクラブ会員対象品', key=1007)
        col27, col25, col25_1, col25_2, col26, col28 = st.columns([2,2,2,2,2,2])
        with col25:
            item07 = st.text_input('税込価格', value=0, key=25)
        with col25_1:
            if check07 == True:
                discounted_price07 = math.floor((Decimal(item07) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price07:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col26:
            amount07 = st.text_input('数量', value=0, key=26)
        with col27:
            tax07 = st.selectbox('税率', [0.08, 0.1], key=27)
        with col28:
            if check07 == True:
                # 割引後価格から計算
                discounted_price07 = math.floor((Decimal(item07) * Decimal(beans_club)))
                point07 = math.floor(int((Decimal(discounted_price07) / Decimal(1+tax07)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point07 = math.floor(int((Decimal(item07) / Decimal(1+tax07)) * Decimal(rank_per)))
            point07_ = Decimal(point07) * Decimal(amount07)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point07_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col25_2:
            try:
                if check07 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price07 = math.floor((Decimal(item07) * Decimal(beans_club)))
                    tax_excluded_price07 = math.floor(int(Decimal(discounted_price07) / Decimal(1+tax07)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price07 = math.floor(int(Decimal(item07) / Decimal(1+tax07)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price07:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)

    if 0 < product >= 8:
        check08 = st.checkbox('ビーンズクラブ会員対象品', key=1008)
        col31, col29, col29_1, col29_2, col30, col32 = st.columns([2,2,2,2,2,2])
        with col29:
            item08 = st.text_input('税込価格', value=0, key=29)
        with col29_1:
            if check08 == True:
                discounted_price08 = math.floor((Decimal(item08) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price08:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col30:
            amount08 = st.text_input('数量', value=0, key=30)
        with col31:
            tax08 = st.selectbox('税率', [0.08, 0.1], key=31)
        with col32:
            if check08 == True:
                # 割引後価格から計算
                discounted_price08 = math.floor((Decimal(item08) * Decimal(beans_club)))
                point08 = math.floor(int((Decimal(discounted_price08) / Decimal(1+tax08)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point08 = math.floor(int((Decimal(item08) / Decimal(1+tax08)) * Decimal(rank_per)))
            point08_ = Decimal(point08) * Decimal(amount08)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point08_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col29_2:
            try:
                if check08 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price08 = math.floor((Decimal(item08) * Decimal(beans_club)))
                    tax_excluded_price08 = math.floor(int(Decimal(discounted_price08) / Decimal(1+tax08)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price08 = math.floor(int(Decimal(item08) / Decimal(1+tax08)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price08:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)

    if 0 < product >= 9:
        check09 = st.checkbox('ビーンズクラブ会員対象品', key=1009)
        col35, col33, col33_1, col33_2, col34, col36 = st.columns([2,2,2,2,2,2])
        with col33:
            item09 = st.text_input('税込価格', value=0, key=33)
        with col33_1:
            if check09 == True:
                discounted_price09 = math.floor((Decimal(item09) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price09:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col34:
            amount09 = st.text_input('数量', value=0, key=34)
        with col35:
            tax09 = st.selectbox('税率', [0.08, 0.1], key=35)
        with col36:
            if check09 == True:
                # 割引後価格から計算
                discounted_price09 = math.floor((Decimal(item09) * Decimal(beans_club)))
                point09 = math.floor(int((Decimal(discounted_price09) / Decimal(1+tax09)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point09 = math.floor(int((Decimal(item09) / Decimal(1+tax09)) * Decimal(rank_per)))
            point09_ = Decimal(point09) * Decimal(amount09)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point09_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col33_2:
            try:
                if check09 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price09 = math.floor((Decimal(item09) * Decimal(beans_club)))
                    tax_excluded_price09 = math.floor(int(Decimal(discounted_price09) / Decimal(1+tax09)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price09 = math.floor(int(Decimal(item09) / Decimal(1+tax09)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price09:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)

    if 0 < product >= 10:
        check10 = st.checkbox('ビーンズクラブ会員対象品', key=1010)
        col39, col37, col37_1, col37_2, col38, col40 = st.columns([2,2,2,2,2,2])
        with col37:
            item10 = st.text_input('税込価格', value=0, key=37)
        with col37_1:
            if check10 == True:
                discounted_price10 = math.floor((Decimal(item10) * Decimal(beans_club)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">割引後価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{discounted_price10:,}</div>
                </div>
                """, unsafe_allow_html=True)
        with col38:
            amount10 = st.text_input('数量', value=0, key=38)
        with col39:
            tax10 = st.selectbox('税率', [0.08, 0.1], key=39)
        with col40:
            if check10 == True:
                # 割引後価格から計算
                discounted_price10 = math.floor((Decimal(item10) * Decimal(beans_club)))
                point10 = math.floor(int((Decimal(discounted_price10) / Decimal(1+tax10)) * Decimal(rank_per)))
            else:
                # 通常価格から計算
                point10 = math.floor(int((Decimal(item10) / Decimal(1+tax10)) * Decimal(rank_per)))
            point10_ = Decimal(point10) * Decimal(amount10)
            st.markdown(f"""
            <div style="font-size: 16px;">
                <div style="color: #666; font-size: 14px;">商品ポイント</div>
                <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{point10_:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col37_2:
            try:
                if check10 == True:
                    # 割引後価格から税抜き価格を計算
                    discounted_price10 = math.floor((Decimal(item10) * Decimal(beans_club)))
                    tax_excluded_price10 = math.floor(int(Decimal(discounted_price10) / Decimal(1+tax10)))
                else:
                    # 通常価格から税抜き価格を計算
                    tax_excluded_price10 = math.floor(int(Decimal(item10) / Decimal(1+tax10)))
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">{tax_excluded_price10:,}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown(f"""
                <div style="font-size: 16px;">
                    <div style="color: #666; font-size: 14px;">税抜価格</div>
                    <div style="font-size: 20px; font-weight: normal; padding: 10px 0px;">0</div>
                </div>
                """, unsafe_allow_html=True)


    if product > 0:
        st.markdown(rf'''
        <hr>
        ''', unsafe_allow_html=True)
        if int(product) == 1:
            if int(point01_) > 0:
                product01 = int(item01)
                point_re01 = math.floor(int((((Decimal(product01)) - Decimal(point)) / (Decimal(product01))) * Decimal(point01)) * Decimal(amount01))
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 4px solid #1f77b4;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #1f77b4;">{point_re01:,}pt</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #999;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #999;">0pt</div>
                </div>
                """, unsafe_allow_html=True)
        if int(product) == 2:
            if int(point01_) > 0 and int(point02_) >= 0:
                product02 = int(int(item01) + int(int(item02)))
                point_re01 = math.floor(int((((Decimal(product02) - Decimal(point)) / Decimal(product02)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product02) - Decimal(point)) / Decimal(product02)) * Decimal(point02))) * Decimal(amount02))
                total_points = int(point_re01) + int(point_re02)
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 4px solid #1f77b4;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #1f77b4;">{total_points:,}pt</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #999;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #999;">0pt</div>
                </div>
                """, unsafe_allow_html=True)
        if int(product) == 3:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0:
                product03 = int(int(item01)) + int(int(item02)) + int(int(item03))
                point_re01 = math.floor(int((((Decimal(product03) - Decimal(point)) / Decimal(product03)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product03) - Decimal(point)) / Decimal(product03)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product03) - Decimal(point)) / Decimal(product03)) * Decimal(point03))) * Decimal(amount03))
                total_points = int(point_re01) + int(point_re02) + int(point_re03)
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 4px solid #1f77b4;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #1f77b4;">{total_points:,}pt</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #999;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #999;">0pt</div>
                </div>
                """, unsafe_allow_html=True)
        if int(product) == 4:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0 and int(point04_) >= 0:
                product04 = int(int(item01)) + int(int(item02)) + int(int(item03)) + int(int(item04))
                point_re01 = math.floor(int((((Decimal(product04) - Decimal(point)) / Decimal(product04)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product04) - Decimal(point)) / Decimal(product04)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product04) - Decimal(point)) / Decimal(product04)) * Decimal(point03))) * Decimal(amount03))
                point_re04 = math.floor(int((((Decimal(product04) - Decimal(point)) / Decimal(product04)) * Decimal(point04))) * Decimal(amount04))
                total_points = int(point_re01) + int(point_re02) + int(point_re03) + int(point_re04)
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 4px solid #1f77b4;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #1f77b4;">{total_points:,}pt</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #999;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #999;">0pt</div>
                </div>
                """, unsafe_allow_html=True)
        if int(product) == 5:
            if int(point01_) > 0 and int(point02_) >= 0 and int(point03_) >= 0 and int(point04_) >= 0 and int(point05_) >= 0:
                product05 = int(int(item01)) + int(int(item02)) + int(int(item03)) + int(int(item04)) + int(int(item05))
                point_re01 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point01))) * Decimal(amount01))
                point_re02 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point02))) * Decimal(amount02))
                point_re03 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point03))) * Decimal(amount03))
                point_re04 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point04))) * Decimal(amount04))
                point_re05 = math.floor(int((((Decimal(product05) - Decimal(point)) / Decimal(product05)) * Decimal(point05))) * Decimal(amount05))
                total_points = int(point_re01) + int(point_re02) + int(point_re03) + int(point_re04) + int(point_re05)
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f0f8ff; padding: 15px; border-radius: 8px; border-left: 4px solid #1f77b4;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #1f77b4;">{total_points:,}pt</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="font-size: 18px; background-color: #f5f5f5; padding: 15px; border-radius: 8px; border-left: 4px solid #999;">
                    <div style="color: #666; font-size: 16px; margin-bottom: 8px;">合計ポイント付与数</div>
                    <div style="font-size: 24px; font-weight: bold; color: #999;">0pt</div>
                </div>
                """, unsafe_allow_html=True)
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

    # 税抜価格を計算
    tax_excluded_price = Decimal(price) / Decimal(1 + tax)
    
    col01, col02 = st.columns([1,1])
    with col01:
        result_white = int(tax_excluded_price * Decimal(white))
        st.metric('ホワイト会員（1%還元）', f'{result_white:,}pt')
    with col02:
        result_silver = int(tax_excluded_price * Decimal(silver))
        st.metric('シルバー会員（1%還元）', f'{result_silver:,}pt')
    col03, col04 = st.columns([1,1])
    with col03:
        result_gold = int(tax_excluded_price * Decimal(gold))
        st.metric('ゴールド会員（2%還元）', f'{result_gold:,}pt')
    with col04:
        result_diamond = int(tax_excluded_price * Decimal(diamond))
        st.metric('ダイヤモンド会員（3%還元）', f'{result_diamond:,}pt')
    
    st.markdown(rf'''
    <hr>
    ''', unsafe_allow_html=True)

    st.subheader('イベント企画計算用')
    
    # 税抜価格を計算
    tax_excluded_price = Decimal(price) / Decimal(1 + tax)
    
    col05, col06, col07, col08 = st.columns([1,1,1,1])
    with col05:
        result_2 = int(tax_excluded_price * Decimal(0.02))
        st.metric('2%還元', f'{result_2:,}pt')
    with col06:
        result_3 = int(tax_excluded_price * Decimal(0.03))
        st.metric('3%還元', f'{result_3:,}pt')
    with col07:
        result_4 = int(tax_excluded_price * Decimal(0.04))
        st.metric('4%還元', f'{result_4:,}pt')
    with col08:
        result_5 = int(tax_excluded_price * Decimal(0.05))
        st.metric('5%還元', f'{result_5:,}pt')
    
    col09, col10, col11, col12 = st.columns([1,1,1,1])
    with col09:
        result_6 = int(tax_excluded_price * Decimal(0.06))
        st.metric('6%還元', f'{result_6:,}pt')
    with col10:
        result_7 = int(tax_excluded_price * Decimal(0.07))
        st.metric('7%還元', f'{result_7:,}pt')
    with col11:
        result_8 = int(tax_excluded_price * Decimal(0.08))
        st.metric('8%還元', f'{result_8:,}pt')
    with col12:
        result_9 = int(tax_excluded_price * Decimal(0.09))
        st.metric('9%還元', f'{result_9:,}pt')
    
    col13, col14, col15, col16 = st.columns([1,1,1,1])
    with col13:
        result_10 = int(tax_excluded_price * Decimal(0.10))
        st.metric('10%還元', f'{result_10:,}pt')
    with col14:
        result_11 = int(tax_excluded_price * Decimal(0.11))
        st.metric('11%還元', f'{result_11:,}pt')
    with col15:
        result_12 = int(tax_excluded_price * Decimal(0.12))
        st.metric('12%還元', f'{result_12:,}pt')
    with col16:
        result_13 = int(tax_excluded_price * Decimal(0.13))
        st.metric('13%還元', f'{result_13:,}pt')
    
    col17, col18, col19, col20 = st.columns([1,1,1,1])
    with col17:
        result_14 = int(tax_excluded_price * Decimal(0.14))
        st.metric('14%還元', f'{result_14:,}pt')
    with col18:
        result_15 = int(tax_excluded_price * Decimal(0.15))
        st.metric('15%還元', f'{result_15:,}pt')
    with col19:
        result_16 = int(tax_excluded_price * Decimal(0.16))
        st.metric('16%還元', f'{result_16:,}pt')
    with col20:
        result_17 = int(tax_excluded_price * Decimal(0.17))
        st.metric('17%還元', f'{result_17:,}pt')
    
    col21, col22, col23, col24 = st.columns([1,1,1,1])
    with col21:
        result_18 = int(tax_excluded_price * Decimal(0.18))
        st.metric('18%還元', f'{result_18:,}pt')
    with col22:
        result_19 = int(tax_excluded_price * Decimal(0.19))
        st.metric('19%還元', f'{result_19:,}pt')
    with col23:
        result_20 = int(tax_excluded_price * Decimal(0.20))
        st.metric('20%還元', f'{result_20:,}pt')
