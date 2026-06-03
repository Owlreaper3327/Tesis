"""This is the login interface for the application"""

#imports go here
import streamlit as st
import requests


#functions go here
async def try_login(username, password):
    return True   


#main code goes here

st.title("Inicio de sesión", text_alignment="center")
result = ""

center_c = st.columns(3)[1]

formul = center_c.form(enter_to_submit=True, clear_on_submit=True, key="login"\
                 , width="content")

formul.write("Este formulario todavía no funciona")
username = formul.text_input(key="username", label="Nombre de usuario")
password = formul.text_input(key="password", label="Contraseña", type="password")

submit_btn = formul.form_submit_button(label="Iniciar", type="primary",\
                          help="Presione el botón tras llenar los campos del formulario con sus credenciales")

if submit_btn:
    st.write(submit_btn)

    if username and password:
        result = try_login(username, password)
        st.success(body="Inicio de sesión probado", title="Mensaje de retroalimentación")
        if result:
            st.write("This feature hasn't been implemented")