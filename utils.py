import streamlit as st

@st.dialog("Confirm")
def confirm_dialog(message: str,yes_func:callable = st.rerun,no_func: callable = st.rerun):
    st.write(message)
    col1,col2 = st.columns(2)
    if col1.button(label="Yes",type="primary",use_container_width=True):
        yes_func()
    if col2.button(label="No",type="secondary",use_container_width=True):
        no_func()

def get_language_by_filename(filename: str):
    filename = filename.lower()
    if filename.endswith('.yaml') or filename.endswith('.yml'):
        return "yaml"
    if filename.endswith('.json'):
        return "json5"
    if filename.endswith('.ini'):
        return "ini"
    if filename.endswith('.toml'):
        return "toml"
    if filename.endswith('.xml'):
        return "xml"
    return "plain_text"