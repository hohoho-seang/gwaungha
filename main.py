import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from pathlib import Path

st.title('나의 첫 웹서비스 만들기!!')

DB_PATH = Path(__file__).with_name('responses.db')


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                menu TEXT NOT NULL,
                time INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def insert_response(name: str, menu: str, time_value: int):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO responses (name, menu, time) VALUES (?, ?, ?)",
            (name, menu, time_value),
        )
        conn.commit()


def fetch_responses() -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        df = pd.read_sql_query(
            "SELECT name, menu, time, created_at FROM responses ORDER BY created_at DESC",
            conn,
        )
    return df


init_db()

name = st.text_input('이름을 입력하세요 : ')
menu = st.selectbox('가장 많이 쓰는 앱은? : ', ['유튜브', '인스타', '카톡'])
time_value = st.slider('하루 사용 시간은?', 0, 12, 2)

if st.button('나의 디지털 습관'):
    safe_name = name.strip() or '익명'
    insert_response(safe_name, menu, int(time_value))
    st.success(f"{safe_name}님은 {menu}를 {time_value}시간 사용중이시군요. 균형잡힌 습관이 중요해요!")
    st.balloons()

responses_df = fetch_responses()

if not responses_df.empty:
    st.subheader('사용자 응답 요약')
    st.dataframe(responses_df, use_container_width=True)

    menu_counts = responses_df['menu'].value_counts()
    avg_time = responses_df.groupby('menu')['time'].mean().reindex(menu_counts.index)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('**앱 사용 비율 (파이그래프)**')
        fig, ax = plt.subplots()
        ax.pie(menu_counts.values, labels=menu_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig, clear_figure=True)

    with col2:
        st.markdown('**앱별 평균 사용 시간 (막대그래프)**')
        st.bar_chart(avg_time)
else:
    st.info('아직 저장된 응답이 없습니다. 첫 응답자가 되어주세요!')
