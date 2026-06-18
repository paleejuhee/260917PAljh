import streamlit as st
import random

# 페이지 설정
st.set_page_config(
    page_title="수학 탐정단 - 나눗셈 방",
    page_icon="🟥",
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
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%);
        min-height: 100vh;
    }
    
    .stApp {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E72 100%);
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
    {"title": "🏴‍☠️ 해적 보물섬 동전 수수께끼", "story": "숨겨진 보물섬에서 해적이 금화를 감췄어요! 나눗셈 암호를 풀어 보물의 정확한 개수를 찾아봅시다!", "suspect_label": "🏴‍☠️ 의심되는 해적들:"},
    {"title": "🐱 고양이 보호소 미스터리", "story": "고양이 보호소의 사료가 없어졌어요! 남겨진 수학 단서로 각 고양이가 먹을 사료의 개수를 찾아주세요!", "suspect_label": "🐱 귀여운 고양이들:"},
    {"title": "🔐 비밀 요원의 암호 해독", "story": "국제 스파이가 남긴 암호가 발견되었어요! 나눗셈을 풀어 비밀 암호를 해독하세요!", "suspect_label": "🕵️ 의심되는 스파이들:"},
    {"title": "🚀 우주선 자원 배분 사건", "story": "달 기지에 도착했는데 우주식량이 평등하게 배분되지 않았어요! 수학 계산으로 올바른 배분을 찾으세요!", "suspect_label": "🚀 우주 탐험대원들:"},
    {"title": "🎪 마술사의 카드 비밀", "story": "마술사의 신비한 카드 트릭을 풀어봅시다! 나눗셈 수수께끼를 풀면 마술의 비밀이 드러날 거예요!", "suspect_label": "🎴 숨겨진 카드들:"},
    {"title": "👑 왕국의 보물 나누기", "story": "왕국의 보물실에서 발견된 보석들을 공평하게 배분해야 해요! 수학 단서로 올바른 개수를 찾아주세요!", "suspect_label": "💎 반짝이는 보석들:"},
    {"title": "🎬 영화 촬영장 소품 미스터리", "story": "영화 촬영장의 소품들이 섞여버렸어요! 나눗셈 계산으로 올바른 배치를 찾아봅시다!", "suspect_label": "🎭 배우들의 소품:"},
    {"title": "🏆 스포츠 대회 상금 수수께끼", "story": "우승팀의 상금 배분에 문제가 생겼어요! 수학으로 공평한 상금 배분을 계산해주세요!", "suspect_label": "⭐ 선수들의 상금:"},
    {"title": "🐉 용의 보물 동굴 탐험", "story": "전설의 용이 숨긴 보물 동굴에 들어갔어요! 나눗셈 마법을 풀어 금색 동전의 개수를 맞춰봅시다!", "suspect_label": "✨ 신비로운 금화들:"},
    {"title": "🎨 미술관 색칠 보드 수수께끼", "story": "유명 화가의 작품을 복원해야 해요! 각 색깔별로 필요한 물감의 양을 나눗셈으로 계산해주세요!", "suspect_label": "🎨 사용할 물감:"},
    {"title": "🍫 초콜릿 공장 배분 사건", "story": "초콜릿 공장에서 만든 초콜릿을 포장해야 하는데 상자 개수가 부족해요! 수학으로 정확한 포장 방법을 찾아봅시다!", "suspect_label": "🍫 초콜릿 상자들:"},
    {"title": "🌟 별 관찰소 신비의 수", "story": "천문대에서 발견된 별들의 그룹을 분석해야 해요! 나눗셈으로 올바른 별의 개수를 찾아주세요!", "suspect_label": "⭐ 밤하늘의 별들:"},
]

# 용의자 생성 함수
def generate_suspects(correct_answer, count=4):
    suspects = {correct_answer}
    
    # 혼동될 만한 오답들 생성
    while len(suspects) < count:
        option = random.choice([
            correct_answer + random.randint(1, 3) if correct_answer + 3 <= 9 else correct_answer - random.randint(1, 3),
            correct_answer - random.randint(1, 3) if correct_answer > 1 else correct_answer + random.randint(1, 3),
            correct_answer + 1 if correct_answer < 9 else correct_answer - 1,
            correct_answer - 1 if correct_answer > 1 else correct_answer + 1,
            random.randint(1, 9),
        ])
        if option > 0 and option <= 9:
            suspects.add(option)
    
    suspects_list = sorted(list(suspects))
    return suspects_list

# 문제 생성 함수
def generate_problem(difficulty):
    if difficulty == "보통":
        # (두 자리 수) ÷ (두 자리 수) = 한 자리 수
        divisor = random.randint(10, 99)
        quotient = random.randint(1, 9)
        dividend = divisor * quotient
    else:  # 어려움
        # (세 자리 수) ÷ (두 자리 수) = 한 자리 수
        divisor = random.randint(10, 99)
        quotient = random.randint(1, 9)
        dividend = divisor * quotient
    
    answer = quotient
    
    # 사건 선택
    case_info = random.choice(cases_stories)
    
    return {
        "dividend": dividend,
        "divisor": divisor,
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
        🟥 나눗셈 방 🟥
    </div>
    <div style="font-size: 1.3em; color: #FFFFFF; font-weight: 600; margin-top: 15px;">
        나눗셈 수수께끼를 풀어 사건을 해결하세요!
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
            💡 팁: 보통은 (두 자리 수) ÷ (두 자리 수)<br>
            어려움은 (세 자리 수) ÷ (두 자리 수) 형태입니다!
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
                {case['dividend']} ÷ {case['divisor']} = ?
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
                    {case['dividend']} ÷ {case['divisor']}를 다시 계산해 봅시다!
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="text-align: center; color: #FFE5B4; font-size: 1.05em; margin-top: 25px; font-weight: 500;">
                💡 도움말: {case['divisor']}를 몇 번 더하면 {case['dividend']}이 될까요?<br>
                또는 {case['divisor']} × ? = {case['dividend']}를 생각해 보세요!
            </div>
            """, unsafe_allow_html=True)
