import streamlit as st
import cryptocode
import random
from time import time

crypto_pass = "may"

with open('user.txt', 'r') as f:
    temp = f.readlines()

with open('people.txt', 'r') as f:
    people = set(f.readline().split())

numbers = [f"{i}" for i in range(1, 10)]
random.seed(int(time()) * 10 % 1000)
random.shuffle(numbers)
    
user_dict = {}
assigned_numbers = set()
for item in temp:
    item.rstrip()
    items = item.split()
    user_dict[items[0]] = (items[1], items[2])
    assigned_numbers.add(cryptocode.decrypt(items[2], crypto_pass))

if 'menu' not in st.session_state:
    st.session_state.menu = "New"

if st.session_state.menu == "New":
    st.title("새로 순번 받기")
    name = st.text_input("이름")
    password = st.text_input("비밀번호")
    st.markdown(':red[자주 쓰는 비밀번호를 입력하지 마세요. 혹시 모를 해킹 위험이 있습니다.]')
    if st.button("확인"):
        if name in user_dict.keys():
            st.text("이미 순번을 받았습니다. 다시 보기를 해주세요.")
        elif name not in people:
            st.text("이름을 다시 확인해 주세요.")
        else:
            for n in numbers:
                if n not in assigned_numbers:
                    number_encoded = cryptocode.encrypt(n, crypto_pass)
                    password_encoded = cryptocode.encrypt(password, crypto_pass)
                    with open('user.txt', 'a') as f:
                        f.write(f"{name} {password_encoded} {number_encoded}\n")
                    st.text('당신의 순번은')
                    st.subheader(n)
                    break;
            else:
                st.text("번호가 이미 모두 할당되었습니다.")

if st.session_state.menu == "Find":
    st.title("순번 다시 보기")
    name = st.text_input("이름")
    password = st.text_input("비밀번호")
    if st.button("확인"):
        if name in user_dict.keys():
            if cryptocode.decrypt(user_dict[name][0], crypto_pass) == password:
                st.text('당신의 순번은')
                st.subheader(cryptocode.decrypt(user_dict[name][1], crypto_pass))
            else:
                st.text("비밀번호를 다시 확인해 주세요.")
        else:
            st.text("순번을 받지 않았거나 이름이 틀렸습니다.")

with st.sidebar:
    st.title("오 월")
    st.subheader("릴레이 소설 순번 뽑기 사이트")
    st.image('cat.jpeg')
    if st.button("새로 순번 받기", use_container_width=True):
        st.session_state.menu = "New"
    if st.button("순번 다시 보기", use_container_width=True):
        st.session_state.menu = "Find"
    st.text('')
    st.text("made by JaeOoO")
    