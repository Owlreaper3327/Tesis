import streamlit as st

st.write("Esta es la página del profesor")

if 'autenticado' not in st.session_state or 'rol' not in st.session_state:
    st.switch_page("Login.py")

else:
    if not st.session_state["autenticado"] or st.session_state["rol"] != "profesor":
        st.session_state.clear()
        st.warning("No se tolerarán los intentos de trampa, fuera")
        st.switch_page("Login.py")