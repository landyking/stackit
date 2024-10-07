import streamlit as st
import api
import json
import utils
from datetime import datetime

def handle_remove_stack(stack_id):
    api.delete_stack(stack_id=stack_id)
    st.session_state['stack_remove_success'] = True
    st.rerun()

if st.session_state.pop("stack_remove_success",False):
    st.success("Remove stack successful!")

ids = api.get_stack_ids()

selected_stack = st.selectbox(label="Select Stack",options=ids)
input_stack = st.text_input("Retype Stack")

same = selected_stack == input_stack
download_data = {}

if same:
    stack:dict = api.get_stack(stack_id=input_stack)
    download_data.update(stack.pop('spec',{}))

left,right = st.columns(2)

if left.button(label="Remove Stack",disabled=not same,type="primary",use_container_width=True):
    utils.confirm_dialog(message=f"Do you want to remove stack: {selected_stack}",yes_func=lambda: handle_remove_stack(stack_id=input_stack))
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
right.download_button(label="Backup Current Spec",
                      data=json.dumps(download_data,indent=4),
                      file_name=f"{input_stack}.{timestamp}.json",mime="text/json",disabled=not same,type="secondary",
                      use_container_width=True)