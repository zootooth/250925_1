

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os


# 한글 폰트 설정
font_path = os.path.join(os.path.dirname(__file__), '../fonts/NanumGothic-Regular.ttf')
if os.path.exists(font_path):
	fm.fontManager.addfont(font_path)
	plt.rc('font', family='NanumGothic')
	plt.rcParams['axes.unicode_minus'] = False

st.title('간단한 데이터 시각화 앱')

# 예시 데이터 생성
data = {
	'연도': [2020, 2021, 2022, 2023],
	'매출': [100, 150, 200, 250],
	'이익': [20, 30, 50, 70]
}
df = pd.DataFrame(data)

st.write('### 데이터 미리보기')
st.dataframe(df)

col = st.selectbox('시각화할 컬럼을 선택하세요', ['매출', '이익'])

fig, ax = plt.subplots()
ax.plot(df['연도'], df[col], marker='o')
ax.set_xlabel('연도')
ax.set_ylabel(col)
ax.set_title(f'연도별 {col} 변화')
st.pyplot(fig)
