import streamlit as st

st.title('나의 첫 웹서비스 만들기!!')
name = st.text_input('이름을 입력하세요 : ')
menu = st.selectbox('가장 많이 쓰는 앱은? : ', ['유튜브','인스타','카톡'])
time = st.slider('하루 사용 시간은?', 0, 12, 2)


if st.button('나의 디지털 습관'):
    st.write(f'{name}님은 {menu}를 {time}시간 사용중이시군요요. 균형잡힌 습관이 중요해요!')
