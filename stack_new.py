import streamlit as st
from streamlit_ace import st_ace
import api
import json
import utils



def stack_new():

    def handle_create_stack(spec):
        api.create_stack(spec)
        st.session_state['stack_create_success'] = True
        st.rerun()

    if st.session_state.pop("stack_create_success",False):
        st.success("Create stack successful!")

    clusterconfigs = api.get_clusterconfigs()
    options_cluster = [it['name'] for it in clusterconfigs]
    default_properties = '''{
        "health_check_interval": 10,
        "pulse_event_interval": 30,
        "easemesh": {},
        "components": []
    }'''
    spec = {}

    ids = api.get_stack_ids()
    with st.expander(label="Existing Stacks",expanded=True):
        st.markdown(", ".join([f"`{it}`" for it in ids]))

    col_left,col_right = st.columns(2,vertical_alignment="top")

    with col_right:
        selected_cluster = st.selectbox(label="Cluster",options=options_cluster)
        input_name = st.text_input(label="Name")
        input_namespace = st.text_input(label="Namespace")
        
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
            "cluster_name": selected_cluster,
            "name": input_name,
            "namespace": input_namespace
        })
        
        if st.button("Submit",type="primary", use_container_width=True):
            utils.confirm_dialog(message="Do you really want submit these data?",yes_func=lambda :handle_create_stack(spec))
    with col_left:
        st.markdown("###### Stack Spec Preview:")
        st.json(spec)