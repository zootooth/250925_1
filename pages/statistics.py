import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import math

# --- 페이지 기본 설정 ---
st.set_page_config(
    page_title="확률 시뮬레이터",
    page_icon="🎲",
    layout="wide",
)

st.title("🎲 확률 시뮬레이션 웹 앱")
st.write("""
이 웹 앱은 독립 시행의 원리를 이용하여 다양한 확률 문제를 시뮬레이션합니다.
시행 횟수를 늘려보면서 경험적 확률이 수학적 확률에 어떻게 근접하는지 확인해보세요.
""")

# --- 사이드바 메뉴 ---
with st.sidebar:
    st.header("시뮬레이션 선택")
    selected_sim = st.selectbox(
        "어떤 시뮬레이션을 실행하시겠습니까?",
        ("주사위 던지기", "로또 1등 당첨", "몬테카를로 파이(π) 추정")
    )
    st.markdown("---")


# --- 1. 주사위 던지기 시뮬레이션 ---
if selected_sim == "주사위 던지기":
    st.header("주사위 던지기")
    st.markdown("""
    공정한 주사위를 여러 번 던질 때 특정 숫자가 나올 확률을 시뮬레이션합니다.
    주사위의 각 면이 나올 수학적 확률은 $$P(X=k) = \\frac{1}{6} \\approx 16.67\\%$$ 입니다.
    """)

    # 사용자 입력
    st.sidebar.subheader("주사위 설정")
    dice_choice = st.sidebar.slider("관심 있는 주사위 눈금", 1, 6, 3)
    num_trials_dice = st.sidebar.slider("시행 횟수 (던지는 횟수)", 100, 100000, 1000, step=100)

    # 시뮬레이션 실행 버튼
    if st.button("주사위 던지기 시뮬레이션 실행"):
        # 시뮬레이션 로직
        with st.spinner(f"{num_trials_dice}번의 주사위를 던지는 중..."):
            rolls = np.random.randint(1, 7, size=num_trials_dice)
            success_count = np.sum(rolls == dice_choice)
            empirical_prob = (success_count / num_trials_dice) * 100
            theoretical_prob = (1/6) * 100

        # 결과 표시
        st.subheader("시뮬레이션 결과")
        col1, col2, col3 = st.columns(3)
        col1.metric("총 시행 횟수", f"{num_trials_dice:,}회")
        col2.metric(f"'{dice_choice}'가 나온 횟수", f"{success_count:,}회")
        col3.metric("성공 횟수", f"{success_count:,}회")

        st.write(f"**수학적 확률:** `{theoretical_prob:.2f}%`")
        st.write(f"**경험적 확률 (시뮬레이션 결과):** `{empirical_prob:.2f}%`")

        # 시각화
        st.subheader("주사위 눈금별 빈도")
        df_rolls = pd.DataFrame(rolls, columns=['결과'])
        counts = df_rolls['결과'].value_counts().sort_index().reset_index()
        counts.columns = ['주사위 눈금', '나온 횟수']

        chart = alt.Chart(counts).mark_bar().encode(
            x=alt.X('주사위 눈금:O', title='주사위 눈금'), # O: Ordinal
            y=alt.Y('나온 횟수:Q', title='나온 횟수'), # Q: Quantitative
            tooltip=['주사위 눈금', '나온 횟수']
        ).properties(
            title=f"{num_trials_dice}번 던졌을 때 각 눈금의 빈도수"
        )
        st.altair_chart(chart, use_container_width=True)


# --- 2. 로또 1등 당첨 시뮬레이션 ---
elif selected_sim == "로또 1등 당첨":
    st.header("로또 1등 당첨")
    st.markdown("""
    대한민국 로또(6/45) 1등에 당첨될 확률을 시뮬레이션합니다.
    1등 당첨의 수학적 확률은 45개의 숫자 중 6개를 정확히 맞춰야 하므로 다음과 같습니다.
    $$P(\\text{1등 당첨}) = \\frac{1}{_{45}C_6} = \\frac{1}{8,145,060} \\approx 0.0000123\\%$$
    이 확률은 매우 낮아, 많은 횟수를 시도해도 1등 당첨이 나오지 않을 가능성이 높습니다.
    """)

    # 사용자 입력
    st.sidebar.subheader("로또 설정")
    num_trials_lotto = st.sidebar.number_input("시행 횟수 (구매할 로또 개수)", min_value=1000, max_value=10000000, value=100000, step=1000)

    # 시뮬레이션 실행 버튼
    if st.button("로또 구매 시뮬레이션 실행"):
        # 시뮬레이션 로직
        with st.spinner(f"{num_trials_lotto:,}개의 로또를 구매하는 중... (시간이 걸릴 수 있습니다)"):
            winning_numbers = set(np.random.choice(range(1, 46), 6, replace=False))
            win_count = 0
            for _ in range(num_trials_lotto):
                my_numbers = set(np.random.choice(range(1, 46), 6, replace=False))
                if my_numbers == winning_numbers:
                    win_count += 1
            
            empirical_prob = (win_count / num_trials_lotto) * 100
            theoretical_prob = (1 / 8145060) * 100

        # 결과 표시
        st.subheader("시뮬레이션 결과")
        st.info(f"이번 회차 당첨 번호: **{sorted(list(winning_numbers))}**")

        col1, col2 = st.columns(2)
        col1.metric("총 구매 개수", f"{num_trials_lotto:,}개")
        col2.metric("1등 당첨 횟수", f"{win_count}회", delta="🎉" if win_count > 0 else "")

        st.write(f"**수학적 확률:** `{theoretical_prob:.10f}%`")
        st.write(f"**경험적 확률 (시뮬레이션 결과):** `{empirical_prob:.10f}%`")


