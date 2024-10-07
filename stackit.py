import streamlit as st

st.set_page_config(layout="wide")
pg = st.navigation({
    "Home":[
        st.Page("dashboard.py",title="Dashboard",default=True),
    ],
    "Manage":[
        st.Page("cluster_new.py",title="Cluster - New"),
        st.Page("stack_new.py",title="Stack - New"),
        st.Page("stack_remove.py",title="Stack - Remove"),
        st.Page("component_new.py",title="Component - New"),
        st.Page("component_update.py",title="Component - Update"),
        st.Page("component_remove.py",title="Component - Remove"),
        st.Page("configuration_new.py",title="Configuration - New"),
    ],
    "Debug":[
        st.Page("api_results.py",title="API Test")
    ]
})
pg.run()