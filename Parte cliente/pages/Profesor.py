import streamlit as st
import jwt
import requests as rq
from streamlit_cookies_manager import EncryptedCookieManager
import time

cookies = EncryptedCookieManager(password="cookie_39_Manager416")

if not cookies.ready():
    st.stop()

def close_session():
    st.session_state.clear()
    cookies.clear()
    st.switch_page("Login.py")

def restore_state():

    token = cookies.get("auth_token")
    
    try:
        decod = jwt.decode(token, options={"verify_signature" : False})

        if not 'autenticado' in st.session_state:
            st.session_state["autenticado"] = True
        if not 'rol' in st.session_state:
            st.session_state["rol"] = decod["tipo"]
        if not 'user' in st.session_state:
            st.session_state["user"] = decod["username"]
        if not 'grupo' in st.session_state:
            st.session_state["grupo"] = decod["grupo"]
        
    except jwt.exceptions.PyJWTError as e:
        close_session()


@st.fragment(run_every=20)
def check_auth():

    token = cookies.get("auth_token")
    try:
        response = rq.get("http://127.0.0.1:8000/session/checktoken", headers={"token" : f"Bearer {token}"})

        if response.status_code != 200:
            close_session()
        
        de_tok = jwt.decode(token, options={"verify_signature":False})
        
        if de_tok["tipo"] != "profesor":
            close_session()
        else:
            st.session_state.clear()
            restore_state()
        pass
    
    except rq.exceptions.RequestException as e:
        
        try:
            check = jwt.decode(token, options={"verify_signature": False})
            if check["exp"] < time.time():
                close_session()
        except jwt.exceptions.PyJWTError as ae:
            close_session()

check_auth()

st.title(f"Bienvenido, {st.session_state["user"]}", text_alignment="center")