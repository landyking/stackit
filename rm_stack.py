import streamlit as st
import api
import json
import utils

def handle_remove_stack(stack_id):
    api.delete_stack(stack_id=stack_id)
    st.rerun()
    
ids = api.get_stack_ids()

selected_stack = st.selectbox(label="Select Stack",options=ids)
input_stack = st.text_input("Retype Stack")
if st.button(label="Remove Stack",disabled=selected_stack!=input_stack):
    utils.confirm_dialog(message=f"Do you want to remove stack: {selected_stack}",yes_func=lambda: handle_remove_stack(stack_id=input_stack))