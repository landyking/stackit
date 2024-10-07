import streamlit as st
from streamlit_ace import st_ace
import api
import json
import utils


def handle_update_component(spec,name,stack_id):
    api.update_component(stack_id=stack_id,spec=spec,name_list=[name])
    st.session_state['component_update_success'] = True
    st.rerun()

if st.session_state.pop("component_update_success",False):
    st.success("Update component successful!")

stack_ids = api.get_stack_ids()
options_stacks = stack_ids

col1,col2 = st.columns(2)

selected_stack_id = col1.selectbox(label="Stack",options=options_stacks)
    
stack_spec:dict = api.get_stack(selected_stack_id).pop("spec")
stack_spec_comps = stack_spec.pop("components",[])
selected_component:dict = col2.selectbox(label="Component",options=stack_spec_comps,format_func=lambda it:it['name'])
if not selected_component:
    st.error(f"No component in stack: {selected_stack_id}")
    st.stop()

st.divider()

current_component = selected_component.copy()

origin_name = current_component.pop("name")
origin_instance_count = current_component.pop("instance_count")
origin_image = current_component.pop("image")
origin_image_version = current_component.pop("image_version")
origin_type = current_component.pop("type")
origin_enable = current_component.pop("enable",False)

default_properties = json.dumps(current_component,indent=4)

spec = {}
col_left,col_right = st.columns(2)

with col_right:
    
    col1,col2 = st.columns(2)
    comp_image = col1.text_input(label="Image",value=origin_image)
    comp_image_version = col2.text_input(label="Image Version",value=origin_image_version)
    
    col1,col2,col3 = st.columns([0.4,0.4,0.2],vertical_alignment="bottom")
    type_options = ['Stateless',"Stateful"];
    type_index = type_options.index(origin_type)
    comp_type= col1.selectbox(label="Type",options=type_options,index=type_index)
    comp_instance_count = col2.number_input(label="Instance Count",min_value=0,value=origin_instance_count)
    comp_enable = col3.checkbox(label="Enable",value=origin_enable)
    
    comp_properties = ""
    with st.expander(label="Properties"):
        comp_properties = st_ace(value=default_properties,language="json")
    # comp_properties = st.text_area(label="Properties",value=default_properties)
    properties: dict = {}
    try:
        properties = json.loads(comp_properties)
        if type(properties) != dict:
            properties = {}
            st.error("Invalid JSON format, not object.")
    except json.JSONDecodeError:
        st.error("Invalid JSON")
    
    spec.update({
        **properties,
        "name": origin_name,
        "image": comp_image,
        "image_version": comp_image_version,
        "instance_count": comp_instance_count,
        "enable":comp_enable,
        "type":comp_type
    })
    
    if st.button("Update",use_container_width=True,type="primary"):
        full_spec = {
            **stack_spec,
            "components":[spec]
        }
        utils.confirm_dialog(message=f"Do you want to update component: {origin_name} in stack: {selected_stack_id}?",
                             yes_func=lambda: handle_update_component(spec=full_spec,name=origin_name,stack_id=selected_stack_id))
with col_left:
    st.subheader("Component Spec YAML Preview:")
    st.json(spec)