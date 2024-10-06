import streamlit as st
import requests
import json

base_url = "http://localhost:38080"

@st.cache_data
def get_stacks():
    resp = requests.get(f"{base_url}/v1/stacks")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)

@st.cache_data
def get_stack_ids():
    resp = requests.get(f"{base_url}/v1/stacks/ids")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)

@st.cache_data
def get_stack(stack_id):
    resp = requests.get(f"{base_url}/v1/stacks/{stack_id}")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)
    
@st.cache_data
def get_clusterconfigs():
    resp = requests.get(f"{base_url}/v1/clusterconfigs")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)

def clear_cache_for_stacks():
    get_stacks.clear()
    get_stack_ids.clear()
    get_stack.clear()

def create_stack(spec):
    resp = requests.post(f"{base_url}/v1/stacks",json=spec)
    if resp.status_code == 200:
        print(f"create stack: {spec['name']}, cluster_name: {spec['cluster_name']}, namespace: {spec['namespace']} successful")
        clear_cache_for_stacks()
    else:
        raise RuntimeError(resp.status_code,resp.text)

# delete_stack('kingtest-gpu-controlplane')
def delete_stack(stack_id):
    resp = requests.delete(f"{base_url}/v1/stacks/{stack_id}")
    if resp.status_code in range(200,300):
        print(f"delete stack[{stack_id}] successful!")
        clear_cache_for_stacks()
    else:
        raise RuntimeError(resp.status_code,resp.text)

def create_component(stack_id:str,spec:dict,name_list:list[dict]):
    resp = requests.put(f"{base_url}/v1/stacks/{stack_id}",json={
        "stack_spec": spec,
        "component_name_list": name_list,
        "message": f"add component: {','.join(name_list)}"
    })
    if resp.status_code == 200:
        print(f"create components stack: {stack_id}, components: {','.join(name_list)} successful")
        clear_cache_for_stacks()
    else:
        raise RuntimeError(resp.status_code,resp.text)
