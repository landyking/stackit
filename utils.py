import streamlit as st

@st.dialog("Confirm")
def confirm_dialog(message: str,yes_func:callable = st.rerun,no_func: callable = st.rerun):
    st.write(message)
    col1,col2 = st.columns(2)
    if col1.button(label="Yes",type="primary",use_container_width=True):
        yes_func()
    if col2.button(label="No",type="secondary",use_container_width=True):
        no_func()