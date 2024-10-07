import streamlit as st
import requests
import json

base_url = "http://localhost:38080"

@st.cache_data
def get_stacks() -> list[dict]:
    resp = requests.get(f"{base_url}/v1/stacks")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)

@st.cache_data
def get_stack_ids() -> list[str]:
    resp = requests.get(f"{base_url}/v1/stacks/ids")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)

@st.cache_data(ttl=30)
def get_stack(stack_id) -> dict:
    resp = requests.get(f"{base_url}/v1/stacks/{stack_id}")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)
    
@st.cache_data
def get_clusterconfigs() -> list[dict]:
    resp = requests.get(f"{base_url}/v1/clusterconfigs")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)

def clear_cache_for_stacks(only_component_change = False):
    get_stacks.clear()
    if not only_component_change:
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
        clear_cache_for_stacks()
        raise RuntimeError(resp.status_code,resp.text)
    
def delete_component(stack_id,component_name):
    resp = requests.delete(f"{base_url}/v1/stacks/{stack_id}/components/{component_name}")
    if resp.status_code in range(200,300):
        print(f"delete component[{component_name}] in stack[{stack_id}] successful!")
        clear_cache_for_stacks(only_component_change=True)
    else:
        clear_cache_for_stacks(only_component_change=True)
        raise RuntimeError(resp.status_code,resp.text)

def create_component(stack_id:str,spec:dict,name_list:list[dict]):
    apply_components(stack_id=stack_id,spec=spec,name_list=name_list,message=f"add components: {','.join(name_list)}")

def update_component(stack_id:str,spec:dict,name_list:list[dict]):
    apply_components(stack_id=stack_id,spec=spec,name_list=name_list,message=f"update components: {','.join(name_list)}")

def apply_components(stack_id:str,spec:dict,name_list:list[dict],message:str):
    resp = requests.put(f"{base_url}/v1/stacks/{stack_id}",json={
        "stack_spec": spec,
        "component_name_list": name_list,
        "message": message
    })
    if resp.status_code == 200:
        print(f"apply stack: {stack_id}, components: {','.join(name_list)} successful")
        clear_cache_for_stacks(only_component_change=True)
    else:
        raise RuntimeError(resp.status_code,resp.text)
