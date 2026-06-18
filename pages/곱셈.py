import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="수학 탐정단 - 곱셈 방",
    page_icon="🟦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS
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
    
    .case-card {
        background: rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 30px;
        border: 3px solid #FFD700;
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
        animation: slideIn 0.6s ease-out;
    }
    
    .case-title {
        font-size: 1.5em;
        color: #FFD700;
        font-weight: 700;
        margin-bottom: 15px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .case-story {
        font-size: 1.15em;
        color: #FFFFFF;
        line-height: 1.8;
        margin-bottom: 20px;
        font-weight: 500;
    }
    
    .problem-box {
        background: rgba(255, 215, 0, 0.2);
        border: 2px solid #FFD700;
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        text-align: center;
    }
    
    .formula {
        font-size: 1.8em;
        color: #FFFFFF;
        font-weight: 700;
        margin: 15px 0;
        font-family: 'Courier New', monospace;
    }
    
    .suspects-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
        margin: 30px 0;
    }
    
    .suspect-btn {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%);
        color: white;
        border: none;
        padding: 20px;
        border-radius: 15px;
        font-size: 1.3em;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        box-shadow: 0px 5px 15px rgba(255, 107, 107, 0.4);
    }
    
    .suspect-btn:hover {
        transform: scale(1.1) translateY(-3px);
        box-shadow: 0px 10px 25px rgba(255, 107, 107, 0.6);
    }
    
    .success-message {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.4em;
        font-weight: 700;
        margin: 20px 0;
        box-shadow: 0px 10px 30px rgba(76, 175, 80, 0.4);
        animation: popIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .error-message {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 1.15em;
        font-weight: 600;
        margin: 20px 0;
        box-shadow: 0px 10px 25px rgba(255, 107, 107, 0.4);
        animation: shake 0.3s ease-in-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes popIn {
        0% {
            transform: scale(0.8);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# 세션 상태 초기화
if "difficulty" not in st.session_state:
    st.session_state.difficulty = None
if "case_data" not in st.session_state:
    st.session_state.case_data = None
if "correct_answer" not in st.session_state:
    st.session_state.correct_answer = None
if "show_success" not in st.session_state:
    st.session_state.show_success = False
if "show_error" not in st.session_state:
    st.session_state.show_error = False
if "solved_count" not in st.session_state:
    st.session_state.solved_count = 0

# 사건 스토리 데이터
cases_stories = [
    {"title": "🏛️ 박물관 보석 도난 사건", "story": "박물관에 전시된 진귀한 보석들이 어둠 속에서 사라졌어! 범인이 남긴 수학 암호를 풀어야만 범인의 정체가 드러날 거야!", "suspect_label": "🕵️ 용의자들의 도난 목록:"},
    {"title": "📚 도서관 희귀본 절도 사건", "story": "도서관의 귀중한 역사 서적이 베팅 계산지와 함께 발견되었어! 이 수학 암호를 풀면 책을 훔쳐간 범인이 누군지 알 수 있을 거야!", "suspect_label": "🔍 의심되는 범인들:"},
    {"title": "🎨 명화 도둑 작전 추적", "story": "유명 미술관의 귀중한 그림이 사라진 밤! 경비실에서 발견된 수학 노트가 범인을 향한 첫 번째 단서야! 이 수식을 풀어 범인의 신원을 밝혀봐!", "suspect_label": "🎭 체포 대상 용의자들:"},
    {"title": "💎 보석 강도 사건", "story": "한밤중에 보석 가게가 침입당했어! CCTV에서 강도가 남긴 수학 메모가 발견되었어. 이 계산식이 강도범의 신원을 숨기고 있어!", "suspect_label": "⚠️ 수배 중인 용의자들:"},
    {"title": "🏪 편의점 절도범 추적", "story": "편의점이 몰래 들어온 도둑에 의해 약탈당했어! 현장에 남겨진 수학 계산식이 범인의 정체를 암시하고 있어. 이 수수께끼를 풀어 범인을 잡아봐!", "suspect_label": "🚨 경찰이 찾는 범인들:"},
    {"title": "🚗 연쇄 자동차 도난 사건", "story": "주차장에서 연달아 자동차가 도난당했어! 모든 범행 현장에서 같은 형태의 수학 수수께끼가 발견되었어. 이 암호를 풀어 연쇄 도둑을 잡아봐!", "suspect_label": "🚗 자동차 도둑 용의자:"},
    {"title": "💰 은행 금고 침입 사건", "story": "은행 금고실의 보안이 뚫렸어! 범인이 남긴 고도의 수학 암호가 발견되었어. 이 계산을 풀면 침입자의 정체가 드러날 거야!", "suspect_label": "💳 은행 강도 용의자들:"},
    {"title": "👑 왕실 보물 도난 수사", "story": "왕궁의 역사적 보물이 밤새 사라졌어! 도둑이 남긴 도발적인 수학 문제가 경찰의 손에 들어왔어. 이 수식을 풀어야 왕실의 보물을 되찾을 수 있어!", "suspect_label": "👑 왕실 도둑 용의자들:"},
    {"title": "🎪 유명 공연장 소품 도난", "story": "공연장의 진귀한 소품들이 공연 밤에 도난당했어! 범인이 남긴 수학 계산식이 범행의 증거가 되고 있어. 이 암호를 풀어 범인을 체포해봐!", "suspect_label": "🎬 공연장 도둑 용의자:"},
    {"title": "🏆 스포츠 대회 금메달 사건", "story": "역대급 올림픽 금메달이 훔쳐졌어! 범인이 새겨놓은 수학 수수께끼가 수사의 전환점이 될 거야. 이 계산식을 풀면 금메달 도둑의 정체가 드러날 거야!", "suspect_label": "🥇 메달 도둑 용의자들:"},
    {"title": "🔐 비밀 연구소 자료 유출", "story": "비밀 연구소의 중요한 자료가 해킹당했어! 사이버 도둑이 남긴 수학 암호가 수사팀에게 넘어왔어. 이 코드를 해독하면 정보 도둑을 잡을 수 있어!", "suspect_label": "🔒 정보 도둑 용의자들:"},
    {"title": "⚡ 보석상 정밀 강도 사건", "story": "나라 최고의 보석상이 조직적인 강도단의 표적이 되었어! 범인들이 남긴 수학 계산식이 그들의 정체를 암시하고 있어. 이 수식을 풀어 조직을 소탕해봐!", "suspect_label": "🔴 강도단 용의자들:"},
]

# 용의자 생성 함수
def generate_suspects(correct_answer, count=4):
    suspects = {correct_answer}
    
    # 혼동될 만한 오답들 생성
    while len(suspects) < count:
        option = random.choice([
            correct_answer + random.randint(5, 50),
            correct_answer - random.randint(5, 50),
            correct_answer + random.randint(-20, 20),
            int(correct_answer * 0.9),
            int(correct_answer * 1.1),
        ])
        if option > 0:
            suspects.add(option)
    
    suspects_list = sorted(list(suspects))
    return suspects_list

# 문제 생성 함수
def generate_problem(difficulty):
    if difficulty == "보통":
        # (세 자리 수) × (몇십)
        num1 = random.randint(100, 999)
        num2 = random.randint(1, 9) * 10
    else:  # 어려움
        # (세 자리 수) × (몇십몇)
        num1 = random.randint(100, 999)
        num2 = random.randint(11, 99)
    
    answer = num1 * num2
    
    # 사건 선택
    case_info = random.choice(cases_stories)
    
    return {
        "num1": num1,
        "num2": num2,
        "answer": answer,
        "title": case_info["title"],
        "story": case_info["story"],
        "suspect_label": case_info["suspect_label"],
        "suspects": generate_suspects(answer)
    }

# 페이지 제목
st.markdown("""
<div style="text-align: center; padding: 30px 20px; animation: fadeIn 0.8s ease-out;">
    <div style="font-size: 3em; font-weight: 900; color: #FFD700; text-shadow: 4px 4px 0px rgba(0, 0, 0, 0.25);">
        🟦 곱셈 방 🟦
    </div>
    <div style="font-size: 1.3em; color: #FFFFFF; font-weight: 600; margin-top: 15px;">
        곱셈 수수께끼를 풀어 사건을 해결하세요!
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ===== 난이도 선택 화면 =====
if st.session_state.difficulty is None:
    st.markdown("""
    <div style="text-align: center; color: #FFFFFF; font-size: 1.3em; font-weight: 600; margin: 40px 0;">
        🎮 난이도를 선택하세요!
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([1, 2, 0.5, 2, 1])
    
    with col2:
        if st.button("⭐ 보통", use_container_width=True, key="difficulty_normal"):
            st.session_state.difficulty = "보통"
            st.session_state.case_data = generate_problem("보통")
            st.session_state.correct_answer = st.session_state.case_data["answer"]
            st.rerun()
    
    with col4:
        if st.button("⭐⭐⭐ 어려움", use_container_width=True, key="difficulty_hard"):
            st.session_state.difficulty = "어려움"
            st.session_state.case_data = generate_problem("어려움")
            st.session_state.correct_answer = st.session_state.case_data["answer"]
            st.rerun()
    
    st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <div style="color: #FFE5B4; font-size: 1.1em; margin-bottom: 20px;">
            💡 팁: 보통은 (세 자리 수) × (몇십)<br>
            어려움은 (세 자리 수) × (몇십몇) 형태입니다!
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== 게임 진행 화면 =====
else:
    # 난이도 표시 및 전체 돌아가기
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown(f"<div style='color: #FFD700; font-size: 1.1em; font-weight: 600;'>난이도: {st.session_state.difficulty} | 해결한 사건: {st.session_state.solved_count}</div>", unsafe_allow_html=True)
    with col3:
        if st.button("◀️ 돌아가기", use_container_width=True):
            st.session_state.difficulty = None
            st.session_state.case_data = None
            st.rerun()
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # 사건 카드
    if st.session_state.case_data:
        case = st.session_state.case_data
        
        st.markdown(f"""
        <div class="case-card">
            <div class="case-title">{case['title']}</div>
            <div class="case-story">
                {case['story']}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 문제 상자
        st.markdown(f"""
        <div class="problem-box">
            <div style="color: #FFE5B4; font-size: 1.1em; font-weight: 600; margin-bottom: 15px;">
                🔍 발견된 수학 단서:
            </div>
            <div class="formula">
                {case['num1']} × {case['num2']} = ?
            </div>
            <div style="color: #FFFFFF; font-size: 1.05em; margin-top: 15px;">
                이 계산의 답이 범인의 ID 번호입니다!
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="text-align: center; color: #FFFFFF; font-size: 1.2em; font-weight: 600; margin: 30px 0;">
            {case['suspect_label']}
        </div>
        """, unsafe_allow_html=True)
        
        # 용의자 버튼들
        cols = st.columns(len(case['suspects']))
        for idx, (col, suspect) in enumerate(zip(cols, case['suspects'])):
            with col:
                if st.button(str(suspect), use_container_width=True, key=f"suspect_{suspect}"):
                    if suspect == st.session_state.correct_answer:
                        st.session_state.show_success = True
                        st.session_state.show_error = False
                        st.session_state.solved_count += 1
                    else:
                        st.session_state.show_error = True
                        st.session_state.show_success = False
                    st.rerun()
        
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # 피드백 메시지
        if st.session_state.show_success:
            st.markdown("""
            <div class="success-message">
                🎉 정답입니다! 사건 해결! 🎉<br>
                <div style="font-size: 0.8em; margin-top: 10px;">
                    훌륭한 탐정 활동입니다!
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("📋 다음 사건 수사하기", use_container_width=True, key="next_case"):
                    st.session_state.case_data = generate_problem(st.session_state.difficulty)
                    st.session_state.correct_answer = st.session_state.case_data["answer"]
                    st.session_state.show_success = False
                    st.session_state.show_error = False
                    st.rerun()
        
        elif st.session_state.show_error:
            st.markdown(f"""
            <div class="error-message">
                ❌ 이건 아닙니다! 다시 계산해 보세요! ❌<br>
                <div style="font-size: 0.9em; margin-top: 8px;">
                    {case['num1']} × {case['num2']}를 다시 계산해 봅시다!
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <div style="text-align: center; color: #FFE5B4; font-size: 1.05em; margin-top: 25px; font-weight: 500;">
                💡 도움말: 천천히 단계별로 계산해 보세요!<br>
                먼저 일의 자리부터, 그 다음 십의 자리를 곱해봅시다!
            </div>
            """, unsafe_allow_html=True)
