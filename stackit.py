import streamlit as st
import utils

st.set_page_config(layout="wide")
pg = st.navigation({
    "Home":[
        st.Page("dashboard.py",title="Dashboard",default=True),
        st.Page("stacks.py",title="Stacks"),
    ],
    "Manage":[
        st.Page("cluster_new.py",title="Cluster - New"),
        st.Page("stack_new.py",title="Stack - New"),
        st.Page("stack_remove.py",title="Stack - Remove"),
        st.Page("component_new.py",title="Component - New"),
        st.Page("component_update.py",title="Component - Update"),
        st.Page("component_remove.py",title="Component - Remove"),
        st.Page("configuration_new.py",title="Configuration - New"),
        st.Page("configuration_update.py",title="Configuration - Update"),
    ],
    "Debug":[
        st.Page("api_results.py",title="API Test")
    ]
})

utils.local_css("style.css")

utils.keep_state("search_stack_id",True)

pg.run()