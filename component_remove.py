import streamlit as st
import api
import json
import utils
from datetime import datetime

def handle_remove_component(stack_id,component_name):
    api.delete_component(stack_id=stack_id,component_name=component_name)
    st.session_state['component_remove_success'] = True
    st.rerun()

if st.session_state.pop("component_remove_success",False):
    st.success("Remove component successful!")

ids = api.get_stack_ids()

selected_stack = st.selectbox(label="Select Stack",options=ids)

single_stack = api.get_stack(stack_id=selected_stack)
all_components = single_stack.get('spec',{}).get('components',[])

selected_component = st.selectbox(label="Component",options=all_components,format_func=lambda it:f"{it['name']} ({it['image']}:{it['image_version']})")

if not selected_component:
    st.error(f"No component in stack: {selected_stack}")
    st.stop()

input_component = st.text_input("Retype Component Name")

same = selected_component['name'] == input_component
download_data = json.dumps(selected_component,indent=4)

left,right = st.columns(2)

if left.button(label="Remove Component",disabled=not same,type="primary",use_container_width=True):
    utils.confirm_dialog(message=f"Do you want to remove component: {input_component} in stack: {selected_stack}",
                         yes_func=lambda: handle_remove_component(stack_id=selected_stack,component_name=input_component))
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
right.download_button(label="Backup Current Spec",
                      data=download_data,
                      file_name=f"{selected_stack}@{input_component}.{timestamp}.json",mime="text/json",disabled=not same,type="secondary",
                      use_container_width=True)