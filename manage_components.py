import streamlit as st
from streamlit_ace import st_ace
import api
import json
import utils
from datetime import datetime
from component_view import component_view
from component_new import component_new
from component_remove import component_remove
from component_update import component_update    

stack_ids = api.get_stack_ids()
if not stack_ids:
    st.error("no available stacks.")
    st.stop()
if st.session_state['search_stack_id'] not in stack_ids:
    utils.correct_state(name='search_stack_id',value=stack_ids[0],sync_query_param=True)
selected_stack = st.sidebar.selectbox(label="Stack",options=stack_ids,key="search_stack_id")

actions = [
    ("View",lambda: component_view(stack_id=selected_stack)),
    ("New",lambda: component_new(stack_id=selected_stack)),
    ("Update",lambda: component_update(stack_id=selected_stack)),
    ("Remove",lambda: component_remove(stack_id=selected_stack))
]
selected_action = st.sidebar.radio(label="Action",options=[it[0] for it in actions],horizontal=True)
st.subheader(f"Components in {selected_stack}")
for (name,callback) in actions:
    if selected_action == name:
        callback()