# --- 3. 몬테카를로 파이(π) 추정 ---
elif selected_sim == "몬테카를로 파이(π) 추정":
    st.header("몬테카를로 방법을 이용한 파이(π) 값 추정")
    st.markdown("""
    복잡한 계산을 무수히 많은 무작위 추출(Random Sampling)을 통해 근사적으로 계산하는 것을 '몬테카를로 방법'이라고 합니다.
    여기서는 정사각형 안에 무작위로 점을 찍어, 원 안에 들어가는 점의 비율을 이용해 원주율 π 값을 추정합니다.

    정사각형의 넓이는 $(2r)^2 = 4r^2$ 이고, 내접하는 원의 넓이는 $\pi r^2$ 입니다.
    무작위로 점을 찍었을 때, 점이 원 안에 있을 확률은 넓이의 비율과 같습니다.
    $$ P(\\text{점 in 원}) = \\frac{\\text{원의 넓이}}{\\text{정사각형의 넓이}} = \\frac{\pi r^2}{4r^2} = \\frac{\pi}{4} $$
    따라서 우리는 시뮬레이션을 통해 π를 다음과 같이 추정할 수 있습니다.
    $$ \pi \\approx 4 \\times \\frac{\\text{원 안의 점 개수}}{\\text{전체 점 개수}} $$
    """)

    # 사용자 입력
    st.sidebar.subheader("몬테카를로 설정")
    num_points = st.sidebar.slider("생성할 점의 개수", 1000, 100000, 5000, step=1000)

    if st.button("π 값 추정 시뮬레이션 실행"):
        # 시뮬레이션 로직
        with st.spinner(f"{num_points:,}개의 점을 생성하여 계산하는 중..."):
            # -1과 1 사이의 x, y 좌표 생성
            points_x = np.random.uniform(-1, 1, num_points)
            points_y = np.random.uniform(-1, 1, num_points)

            # 원점으로부터의 거리 계산 (x^2 + y^2)
            distance_sq = points_x**2 + points_y**2
            
            # 거리가 1 이하이면 원 안의 점
            is_inside = distance_sq <= 1
            points_inside_circle = np.sum(is_inside)

            # 파이 값 추정
            pi_estimate = 4 * (points_inside_circle / num_points)

        # 결과 표시
        st.subheader("시뮬레이션 결과")
        col1, col2, col3 = st.columns(3)
        col1.metric("총 생성된 점", f"{num_points:,}개")
        col2.metric("원 안의 점", f"{points_inside_circle:,}개")
        col3.metric("추정된 π 값", f"{pi_estimate:.6f}", delta=f"{pi_estimate - math.pi:.6f} (실제 π와의 차이)")

        # 시각화
        st.subheader("무작위 점 분포 시각화")
        df_points = pd.DataFrame({
            'x': points_x,
            'y': points_y,
            '위치': np.where(is_inside, '원 안', '원 밖')
        })

        # 성능을 위해 10000개 이상의 점은 샘플링하여 표시
        if num_points > 10000:
            st.info("점의 개수가 많아 10,000개만 샘플링하여 시각화합니다.")
            df_points = df_points.sample(n=10000)

        chart = alt.Chart(df_points).mark_circle(size=10, opacity=0.7).encode(
            x=alt.X('x', scale=alt.Scale(domain=[-1, 1])),
            y=alt.Y('y', scale=alt.Scale(domain=[-1, 1])),
            color=alt.Color('위치', legend=alt.Legend(title="점의 위치"), scale=alt.Scale(domain=['원 안', '원 밖'], range=['#1f77b4', '#ff7f0e'])),
            tooltip=['x', 'y', '위치']
        ).properties(
            width=600,
            height=600,
            title="몬테카를로 시뮬레이션 시각화"
        ).configure_axis(
            grid=False
        )
        st.altair_chart(chart, use_container_width=True)
