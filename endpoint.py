import streamlit as st
import utils

old =  utils.load_settings()
# st.json(old)
col1,col2,col3 = st.columns([1,2,1])
with col2:
    st.subheader("Endpoint")
    st.divider()
    input_address = st.text_input(label="Address",placeholder="http://localhost:38080",value=old.get('address',''))
    input_need_auth = st.checkbox(label="Basic Authentication",value=old.get('need_auth','')=="1")
    input_user = ''
    input_password = ''
    if input_need_auth:
        input_user = st.text_input(label="User",value=old.get('user',''))
        input_password = st.text_input(label="Password",type="password",value=old.get('password',''))
    cols = st.columns(3)
    if cols[2].button(label="Save",type="primary",use_container_width=True):
        utils.save_settings({"address":input_address,
                             "need_auth":input_need_auth,
                             "user":input_user,
                             "password":input_password})
        st.toast("Save successful")
        st.rerun()