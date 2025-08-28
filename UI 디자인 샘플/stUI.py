import streamlit as st
import io, csv

# ---------------------------
# 3.1 페이지 설정
# ---------------------------
st.set_page_config(page_title="패스포인트", page_icon="💬", layout="wide", initial_sidebar_state="expanded")

# ---------------------------
# 3.2 최소한의 CSS 스타일
# ---------------------------
st.markdown(
    """
    <style>
      /* 말풍선 */
      .bubble-user {background:#f0f0f0;color:#000;padding:0.7rem 1rem;border-radius:14px;display:inline-block;}
      .bubble-assistant {background:#d3f9d8;color:#000;padding:0.7rem 1rem;border-radius:14px;display:inline-block;}
      .muted {color:#6b7280;font-size:0.85rem}
      /* 카드 모양 컨테이너 */
      [data-testid="stVerticalBlock"]>.st-emotion-cache-ue6h4q {padding:0.6rem 0.8rem;border-radius:12px;background:#ffffff;}
      /* 사이드바 너비 힌트 */
      section[data-testid="stSidebar"] {min-width: 300px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------
# 3.3 앱 상태 (모든 페이지 공유)
# ---------------------------
if "profile" not in st.session_state:
    st.session_state.profile = {"name": "게스트", "avatar": None}
if "settings" not in st.session_state:
    st.session_state.settings = {"model": "demo", "temperature": 0.7, "theme": "system"}
if "chat" not in st.session_state:
    st.session_state.chat = {"history": []}  # 역할과 내용을 담은 딕셔너리 목록
if "docs" not in st.session_state:
    st.session_state.docs = {"files": [], "notes": ""}

# ---------------------------
# 3.4 내비게이션 (커스텀 라우터)
# ---------------------------
with st.sidebar:
    st.header("내비게이션")
    page = st.radio("이동", ["메인", "채팅", "문서", "설정", "사용자"], label_visibility="collapsed")

# ---------------------------
# 3.5 페이지 함수
# ---------------------------

def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div style='padding:1rem;border-radius:16px;background:#f5f5f5'>
          <h1 style='margin:0;color:#2e7d32'>{title}</h1>
          <p style='margin:0.3rem 0 0 0;color:#555'>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

def page_title(text: str):
    st.markdown(f"<h1 style='color:#2e7d32'>{text}</h1>", unsafe_allow_html=True)

# --- 메인 ---

def page_home():
    hero("💬 패스포인트", "패스포인트는 자기소개서 작성 도우미 챗봇 프로그램입니다.")
    st.write("by 숭실대ICT PassPoint")
    # c1, c2, c3 = st.columns(3)
    # c1.metric("대화 수", len([m for m in st.session_state.chat["history"] if m["role"]=="user"]))
    # c2.metric("챗봇 답변 수", len([m for m in st.session_state.chat["history"] if m["role"]=="assistant"]))
    # c3.metric("업로드된 파일 수", len(st.session_state.docs.get("files", [])))

# --- 채팅 로직 (플레이스홀더) ---

def simple_answer(user_text: str) -> str:
    # 매우 단순한 예: 메모에서 내용을 찾아 보여줍니다
    notes = (st.session_state.docs.get("notes") or "").lower()
    if user_text and user_text.lower() in notes:
        return "메모에서 찾았습니다. 일부만 보여드릴게요: " + notes[:300]
    return f"사용자 입력: {user_text}. (여기에 모델 호출을 구현하세요.)"

# --- 채팅 페이지 ---

def page_chat():
    page_title("채팅")

    # Render history
    for msg in st.session_state.chat["history"]:
        with st.chat_message(msg["role"]):
            css = "bubble-user" if msg["role"]=="user" else "bubble-assistant"
            st.markdown(f"<div class='{css}'>{msg['content']}</div>", unsafe_allow_html=True)

    # Input
    user_text = st.chat_input("메시지를 입력하세요…")
    if user_text:
        st.session_state.chat["history"].append({"role": "user", "content": user_text})
        with st.chat_message("user"):
            st.markdown(f"<div class='bubble-user'>{user_text}</div>", unsafe_allow_html=True)

        reply = simple_answer(user_text)
        st.session_state.chat["history"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(f"<div class='bubble-assistant'>{reply}</div>", unsafe_allow_html=True)

    st.divider()
    col1, col2, col3 = st.columns(3)
    if col1.button("채팅 지우기"):
        st.session_state.chat["history"] = []
        st.toast("채팅이 지워졌습니다.")
    if col2.button("마지막 답변 복사") and any(m["role"]=="assistant" for m in st.session_state.chat["history"]):
        last = [m for m in st.session_state.chat["history"] if m["role"]=="assistant"][-1]["content"]
        st.code(last)
    if col3.download_button("대화 내역 다운로드 (JSON)", str(st.session_state.chat["history"])):
        pass

# --- 문서 페이지 ---

def page_documents():
    page_title("문서")
    tabs = st.tabs(["업로드", "미리보기", "메모"])  # 메모는 데모 채팅에 사용

    with tabs[0]:
        uploaded = st.file_uploader(
            "파일 업로드 (TXT, CSV, PDF, PNG, JPG)",
            type=["txt","csv","pdf","png","jpg","jpeg"],
            accept_multiple_files=True,
        )
        if uploaded:
            st.session_state.docs["files"] = uploaded
            st.success(f"파일 {len(uploaded)}개가 저장되었습니다. 미리보기 탭으로 이동하세요.")

    with tabs[1]:
        files = st.session_state.docs.get("files", [])
        if not files:
            st.info("아직 업로드된 파일이 없습니다.")
        else:
            for f in files:
                st.write("—", f.name)
                if f.type == "text/plain":
                    st.text(f.read().decode("utf-8")[:500]); f.seek(0)
                elif f.type in ("text/csv", "application/vnd.ms-excel"):
                    # csv 모듈 사용 (pandas 없음)
                    content = io.StringIO(f.read().decode("utf-8")); f.seek(0)
                    reader = csv.reader(content)
                    rows = list(reader)[:10]
                    st.table(rows)
                elif f.type.startswith("image/"):
                    st.image(f, use_container_width=True); f.seek(0)
                else:
                    st.caption("미리보기가 구현되지 않았습니다 — 추후 처리를 위해 저장되었습니다.")

    with tabs[2]:
        st.caption("데모 채팅을 위해 간단한 메모나 주요 텍스트를 추가하세요.")
        st.session_state.docs["notes"] = st.text_area("참고 메모", value=st.session_state.docs.get("notes", ""), height=160)
        st.success("메모가 저장되었습니다.")

# --- 설정 페이지 ---

def page_settings():
    page_title("설정")
    with st.form("settings_form"):
        model_options = {"데모": "demo", "GPT유사": "gpt-like", "로컬": "local"}
        current_model_display = [k for k, v in model_options.items() if v == st.session_state.settings["model"]][0]
        model_display = st.selectbox("모델", list(model_options.keys()), index=list(model_options.keys()).index(current_model_display))
        model = model_options[model_display]
        temperature = st.slider("창의성(온도)", 0.0, 1.0, st.session_state.settings["temperature"], 0.05)
        theme_options = {"시스템": "system", "라이트": "light", "다크": "dark"}
        current_theme_display = [k for k, v in theme_options.items() if v == st.session_state.settings["theme"]][0]
        theme_display = st.radio("테마", list(theme_options.keys()), index=list(theme_options.keys()).index(current_theme_display))
        theme = theme_options[theme_display]
        submitted = st.form_submit_button("설정 저장")
    if submitted:
        st.session_state.settings.update({"model": model, "temperature": temperature, "theme": theme})
        st.success("설정이 저장되었습니다.")

# --- 사용자 페이지 ---

def page_user():
    page_title("사용자")
    c1, c2 = st.columns([1,3])
    with c1:
        if st.session_state.profile["avatar"]:
            st.image(st.session_state.profile["avatar"], caption="아바타", use_container_width=True)
        else:
            st.markdown("<div class='muted'>아바타가 없습니다</div>", unsafe_allow_html=True)
    with c2:
        with st.form("profile_form"):
            name = st.text_input("표시 이름", value=st.session_state.profile.get("name", "게스트"))
            avatar = st.file_uploader("아바타 업로드", type=["png","jpg","jpeg"])
            ok = st.form_submit_button("프로필 저장")
        if ok:
            st.session_state.profile["name"] = name or "게스트"
            if avatar:
                st.session_state.profile["avatar"] = avatar
            st.success("프로필이 업데이트되었습니다.")

# ---------------------------
# 3.6 라우터 스위치
# ---------------------------
if page == "메인":
    page_home()
elif page == "채팅":
    page_chat()
elif page == "문서":
    page_documents()
elif page == "설정":
    page_settings()
elif page == "사용자":
    page_user()
