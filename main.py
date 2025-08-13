import streamlit as st

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

st.title("짱구 캐릭터 MBTI 확인하기")

choice = st.selectbox("캐릭터를 선택하세요", list(characters.keys()))

character_info = characters[choice]

st.subheader(f"{choice}의 MBTI는 {character_info['mbti']} 입니다.")
st.image(character_info['image'], width=200)  

