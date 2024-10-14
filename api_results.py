import streamlit as st
import api

apis = [
    ("/v1/stacks",api.get_stacks,False),
    ("/v1/clusterconfigs",api.get_clusterconfigs,False),
    ("/v1/sshtunnels",api.get_sshtunnels,False),
    ("/v1/stacks/{id}/versions",api.get_stack_versions,True),
    ("/v1/stacks/{id}/events",api.get_stack_events,True)
]

selected_api = st.sidebar.selectbox(label="API",options=apis,format_func=lambda it: it[0])

stack_ids = api.get_stack_ids()
selected_stack_id = st.sidebar.selectbox(label="Stack",options=stack_ids)

data = selected_api[1](**{"stack_id":selected_stack_id}) if selected_api[2] else selected_api[1]()

st.title(f"Result of API: {selected_api[0]}")
st.button("Refresh",on_click=lambda:selected_api[1].clear())    
st.json(data,expanded=2)