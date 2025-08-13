import streamlit as st

# 페이지 설정 + 이모티콘 타이틀
st.set_page_config(page_title="짱구 캐릭터 MBTI 🧸✨", page_icon="🧸")

st.markdown("<h1 style='text-align: center; color: #FF5733;'>짱구 캐릭터 MBTI 확인하기 🧸✨</h1>", unsafe_allow_html=True)
st.markdown("---")

characters = {
    "짱구": {
        "mbti": "ENFP",
        "image": "https://upload.wikimedia.org/wikipedia/en/8/82/Shinchan_character.png"
    },
    "유리": {
        "mbti": "ISFJ",
        "image": "https://static.wikia.nocookie.net/shinchan/images/2/2e/Yuri.png"
    },
    "철수": {
        "mbti": "ISTJ",
        "image": "https://static.wikia.nocookie.net/shinchan/images/6/6a/Bo-chan.png"
    },
    "맹구": {
        "mbti": "ESFP",
        "image": "https://static.wikia.nocookie.net/shinchan/images/8/85/Masukawa.png"
    }
}

choice = st.selectbox("👀 보고싶은 캐릭터를 선택하세요!", list(characters.keys()))

character_info = characters[choice]

st.markdown(f"### ✨ {choice}의 MBTI는 **{character_info['mbti']}** 입니다!")
st.image(character_info['image'], width=250, caption=f"{choice} 캐릭터 이미지")

st.markdown("---")
st.markdown(
    """
    <p style='text-align: center; font-size: 14px; color: gray;'>
    ※ MBTI는 재미로 보는 것입니다! 😊
    </p>
    """, unsafe_allow_html=True)
