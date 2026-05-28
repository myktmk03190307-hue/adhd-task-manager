import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="ADHDタスク管理",
    page_icon="🧠",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f7e7df 0%, #f8f4f1 45%, #eadcf8 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", sans-serif;
}

.main-card {
    background: rgba(255,255,255,0.72);
    padding: 28px;
    border-radius: 32px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.08);
    margin-bottom: 24px;
}

.task-card {
    background: rgba(255,255,255,0.9);
    padding: 22px;
    border-radius: 28px;
    margin-bottom: 18px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.08);
}

.progress-card {
    background: #1f1f1f;
    color: white;
    padding: 24px;
    border-radius: 28px;
    margin-bottom: 24px;
}

.circle {
    width: 110px;
    height: 110px;
    border-radius: 50%;
    background: conic-gradient(#d7ef72 var(--progress), #ffffff22 0deg);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
}

.small-text {
    color: #777;
    font-size: 14px;
}

.stButton button {
    background-color: #1f1f1f;
    color: white;
    border-radius: 999px;
    border: none;
    padding: 10px 24px;
    font-weight: 600;
}

.stButton button:hover {
    background-color: #333333;
    color: white;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div,
.stDateInput input,
.stTimeInput input {
    border-radius: 18px !important;
}

h1, h2, h3 {
    color: #222;
}
</style>
""", unsafe_allow_html=True)

today = datetime.today().date()

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "done_tasks" not in st.session_state:
    st.session_state.done_tasks = []

st.markdown("""
<div class="main-card">
<h1>🧠 ADHDタスク管理</h1>
<p>完璧じゃなくてもOK。5分だけでもOK。</p>
</div>
""", unsafe_allow_html=True)

total_tasks = len(st.session_state.tasks) + len(st.session_state.done_tasks)
done_count = len(st.session_state.done_tasks)

if total_tasks == 0:
    progress = 0
else:
    progress = int((done_count / total_tasks) * 100)

st.markdown(f"""
<div class="progress-card">
<h3 style="color:white;">Today's Progress</h3>
<div style="display:flex; gap:28px; align-items:center;">
    <div class="circle" style="--progress:{progress * 3.6}deg;">{progress}%</div>
    <div>
        <p>✅ 完了：{done_count}</p>
        <p>📌 未完了：{len(st.session_state.tasks)}</p>
        <p>📅 今日：{today}</p>
    </div>
</div>
</div>
""", unsafe_allow_html=True)

memo = st.text_area("🧠 メモ", placeholder="今の気分・思いつき・忘れたくないことを書く")

st.divider()

st.subheader("➕ Add New Task")

task = st.text_input("Task Title / やること")

category = st.selectbox("分類", ["今", "明日", "あとで", "助け"])
priority = st.selectbox("優先順位", ["低", "中", "高"])
easy = st.selectbox("5分だけでできる？", ["はい", "いいえ"])
deadline = st.date_input("締切")
start_time = st.time_input("開始時間")
end_time = st.time_input("終了時間")

helper = ""
if category == "助け":
    helper = st.text_input("誰に頼む？")

if st.button("Create Task"):
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
            "頼む人": helper,
            "メモ": memo
        }

        st.session_state.tasks.append(task_data)
        st.success("追加できた！")

tired = st.checkbox("🌱 疲れてるモード：5分タスクだけ表示")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📌 今やる", "📅 明日", "🗂 あとで", "🫶 助け", "✅ 完了履歴"]
)

def show_tasks(category_name):
    filtered_tasks = [
        t for t in st.session_state.tasks
        if t["分類"] == category_name
    ]

    if len(filtered_tasks) == 0:
        st.info("まだタスクはありません")
        return

    for i, t in enumerate(filtered_tasks):
        if tired and t["5分"] != "はい":
            continue

        deadline_date = datetime.strptime(t["締切"], "%Y-%m-%d").date()
        days_left = (deadline_date - today).days

        if t["優先順位"] == "高":
            priority_label = "🔴 High Priority"
        elif t["優先順位"] == "中":
            priority_label = "🟠 Medium Priority"
        else:
            priority_label = "🟢 Low Priority"

        st.markdown(f"""
        <div class="task-card">
            <p class="small-text">{priority_label}</p>
            <h3>{t['内容']}</h3>
            <p class="small-text">
                ⏰ {t['開始']} - {t['終了']}<br>
                📅 締切：{t['締切']}<br>
                🌱 5分タスク：{t['5分']}
            </p>
        </div>
        """, unsafe_allow_html=True)

        if t["頼む人"] != "":
            st.write(f"🫶 頼む人：{t['頼む人']}")

        if days_left < 0:
            st.error("🚨 締切過ぎてる！")
        elif days_left == 0:
            st.warning("🔥 今日まで！")
        elif days_left == 1:
            st.warning("⚠️ 明日締切！")

        if st.button("完了 ✅", key=f"{category_name}_{i}_{t['内容']}"):
            st.session_state.done_tasks.append(t)
            st.session_state.tasks.remove(t)
            st.success("🎉 完了！えらい！")
            st.rerun()

with tab1:
    show_tasks("今")

with tab2:
    show_tasks("明日")

with tab3:
    show_tasks("あとで")

with tab4:
    show_tasks("助け")

with tab5:
    if len(st.session_state.done_tasks) == 0:
        st.info("まだ完了履歴はありません")
    else:
        for done in st.session_state.done_tasks:
            st.markdown(f"""
            <div class="task-card">
                <h3>✅ {done['内容']}</h3>
                <p class="small-text">
                    分類：{done['分類']}<br>
                    締切：{done['締切']}<br>
                    時間：{done['開始']} - {done['終了']}
                </p>
            </div>
            """, unsafe_allow_html=True)

st.divider()

if st.button("今日も頑張った！"):
    st.balloons()
    st.success("🎉 えらい！！今日もちゃんと進んでる！")