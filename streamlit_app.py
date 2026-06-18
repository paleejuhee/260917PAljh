import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="수학 탐정단",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
if "game_started" not in st.session_state:
    st.session_state.game_started = False

# 커스텀 CSS 스타일
custom_css = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700;900&display=swap');
    
    * {
        font-family: 'Noto Sans KR', sans-serif !important;
    }
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 사이드바 숨김 */
    [data-testid="collapsedControl"] {
        display: none;
    }
    
    /* 메인 컨테이너 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* 제목 영역 */
    .title-container {
        text-align: center;
        padding: 50px 20px 20px;
        animation: fadeInDown 1s ease-out;
    }
    
    .main-title {
        font-size: 4.5em;
        font-weight: 900;
        color: #FFD700;
        text-shadow: 4px 4px 0px rgba(0, 0, 0, 0.25),
                     0px 0px 25px rgba(255, 215, 0, 0.6);
        margin: 0;
        padding: 10px 0;
        animation: bounce 1.2s ease-in-out infinite;
        letter-spacing: 2px;
    }
    
    .emoji-decoration {
        font-size: 2.5em;
        animation: float 3s ease-in-out infinite;
        margin: 10px 0;
    }
    
    .subtitle-text {
        font-size: 1.4em;
        color: #FFFFFF;
        margin-top: 25px;
        line-height: 1.8;
        font-weight: 600;
        animation: fadeIn 1.5s ease-out 0.3s both;
    }
    
    .welcome-message {
        font-size: 1.15em;
        color: #FFE5B4;
        margin-top: 15px;
        line-height: 1.9;
        animation: fadeIn 1.5s ease-out 0.5s both;
        font-weight: 500;
    }
    
    /* 버튼 영역 */
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 50px 20px 60px;
        animation: fadeInUp 1s ease-out 0.8s both;
    }
    
    .detective-button {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%);
        color: white;
        border: none;
        padding: 25px 60px;
        font-size: 1.4em;
        font-weight: 700;
        border-radius: 40px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.35),
                    0px 0px 30px rgba(255, 107, 107, 0.4);
        text-shadow: 2px 2px 3px rgba(0, 0, 0, 0.2);
        font-family: 'Noto Sans KR', sans-serif;
    }
    
    .detective-button:hover {
        transform: scale(1.12) translateY(-3px);
        box-shadow: 0px 15px 35px rgba(255, 107, 107, 0.6),
                    0px 0px 40px rgba(255, 200, 124, 0.5),
                    inset 0px 0px 20px rgba(255, 255, 255, 0.2);
        filter: brightness(1.1);
    }
    
    .detective-button:active {
        transform: scale(0.96) translateY(0px);
    }
    
    /* 하단 메시지 */
    .bottom-message {
        text-align: center;
        margin-top: 30px;
        color: white;
        font-size: 1.05em;
        line-height: 1.8;
        opacity: 0.95;
        animation: fadeIn 1.5s ease-out 1s both;
    }
    
    /* 애니메이션 정의 */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounce {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-15px);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-15px);
        }
    }
    
    @keyframes shine {
        0% {
            text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5);
        }
        50% {
            text-shadow: 0px 0px 25px rgba(255, 215, 0, 1);
        }
        100% {
            text-shadow: 0px 0px 10px rgba(255, 215, 0, 0.5);
        }
    }
    
    /* Streamlit 컴포넌트 조정 */
    .stMarkdown {
        text-align: center;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# 상단 데코레이션
st.markdown("""
<div class="emoji-decoration">
🔍 🎯 📚 🧩 ⭐
</div>
""", unsafe_allow_html=True)

# 메인 제목 및 안내 텍스트
st.markdown("""
<div class="title-container">
    <div class="main-title">수학 탐정단</div>
    <div class="subtitle-text">
        🔎 미스터리한 수학 수수께끼를 풀어보세요! 🔎
    </div>
    <div class="welcome-message">
        수학 탐정단에 오신 것을 환영합니다!<br>
        여러분도 지금부터 수학 탐정입니다.<br>
        함께 흥미로운 사건들을 해결해 봅시다!
    </div>
</div>
""", unsafe_allow_html=True)

# 시작 버튼
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🕵️ 사건 수사 시작하기 🕵️", use_container_width=True, key="start_game"):
        st.session_state.game_started = True
        st.rerun()

# 하단 메시지
if not st.session_state.game_started:
    st.markdown("""
    <div class="bottom-message">
        <div style="font-size: 1.2em; margin-bottom: 10px;">
            🎮 수학 탐정이 되어 숨겨진 패턴을 발견하고 🎮
        </div>
        <div>
            문제 해결의 즐거움을 느껴보세요!
        </div>
    </div>
    """, unsafe_allow_html=True)

# 추가 공간
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ===== 게임 시작 후 방 선택 화면 =====
if st.session_state.game_started:
    # 제목 변경
    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; animation: fadeIn 0.8s ease-out;">
        <div style="font-size: 3.5em; font-weight: 900; color: #FFD700; text-shadow: 4px 4px 0px rgba(0, 0, 0, 0.25); margin-bottom: 20px;">
            🔎 수사 방을 선택하세요! 🔎
        </div>
        <div style="font-size: 1.3em; color: #FFFFFF; font-weight: 600;">
            어떤 사건을 해결할 준비가 되셨나요?
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    
    # 방 선택 버튼
    col1, col2, col3 = st.columns([1, 1.5, 1.5])
    
    with col1:
        pass
    
    with col2:
        if st.button("🟦 곱셈 방 🟦", use_container_width=True, key="room_multiplication", help="곱셈의 신비를 풀어보세요!"):
            st.switch_page("pages/곱셈.py")
    
    with col3:
        if st.button("🟥 나눗셈 방 🟥", use_container_width=True, key="room_division", help="나눗셈의 비밀을 찾아보세요!"):
            st.switch_page("pages/나눗셈.py")
    
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # 돌아가기 버튼
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("◀️ 본부로 돌아가기", use_container_width=True, key="go_back"):
            st.session_state.game_started = False
            st.rerun()
