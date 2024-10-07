import streamlit as st
from streamlit_ace import st_ace,LANGUAGES
import api
import json
import utils
    
def handle_update_configuration(configurations,component,stack):
    api.apply_configurations(stack_id=stack,component_name=component,configurations=configurations)
    st.session_state['create_configuration_success'] = True
    st.rerun()

if st.session_state.pop("create_configuration_success",False):
    st.toast("Create configuration successful!")

stack_ids = api.get_stack_ids()
options_stacks = sorted(stack_ids)



selected_stack_id = st.selectbox(label="Stack",options=options_stacks)
    
stack_spec:dict = api.get_stack(selected_stack_id).pop("spec")
stack_spec_comps = stack_spec.pop("components",[])
selected_component:dict = st.selectbox(label="Component",options=stack_spec_comps,format_func=lambda it:it['name'])
if not selected_component:
    st.error(f"No component in stack: {selected_stack_id}")
    st.stop()

all_configurations: list[dict] = selected_component.pop("configurations",[])
with st.expander("Existing Configurations",expanded=True):
    if all_configurations:
        st.markdown('''\r\n'''.join([f"- {it['key']} `{it['use_as_file']}`" for it in all_configurations]))
    else:
        st.write("No configuration.")


config = {}

input_key = st.text_input(label="Key")
input_use_as_file = st.text_input(label="Use As File")
detect_language = utils.get_language_by_filename(input_use_as_file)
col1,col2 = st.columns(2,vertical_alignment="bottom")
input_is_sub_path = col1.checkbox(label="Is Sub Path")
input_encode_with_base64 = col2.checkbox(label="Encode with Base64")

col1,col2 = st.columns([0.6,0.4],vertical_alignment="bottom")
input_local_file_name = col1.text_input(label="Local File Name")
selected_language = col2.selectbox(label="Value Language",options=LANGUAGES,index=LANGUAGES.index(detect_language))
input_value = st_ace(language=selected_language)

config.update({
    "key":input_key,
    "use_as_file":input_use_as_file,
    "is_sub_path":input_is_sub_path,
    "encode_with_base64":input_encode_with_base64,
    "local_file_name":input_local_file_name,
    "value":input_value,
})

if st.button(label="Submit",type="primary",use_container_width=True):
    utils.confirm_dialog(message=f"Do you want to create new configuration for component: {selected_component['name']} in stack: {selected_stack_id} ?",
                         yes_func=lambda:handle_update_configuration(stack=selected_stack_id,
                                                                     component=selected_component['name'],
                                                                     configurations=[*all_configurations,config]))