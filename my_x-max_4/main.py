# 통합 메인 프로세스

import streamlit as st
from adcopy_main_streamlit import main_adcopy
from youtube_main_streamlit import main_ytb
from sns_main_streamlit import main_sns

# 페이지 전체 너비 사용
st.set_page_config(layout="wide")

# 사이드바 제목과 메뉴 선택
with st.sidebar :
    st.title("콘텐츠 에이전트!")
    menu = st.selectbox("메뉴선택", ["1.광고 카피", "2.유튜브 스크립트", "3.SNS 포스팅"])

# 선택된 메뉴별 메인 코드 호출
if menu == "1.광고 카피" :
    main_adcopy()
elif menu == "2.유튜브 스크립트" :
    main_ytb()
elif menu == "3.SNS 포스팅" :
    main_sns()
    