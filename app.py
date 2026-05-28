import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="ADHDタスク管理",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
<style>
.main {
    background-color: #f8f6f2;
}
.stButton button {
    background-color: #d8c3a5;
    color: black;
    border-radius: 15px;
    border: none;
    padding: 10px 20px;
}
.task-card {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.small-text {
    color: gray;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧠 ADHDタスク管理")
st.write("完璧じゃなくてもOK")
st.write("5分だけでもOK")

today = datetime.today().date()
st.write(f"今日：{today}")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "done_tasks" not in st.session_state:
    st.session_state.done_tasks = []

memo = st.text_area("🧠 メモ", placeholder="今の気分やメモを書く")

task = st.text_input("やること")

category = st.selectbox("分類", ["今", "明日", "あとで", "助け"])
priority = st.selectbox("優先順位", ["高", "中", "低"])
easy = st.selectbox("5分だけでできる？", ["はい", "いいえ"])
deadline = st.date_input("締切")
start_time = st.time_input("開始時間")
end_time = st.time_input("終了時間")

helper = ""
if category == "助け":
    helper = st.text_input("誰に頼む？")

if st.button("追加"):
    if task.strip() == "":
        st.warning("やることを入力してね")
    else:
        task_data = {
            "内容": task,
            "分類": category,
            "優先順位": priority,
            "5分": easy,
            "締切": str(deadline),
            "開始": str(start_time),
            "終了": str(end_time),
            "頼む人": helper
        }

        st.session_state.tasks.append(task_data)
        st.success("追加できた！")

tired = st.checkbox("疲れてるモード")

st.divider()

def show_tasks(title, category_name):
    st.subheader(title)

    filtered_tasks = [
        t for t in st.session_state.tasks
        if t["分類"] == category_name
    ]

    for i, t in enumerate(filtered_tasks):
        if tired and t["5分"] != "はい":
            continue

        st.markdown(
            f"""
            <div class="task-card">
                <h3>📌 {t['内容']}</h3>
                <p class="small-text">
                    優先順位：{t['優先順位']}<br>
                    締切：{t['締切']}<br>
                    開始：{t['開始']}<br>
                    終了：{t['終了']}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if t["頼む人"] != "":
            st.write(f"🫶 頼む人：{t['頼む人']}")

        deadline_date = datetime.strptime(t["締切"], "%Y-%m-%d").date()
        days_left = (deadline_date - today).days

        if days_left < 0:
            st.error("🚨 締切過ぎてる！")
        elif days_left == 0:
            st.warning("🔥 今日まで！")
        elif days_left == 1:
            st.warning("⚠️ 明日締切！")

        if st.button("完了 ✅", key=f"{category_name}_{i}_{t['内容']}"):
            st.session_state.done_tasks.append(t["内容"])
            st.session_state.tasks.remove(t)
            st.success("🎉 完了！えらい！")
            st.rerun()

        st.divider()

show_tasks("📌 今やる", "今")
show_tasks("📅 明日やる", "明日")
show_tasks("🗂 あとで", "あとで")
show_tasks("🫶 人に助けを求める", "助け")

st.divider()

st.subheader("✅ 完了履歴")
for done in st.session_state.done_tasks:
    st.write(f"・{done}")

st.divider()

if st.button("今日も頑張った！"):
    st.balloons()
    st.success("🎉 えらい！！")