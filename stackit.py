import streamlit as st

st.set_page_config(layout="wide")
pg = st.navigation({
    "Home":[
        st.Page("dashboard.py",title="Dashboard",default=True),
    ],
    "Manage":[
        st.Page("new_cluster.py",title="New Cluster"),
        st.Page("new_stack.py",title="New Stack"),
        st.Page("rm_stack.py",title="Remove Stack"),
        st.Page("new_component.py",title="New Component"),
        st.Page("new_configuration.py",title="New Configuration"),
    ],
    "Debug":[
        st.Page("api_results.py",title="API Test")
    ]
})
pg.run()