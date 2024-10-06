import requests
import streamlit as st
import api
import pandas as pd
from annotated_text import annotated_text

stacks_data = api.get_stacks()

all_stack_specs = [{
        "id":it["spec"]['id'],
        "name": it["spec"]['name'],
        "cluster_name":it["spec"]['cluster_name'],
        "namespace": it["spec"]['namespace'],
        **it['stack_status']
    } for it in stacks_data]
all_stack_clusters = set([it['cluster_name'] for it in all_stack_specs])


clusters =["all"] + list(all_stack_clusters)

with st.sidebar:
    selected_cluster = st.selectbox(label="Cluster",options=clusters)
    namespaces = ["all"] + list(set([it['namespace'] for it in all_stack_specs if selected_cluster == 'all' or it['cluster_name'] == selected_cluster]))
    selected_namespace = st.selectbox(label="Namespace",options=namespaces)
    stacks = ["all"] + [it['id'] for it in all_stack_specs if (selected_cluster == 'all' or it['cluster_name'] == selected_cluster) and (selected_namespace == 'all' or it['namespace'] == selected_namespace)]
    selected_stack = st.selectbox(label="Stack",options=stacks)
    states = ["all"] + list(set([it['state'] for it in all_stack_specs]))
    selected_state = st.selectbox(label="State",options=states)
    search_id = st.text_input(label="ID").strip()
    if st.button(label="Force Reload",use_container_width=True,type="primary"):
        api.get_stacks.clear()

filtered_stacks = all_stack_specs
if selected_cluster != 'all':
    filtered_stacks = [it for it in filtered_stacks if it['cluster_name'] == selected_cluster]
if selected_namespace != 'all':
    filtered_stacks = [it for it in filtered_stacks if it['namespace'] == selected_namespace]
if selected_stack != 'all':
    filtered_stacks = [it for it in filtered_stacks if it['id'] == selected_stack]
if search_id != '':
    filtered_stacks = [it for it in filtered_stacks if search_id in it['id']]

# st.write(f"Cluster: {selected_cluster}, Stack: {selected_stack}, size: {len(filtered_stacks)}")
filtered_stacks = sorted(filtered_stacks,key=lambda it:it.get('id'))
filtered_stacks = sorted(filtered_stacks,key=lambda it:it.get('state')=='StackConsistency')

def single_stack(stack: dict):
    st.subheader(f":red[{stack['id']}]" if stack['state'] != 'StackConsistency' else f"{stack['id']}")
    st.markdown(f"**name**: `{stack['name']}`, **cluster_name**: `{stack['cluster_name']}`, **namespace**: `{stack['namespace']}`, **state**: `{stack['state']}`")

    all_comps: list = stack.get('components',[])
    all_comps = sorted(all_comps,key=lambda it:it.get('name'))
    all_comps = sorted(all_comps,key=lambda it:it.get('healthy'))
    anno_list = [(it['name'],'','rgb(9, 171, 59)' if it.get('healthy') else 'orange') for it in all_comps]
    anno_list = [it for idx,one in enumerate(anno_list) for it in ([' ',one] if idx!= 0 else [one])]
    annotated_text(anno_list)
    
while filtered_stacks:
    cols = st.columns(3)
    for i in range(3):
        if not filtered_stacks:
            break
        stack = filtered_stacks.pop(0)
        with cols[i].container(border=True):
            single_stack(stack)
# for stack in filtered_stacks:
#     with st.container(border=True):
#         st.subheader(f":red[{stack['id']}]" if stack['state'] != 'StackConsistency' else f"{stack['id']}")
#         st.markdown(f"**name**: `{stack['name']}`, **cluster_name**: `{stack['cluster_name']}`, **namespace**: `{stack['namespace']}`, **state**: `{stack['state']}`")

#         all_comps: list = stack.get('components',[])
#         all_comps = sorted(all_comps,key=lambda it:it.get('name'))
#         anno_list = [(it['name'],'','lightgreen' if it.get('healthy') else 'orange') for it in all_comps]
#         anno_list = [it for idx,one in enumerate(anno_list) for it in ([' ',one] if idx!= 0 else [one])]
#         annotated_text(anno_list)