import streamlit as st
from streamlit_ace import st_ace,LANGUAGES
import api
import json
import utils
import time

def configuration_update(stack_id: str, component: dict):
    def handle_update_configuration(configurations,component,stack):
        api.apply_configurations(stack_id=stack,component_name=component,configurations=configurations)
        st.session_state['update_configuration_success'] = True
        st.rerun()

    if st.session_state.pop("update_configuration_success",False):
        st.toast("Update configuration successful!")

    selected_stack_id = stack_id
        
    selected_component:dict = component
    if not selected_component:
        st.error(f"No component in stack: {selected_stack_id}")
        st.stop()

    all_configurations: list[dict] = selected_component.pop("configurations",[])
    all_configurations = sorted(all_configurations,key=lambda it:it['key'])
    selected_configuration:dict = st.selectbox(label="Configuration",options=all_configurations,format_func=lambda it:f"{it['key']} ({it['use_as_file']})")
    if not selected_configuration:
        st.error(f"No configuration in component: {selected_component['name']}")
        st.stop()

    config = selected_configuration.copy()

    input_use_as_file = st.text_input(label="Use As File",value=config.get("use_as_file"))

    col1,col2 = st.columns(2,vertical_alignment="bottom")
    input_is_sub_path = col1.checkbox(label="Is Sub Path",value=config.get("is_sub_path"))
    input_encode_with_base64 = col2.checkbox(label="Encode with Base64",value=config.get("encode_with_base64"))

    col1,col2 = st.columns([0.6,0.4],vertical_alignment="bottom")
    input_local_file_name = col1.text_input(label="Local File Name",value=config.get("local_file_name"))
    detect_language = utils.get_language_by_filename(input_use_as_file)
    selected_language = col2.selectbox(label="Value Language",options=LANGUAGES,index=LANGUAGES.index(detect_language))
    input_value = st_ace(value=config.get("value"),language=selected_language)

    config.update({
        "use_as_file":input_use_as_file,
        "is_sub_path":input_is_sub_path,
        "encode_with_base64":input_encode_with_base64,
        "local_file_name":input_local_file_name,
        "value":input_value,
    })

    col1,col2 = st.columns(2)
    if col1.button(label="Update",type="primary",use_container_width=True):
        new_configurations = [
            *[it for it in all_configurations if it['key'] != config['key']],
            config
        ]
        new_configurations = sorted(new_configurations,key=lambda it:it['key'])
        utils.confirm_dialog(message=f"Do you want to update this configuration for component: {selected_component['name']} in stack: {selected_stack_id} ?",
                            yes_func=lambda:handle_update_configuration(
                                stack=selected_stack_id,
                                component=selected_component['name'],
                                configurations=new_configurations))
    if col2.button(label="Remove",type="primary",use_container_width=True):
        new_configurations = [
            *[it for it in all_configurations if it['key'] != config['key']]
        ]
        new_configurations = sorted(new_configurations,key=lambda it:it['key'])
        utils.confirm_dialog(message=f"Do you want to remove this configuration for component: {selected_component['name']} in stack: {selected_stack_id} ?",
                            yes_func=lambda:handle_update_configuration(
                                stack=selected_stack_id,
                                component=selected_component['name'],
                                configurations=new_configurations))