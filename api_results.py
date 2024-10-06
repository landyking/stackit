import streamlit as st
import api

apis = [
    ("/v1/stacks",api.get_stacks),
    ("/v1/clusterconfigs",api.get_clusterconfigs)
]

selected_api = st.sidebar.selectbox(label="API",options=apis,format_func=lambda it: it[0])

data = selected_api[1]()

st.title(f"Result of API: {selected_api[0]}")
st.button("Refresh",on_click=lambda:selected_api[1].clear())    
st.json(data,expanded=2)