import streamlit as st
import utils

st.set_page_config(layout="wide")

utils.initial_db()
settings = utils.load_settings()
debug_menu = {}
if st.query_params.get('__debug','') == 'stackit':
    debug_menu={
        "Debug":[
            st.Page("api_results.py",title="API Test")
        ]
    }
if settings.get('address'):
    pg = st.navigation({
        "Home":[
            st.Page("dashboard.py",title="Dashboard",default=True),
            st.Page("stacks.py",title="Stacks"),
        ],
        "Manage":[
            # st.Page("cluster_new.py",title="Cluster - New"),
            st.Page("manage_stacks.py",title="Stacks"),
            st.Page("manage_components.py",title="Components"),
            st.Page("manage_configurations.py",title="Configurations"),
            
        ],
        "Setting":[
            st.Page("endpoint.py",title="Endpoint"),
        ],
        **debug_menu
    })

    utils.local_css("style.css")

    # print(f"")

    utils.keep_state("search_stack_id",True)
    utils.keep_state("search_component_name",True)

    pg.run()
else:
    pg = st.navigation({
        "Setting":[
            st.Page("endpoint.py",title="Endpoint",default=True),
        ]
    })
    pg.run()
