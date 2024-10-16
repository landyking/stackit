import streamlit as st
from streamlit_ace import st_ace
import api
import json
import utils
from datetime import datetime
from configuration_view import configuration_view
from configuration_new import configuration_new
from configuration_update import configuration_update    

stack_ids = api.get_stack_ids()

if not stack_ids:
    st.error("no available stacks.")
    st.stop()

if st.session_state['search_stack_id'] not in stack_ids:
    utils.correct_state(name='search_stack_id',value=stack_ids[0],sync_query_param=True)

selected_stack = st.sidebar.selectbox(label="Stack",options=stack_ids,key="search_stack_id")

result_stack =  api.get_stack(stack_id=selected_stack)

components = [it for it in result_stack.get("spec",{}).get('components',[])]

if not components:
    st.error(f"no available components in {selected_stack}.")
    st.stop()

options_comp = [it['name'] for it in components]
if st.session_state['search_component_name'] not in options_comp:
    utils.correct_state(name='search_component_name',value=options_comp[0],sync_query_param=True)

selected_component_name = st.sidebar.selectbox(label="Component",options=options_comp,key="search_component_name")

selected_component = next(it for it in components if it['name'] == selected_component_name)

actions = [
    ("View",lambda: configuration_view(stack_id=selected_stack,component=selected_component)),
    ("New",lambda: configuration_new(stack_id=selected_stack,component=selected_component)),
    ("Update/Remove",lambda: configuration_update(stack_id=selected_stack,component=selected_component)),
]
selected_action = st.sidebar.radio(label="Action",options=[it[0] for it in actions],horizontal=True)

st.subheader(f"Configurations in {selected_component['name']} in {selected_stack}")
for (name,callback) in actions:
    if selected_action == name:
        callback()
