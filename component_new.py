import streamlit as st
from streamlit_ace import st_ace
import api
import json
import utils

def component_new(stack_id: str):
    def handle_create_component(spec,name,stack_id):
        api.create_component(stack_id=stack_id,spec=spec,name_list=[name])
        st.session_state['component_create_success'] = True
        st.rerun()

    if st.session_state.pop("component_create_success",False):
        st.success("Create component successful!")

    
    spec = {}
    col_left,col_right = st.columns(2)

    default_properties ='''{
        "liveness_probe_command": [],
        "readiness_probe_command": [],
        "readiness_probe_http_getpath": "",
        "readiness_probe_http_port": 0,
        "readiness_probe_tcp_port": 0,
        "dependency_components": [],
        "resource_require": {"cpu": "200m","memory": "256Mi"},
        "resource_limit": {"cpu": "1200m","memory": "2048Mi"},
        "configurations": [],
        "initial_delay_seconds": 10,
        "probe_timeout_seconds": 3,
        "probe_period_seconds": 3,
        "health_check_retry_times": 10,
        "health_check_interval": 10,
        "named_ports":[{"name":"httport","port":0,"target_port":0}],
        "node_port_policy": "default",
        "env_variables": [{"name":"test_name","value":"test_value"}],
        "MaxHealthCheckPeriodTime": 10000000000,
        "container_extensions": {},
        "topology_spread_constraints": []
    }'''
    selected_stack_id = stack_id
    with col_right:
        
        stack_spec:dict = api.get_stack(selected_stack_id).pop("spec")
        stack_spec_comps = stack_spec.pop("components",[])
        with st.expander(label="Existing Components",expanded=True):
            tmp = ", ".join([f"`{it['name']}`" for it in stack_spec_comps])
            st.markdown(f"{tmp}" if tmp else "No components." )
        
        col1,col2 = st.columns(2)
        comp_name = col1.text_input(label="Name")
        comp_instance_count = col2.number_input(label="Instance Count",value=1,min_value=0)
        
        col1,col2 = st.columns(2)
        comp_image = col1.text_input(label="Image")
        comp_image_version = col2.text_input(label="Image Version")
        
        col1,col2 = st.columns(2,vertical_alignment="bottom")
        comp_type= col1.selectbox(label="Type",options=['Stateless',"Stateful"])
        comp_enable = col2.checkbox(label="Enable")
        
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
            "name": comp_name,
            "image": comp_image,
            "image_version": comp_image_version,
            "instance_count": comp_instance_count,
            "enable":comp_enable,
            "type":comp_type
        })
        
        if st.button("Submit",use_container_width=True,type="primary"):
            full_spec = {
                **stack_spec,
                "components":[spec]
            }
            utils.confirm_dialog(message=f"Do you want to create component: {comp_name} in stack: {selected_stack_id} ?",
                                yes_func=lambda: handle_create_component(spec=full_spec,name=comp_name,stack_id=selected_stack_id))
    with col_left:
        st.markdown("###### Component Spec Preview:")
        st.json(spec)