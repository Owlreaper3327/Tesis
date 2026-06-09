"""Register page"""
import streamlit as st
import requests as rq
import st_keyup

if 'valid_username' not in st.session_state:
    st.session_state["valid_username"] = False
if 'valid_password' not in st.session_state:
    st.session_state["valid_password"] = False
if 'username' not in st.session_state:
    st.session_state["username"] = ""

group_list = ["FIO101", "FIO102", "FIO103", "FIO104",\
              "FIO201", "FIO202", "FIO203", "FIO204",\
              "FIO301", "FIO302", "FIO303", "FIO304",\
              "FIO401", "FIO402", "FIO403", "FIO404",\
              "FTI101", "FTI102", "FTI103", "FTI104",\
              "FTI201", "FTI202", "FTI203", "FTI204",\
              "FTI301", "FTI302", "FTI303", "FTI304",\
              "FTI401", "FTI402", "FTI403", "FTI404",\
              "FTE101", "FTE102", "FTE103", "FTE104",\
              "FTE201", "FTE202", "FTE203", "FTE204",\
              "FTE301", "FTE302", "FTE303", "FTE304",\
              "FTE401", "FTE402", "FTE403", "FTE404",\
              "FTL101", "FTL102", "FTL103", "FTL104",\
              "FTL201", "FTL202", "FTL203", "FTL204",\
              "FTL301", "FTL302", "FTL303", "FTL304",\
              "FTL401", "FTL402", "FTL403", "FTL404",\
              "CITEC101", "CITEC102", "CITEC103", "CITEC104",\
              "CITEC201", "CITEC202", "CITEC203", "CITEC204",\
              "CITEC301", "CITEC302", "CITEC303", "CITEC304",\
              "CITEC401", "CITEC402", "CITEC403", "CITEC404",\
              "FCI101", "FCI102", "FCI103", "FCI104",\
              "FCI201", "FCI202", "FCI203", "FCI204",\
              "FCI301", "FCI302", "FCI303", "FCI304",\
              "FCI401", "FCI402", "FCI403", "FCI404"]

lista_facultades = ["Facultad de Informática Organizacional",\
                    "Facultad de Tecnologías Interactivas",\
                    "Facultad de Ciberseguridad",\
                    "Facultad de Ciencia y Tecnologías Computacionales",\
                    "Facultad de Tecnologías Libres",\
                    "Facultad de Tecnologías Educativas"]

#functions goe here

def check_username(username:str):
    """Utility function to check the username with the api"""

    result = rq.get(f"http://127.0.0.1:8000/session/checkuser/{username}").json()

    st.session_state.valid_username = result["valid_username"]

def check_password(password:str, conf_pass:str):
    """Utility function to check if password it's well confirmed"""

    st.session_state["valid_password"] = password == conf_pass

def try_register(username:str, password:str, grupo:str, nombre:str, departamento:str, facultad:str):
    """Method that communicates with api to register new users"""

    if facultad:
        result = rq.post("http://127.0.0.1:8000/session/register/student",
                         data={
                             "username": username,
                             "password": password,
                             "grupo": grupo,
                             "nombre": nombre,
                             "facultad": facultad
                         }).json()

        if result:
            st.success("Estdudiante registrado con éxito")
            st.switch_page("Login.py")
        else:
            st.error("Algo ha fallado, vuelve a intentarlo")
    else:
        result = rq.post("http://127.0.0.1:8000/session/register/prof",
                         data={
                             "username": username,
                             "password": password,
                             "grupo": grupo,
                             "nombre": nombre,
                             "departamento": departamento
                         }).json()
        
        if "status" in result:
            st.success("Profesor registrado con éxito")
            st.switch_page("Login.py")
        else:
            st.error("Algo ha fallado, vuelve a intentarlo")


#Main code
st.title("Registro de usuario", text_alignment="center")
centered_c = st.columns(3)[1]

form = centered_c.form(border=True, key="formulario", enter_to_submit=False)

username = form.text_input(label="Nombre de usuario", help="Escriba su nombre de usuario, debe ser único",\
                           key="username")
password = form.text_input(label="Contraseña", type="password", key="password")
password_c = form.text_input(label="Confirmar contraseña", type="password",\
                            on_change=None, key="r_password")
grupo = form.selectbox(label="Grupo", options=group_list, key="grupo")
rol = st.selectbox(label="Rol", options=["Estudiante", "Profesor"])
nombre = form.text_input(label="Nombre completo", key="nombre")

departamento = False
facultad = False



if rol == "Profesor":
    departamento = form.text_input(label="Departamento", key="Departamento")
else:
    facultad = form.selectbox(label="Facultad", options=lista_facultades, key="facultad")

submit_btn = form.form_submit_button(key="sbt_btn")

if submit_btn:
    if username and password and password_c\
    and grupo and rol and nombre and (departamento or facultad):
        
        check_username(username)
        check_password(password, password_c)
        
        if st.session_state["valid_username"] and st.session_state["valid_password"]:
            try_register(username, password, grupo, nombre, departamento, facultad)
        else:
            if not st.session_state["valid_username"]:
                st.error("Nombre de usuario no disponible")
            if not st.session_state["valid_password"]:
                st.error("Contraseña confirmada incorrectamente")