import streamlit as st
import utils

st.set_page_config(layout="wide")

utils.initial_db()
settings = utils.load_settings()
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
        # "Debug":[
        #     st.Page("api_results.py",title="API Test")
        # ]
    })

    utils.local_css("style.css")

    # print(f"")

    utils.keep_state("search_stack_id",True)
    utils.keep_state("search_component_name",True)

    pg.run()
else:
    pg = st.navigation({
        "Setting":[
            st.Page("setting.py",title="Setting",default=True),
        ]
    })
    pg.run()
