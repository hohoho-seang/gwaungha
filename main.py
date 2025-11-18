import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('나의 첫 웹서비스 만들기!!')

if 'responses' not in st.session_state:
    st.session_state.responses = []

name = st.text_input('이름을 입력하세요 : ')
menu = st.selectbox('가장 많이 쓰는 앱은? : ', ['유튜브', '인스타', '카톡'])
time = st.slider('하루 사용 시간은?', 0, 12, 2)

if st.button('나의 디지털 습관'):
    record = {
        'name': name if name.strip() else '익명',
        'menu': menu,
        'time': time,
    }
    st.session_state.responses.append(record)
    st.success(f"{record['name']}님은 {menu}를 {time}시간 사용중이시군요. 균형잡힌 습관이 중요해요!")
    st.balloons()

if st.session_state.responses:
    st.subheader('사용자 응답 요약')
    df = pd.DataFrame(st.session_state.responses)
    st.dataframe(df, use_container_width=True)

    menu_counts = df['menu'].value_counts()
    avg_time = df.groupby('menu')['time'].mean().reindex(menu_counts.index)

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
