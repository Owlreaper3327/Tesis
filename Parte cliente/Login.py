"""This is the login interface for the application"""

#imports go here
import streamlit as st
import requests
import jwt

if 'user' not in st.session_state:
    st.session_state.user = ""
if 'rol' not in st.session_state:
    st.session_state.rol = ""
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False
if 'token' not in st.session_state:
    st.session_state.token = ""
if 'grupo' not in st.session_state:
    st.session_state.grupo = ""


#functions go here
def try_login(username, password):

    resp = requests.post("http://127.0.0.1:8000/session/auth", data={
        "username":username,
        "password":password 
    }, json={...})

    token = resp.text
    

    if token != "\"No autorizado\"":
        t = token.replace("\"", "")
        return t
    else:
        return False

def get_session():
    """Little method to grant access per role, idk, I didn't want to finish it down there"""

    if st.session_state["rol"] == "estudiante":
        st.switch_page("pages/Estudiante.py")
    else:
        st.switch_page("pages/Profesor.py")

def go_register():
    """Utility function to switch between login and register"""

    if 'register' not in st.session_state:
        st.session_state["register"] = "estudiante"
    
    st.switch_page("pages/Registrar.py")

#main code goes here

st.title("Inicio de sesión", text_alignment="center")
result = ""

center_c = st.columns(3)[1]

formul = center_c.form(enter_to_submit=True, clear_on_submit=True, key="login"\
                 , width="content")

formul.write("Este formulario ya funciona, pero todavía no está terminado")
username = formul.text_input(key="username", label="Nombre de usuario")
password = formul.text_input(key="password", label="Contraseña", type="password")

submit_btn = formul.form_submit_button(label="Iniciar", type="primary",\
                          help="Presione el botón tras llenar los campos del formulario con sus credenciales")

if submit_btn:
    if username and password:
        result = try_login(username, password)

        if result:
            tok = result
            decoded_tok = jwt.decode(result, options={"verify_signature": False})
            st.session_state["user"] = decoded_tok["username"]
            st.session_state["rol"] = decoded_tok["tipo"]
            st.session_state["autenticado"] = True
            st.session_state["grupo"] = decoded_tok["grupo"]
            st.session_state["token"] = tok

            get_session()
        else:
            adv = st.error(title="Credenciales inválidas", body="Nombre de usuario o contraseña incorrectos")
    else:
        st.warning("Debe rellenar todos los campos del formulario para continuar")

registro = center_c.button(label="Registrar")

if registro:
    go_register()
