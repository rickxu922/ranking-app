import streamlit as st
import pandas as pd

# =========================
# 標準化函式
# =========================
def standard(scores):
    avg = sum(scores) / len(scores)
    sd = (sum((x - avg) ** 2 for x in scores) / len(scores)) ** 0.5

    if sd == 0:
        return [0] * len(scores)

    return [(x - avg) / sd for x in scores]


# =========================
# UI 標題
# =========================
st.set_page_config(page_title="評分排名系統", page_icon="🏆")
st.title("評分排名系統")
st.write("輸入評分後，系統會自動標準化並計算排名")

st.divider()

# =========================
# 輸入人數
# =========================
people = st.number_input("請輸入人數", min_value=4, max_value=15, value=5)
people = int(people)

# =========================
# 輸入名字
# =========================
st.subheader("① 輸入名字")
names = []

for i in range(people):
    name = st.text_input(f"第 {i+1} 人名字", value=f"玩家{i+1}")
    names.append(name)

st.divider()

# =========================
# 輸入分數
# =========================
st.subheader("② 輸入評分")

score_data = []

for rater in range(people):
    st.markdown(f"### {names[rater]} 的評分")
    row_scores = []
    row_targets = []

    cols = st.columns(people)

    for target in range(people):
        with cols[target]:
            if rater == target:
                st.write("自己")
            else:
                score = st.number_input(
                    f"{names[target]}",
                    min_value=0.0,
                    max_value=100.0,
                    value=80.0,
                    key=f"{rater}-{target}"
                )
                row_scores.append(score)
                row_targets.append(target)

    score_data.append({
        "rater": rater,
        "targets": row_targets,
        "scores": row_scores
    })

st.divider()

# =========================
# 計算排名
# =========================
if st.button("🔥 計算排名"):

    records = []

    # 標準化
    for item in score_data:
        rater = item["rater"]
        targets = item["targets"]
        scores = item["scores"]

        std_scores = standard(scores)

        for i in range(len(targets)):
            records.append({
                "評分者": names[rater],
                "被評者": names[targets[i]],
                "標準化分數": std_scores[i]
            })

    # 加總
    total = {name: 0 for name in names}

    for r in records:
        total[r["被評者"]] += r["標準化分數"]

    # 排序
    ranking = sorted(total.items(), key=lambda x: x[1], reverse=True)

    st.subheader("從夯到拉銳評")

    # 顯示排名
    for i, (name, score) in enumerate(ranking):

        if i == 0:
            st.success(f"🏆 {name} 夯（{score:.3f}）")
            st.image("https://cdn-icons-png.flaticon.com/512/2583/2583344.png", width=120)

        elif i == 1:
            st.info(f"🥈 {name} 頂級（{score:.3f}）")

        elif i == 2:
            st.warning(f"🥉 {name} 人上人（{score:.3f}）")

        elif i == 3:
            st.warning(f"🥉 {name} NPC（{score:.3f}）")

        else:
            st.write(f"{name} 拉玩了💩 （{score:.3f}）")

    # 表格
    df = pd.DataFrame(ranking, columns=["姓名", "分數"])
    st.dataframe(df)

    # 圖表
    st.subheader("📊 分數圖")
    st.bar_chart(df.set_index("姓名"))