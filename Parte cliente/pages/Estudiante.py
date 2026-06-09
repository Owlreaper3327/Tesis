import streamlit as st

st.write("Esta es la página de los estudiantes. Los vamos a vigilar ahora, hijos de pu**.")

if not 'autenticado' in st.session_state or not 'rol' in st.session_state:
    st.switch_page("Login.py")
else:
    if not st.session_state["autenticado"] or st.session_state["rol"] != "estudiante":
        st.switch_page("Login.py")