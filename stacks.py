import requests
import streamlit as st
import api
import pandas as pd



st.title("Stackit")

stacks_data = api.get_stacks()

all_stack_specs = [it["spec"] for it in stacks_data]
all_stack_clusters = set([it['cluster_name'] for it in all_stack_specs])


clusters =["all"] + list(all_stack_clusters)

with st.sidebar:
    selected_cluster = st.selectbox(label="Cluster",options=clusters)
    namespaces = ["all"] + list(set([it['namespace'] for it in all_stack_specs if selected_cluster == 'all' or it['cluster_name'] == selected_cluster]))
    selected_namespace = st.selectbox(label="Namespace",options=namespaces)
    stacks = ["all"] + [it['id'] for it in all_stack_specs if (selected_cluster == 'all' or it['cluster_name'] == selected_cluster) and (selected_namespace == 'all' or it['namespace'] == selected_namespace)]
    selected_stack = st.selectbox(label="Stack",options=stacks)
    search_name = st.text_input(label="Name").strip()

filtered_stacks = all_stack_specs
if selected_cluster != 'all':
    filtered_stacks = [it for it in filtered_stacks if it['cluster_name'] == selected_cluster]
if selected_namespace != 'all':
    filtered_stacks = [it for it in filtered_stacks if it['namespace'] == selected_namespace]
if selected_stack != 'all':
    filtered_stacks = [it for it in filtered_stacks if it['id'] == selected_stack]
if search_name != '':
    filtered_stacks = [it for it in filtered_stacks if search_name in it['name']]

st.write(f"Cluster: {selected_cluster}, Stack: {selected_stack}, size: {len(filtered_stacks)}")

for idx,stack in enumerate(filtered_stacks):
    with st.container(border=True):
        st.subheader(f"stack: {stack['id']}")
        st.write(f"namespace: {stack['namespace']}")
        st.write(f"name: {stack['name']}")
        dt = pd.DataFrame(data=stack['components'])
        st.dataframe(data=dt,use_container_width=True)