import streamlit as st
import api
import json
import utils
from datetime import datetime
import pandas as pd



def stack_revert():
    def handle_revert_stack(stack_id,version):
        api.revert_stack(stack_id=stack_id,version=version)
        st.session_state['stack_revert_success'] = True
        st.rerun()

    if st.session_state.pop("stack_revert_success",False):
        st.success("Revert stack successful!")
    
    ids = api.get_stack_ids()
    if not ids:
        st.error("no available stacks.")
        st.stop()
    if st.session_state['search_stack_id'] not in ids:
        utils.correct_state(name='search_stack_id',value=ids[0],sync_query_param=True)
    selected_stack = st.selectbox(label="Select Stack",options=ids,key="search_stack_id")
    result_versions = api.get_stack_versions(stack_id=selected_stack)
    current_version =result_versions.get('current','')
    st.info(f"Current version is **{current_version}**")
    versions = result_versions.get('versions',[])
    pd_versions = pd.DataFrame(versions)
    df = st.dataframe(pd_versions,
                      hide_index=True,
                      column_order=("time","version","message"),
                      on_select="rerun",
                      selection_mode="single-row",
                      use_container_width=True)
    
    selected_version = ''
    if df.selection.rows:
        row = pd_versions.iloc[df.selection.rows[0]]
        selected_version = row.get('version')
    left,right = st.columns(2)

    if right.button(label=f"Revert with Version: {selected_version}",disabled=not selected_version,type="primary",use_container_width=True):
        utils.confirm_dialog(message=f"Do you want to revert stack: {selected_stack}",yes_func=lambda: handle_revert_stack(stack_id=selected_stack,version=selected_version))