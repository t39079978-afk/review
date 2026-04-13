import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def classify_sentiment(review):
    """
    텍스트를 분석하여 감정 분류 (키워드 기준)
    """
    positive_keywords = ["만족", "추천", "좋아"]
    negative_keywords = ["실망", "불편", "아쉬움", "별로"]
    neutral_keywords = ["그저그럼", "그냥저냥"]

    review = str(review)

    if any(word in review for word in positive_keywords):
        return "긍정"
    elif any(word in review for word in negative_keywords):
        return "부정"
    else:
        return "중립"


def process_text_file(raw_text):
    """
    [후기 n]과 다음 줄의 내용을 하나로 그룹화하는 함수
    """
    lines = raw_text.splitlines()
    grouped_reviews = []
    current_content = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # [후기]로 시작하는 줄을 만나면 이전까지 모인 내용을 저장
        if line.startswith("[") and "]" in line:
            if current_content:
                grouped_reviews.append(current_content)
            current_content = ""  # 새로운 후기를 위해 초기화
        else:
            # 후기 번호가 아닌 일반 텍스트는 내용으로 합침
            current_content += " " + line

    # 마지막으로 남아있는 내용 추가
    if current_content:
        grouped_reviews.append(current_content.strip())

    return grouped_reviews


def plot_pie_chart(df):
    """
    감정 분석 결과를 원형 그래프로 시각화
    """
    counts = df["감정"].value_counts()

    fig = go.Figure(data=[go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.3,
        textinfo='label+percent',
        marker_colors=['#66b3ff', '#ff9999', '#99ff99']
    )])

    fig.update_layout(title_text="그룹화된 리뷰 감정 분석 비율")
    st.plotly_chart(fig, use_container_width=True)


def main():
    """
    메인 실행 함수
    """
    st.set_page_config(page_title="그룹화 감정 분석기")
    st.title("말머리 그룹화 리뷰 분석기")

    uploaded_file = st.file_uploader("텍스트 파일(.txt)을 업로드하세요", type=["txt"])

    if uploaded_file is not None:
        try:
            # 파일 읽기
            raw_text = uploaded_file.getvalue().decode("utf-8")

            # 1. 후기 제목과 내용을 그룹화
            reviews = process_text_file(raw_text)
            df = pd.DataFrame(reviews, columns=["review"])

            if df.empty:
                st.warning("분석할 리뷰 내용이 없습니다.")
                return

            # 2. 감정 분석 실행
            df['감정'] = df['review'].apply(classify_sentiment)

            # 분석 결과 확인 (그룹화가 잘 되었는지 미리보기)
            st.subheader("그룹화 분석 결과 요약")
            st.dataframe(df, use_container_width=True)

            # 3. 시각화
            plot_pie_chart(df)

        except Exception as e:
            st.error(f"오류 발생: {e}")
    else:
        st.info("파일을 업로드하면 [후기] 단위로 묶어서 분석을 시작합니다.")


if __name__ == "__main__":
    main()