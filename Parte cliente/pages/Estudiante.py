import streamlit as st
import requests as rq
from streamlit_cookies_manager import EncryptedCookieManager
import jwt
import time

def close_session():
    st.session_state.clear()
    cookies.clear()
    st.switch_page("Login.py")


cookies = EncryptedCookieManager(password="cookie_39_Manager416")
com = False

if not cookies.ready():
    st.stop()

def is_session_established():

    is_sesion = True

    if not 'autenticado' in st.session_state:
        is_sesion = False
    if not 'rol' in st.session_state:
        is_sesion = False
    if not 'user' in st.session_state:
        is_sesion = False
    if not 'nombre' in st.session_state:
        is_sesion = False
    
    if not is_sesion:
        st.session_state.clear()
    
    return is_sesion


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
        
        restore_state()
        pass
    
    except rq.exceptions.RequestException as e:
        
        check = jwt.decode(token, options={"verify_signature": False})
        if check["exp"] < time.time():
            close_session()

check_auth()

if not 'acuerdo' in st.session_state:
    st.session_state["acuerdo"] = False

if not st.session_state["acuerdo"]:

    pop = st.popover("Acuerdo de privacidad")
    pop.markdown("Este sistema utiliza tus datos para asegurar la integridad académica")
    pop.markdown("Se incluyen datos de las ventanas abiertas en tu sistema, así como los sitios a los que accedes")
    pop.markdown("También se rastrearán los movimientos que hagas mediante teclado y ratón")
    pop.markdown("""No es el objetivo violentar la privacidad de nuestros usuarios
                    ¿Está de acuerdo en que usemos esos datos?""")
        
    ap = pop.checkbox(label="Estoy de acuerdo en que usen mis datos")
    but = pop.button(label="Confirmar")

    if but:
        if not ap:
            st.session_state.clear()
            st.switch_page("Login.py")
        else:
            st.toast("Gracias")
            st.session_state["acuerdo"] = True
else:
    pop = st.popover("Acuerdo de privacidad", disabled=True)
