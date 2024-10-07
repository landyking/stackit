import streamlit as st
import requests
import json
from datetime import datetime
import os

base_url = os.getenv("STACKIT_BASE_URL",default="http://localhost:38080")

print(f"using base_url: {base_url}")

@st.cache_data(ttl=30)
def get_stacks() -> list[dict]:
    resp = requests.get(f"{base_url}/v1/stacks")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)

@st.cache_data(ttl=30)
def get_stack_ids() -> list[str]:
    resp = requests.get(f"{base_url}/v1/stacks/ids")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return sorted(resp.json())
    else:
        raise RuntimeError(resp.status_code,resp.text)

@st.cache_data(ttl=30)
def get_stack(stack_id) -> dict:
    print(f"loading stack: {stack_id}")
    resp = requests.get(f"{base_url}/v1/stacks/{stack_id}")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)
    
@st.cache_data(ttl=30)
def get_clusterconfigs() -> list[dict]:
    resp = requests.get(f"{base_url}/v1/clusterconfigs")
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)

def clear_cache_for_stacks(only_component_change: bool = False,stack_id: str = None):
    get_stacks.clear()
    if not only_component_change:
        get_stack_ids.clear()
    if stack_id:
        get_stack.clear(stack_id)
    else:
        get_stack.clear()

def create_stack(spec):
    resp = requests.post(f"{base_url}/v1/stacks",json=spec)
    if resp.status_code == 200:
        print(f"create stack: {spec['name']}, cluster_name: {spec['cluster_name']}, namespace: {spec['namespace']} successful")
        clear_cache_for_stacks()
    else:
        raise RuntimeError(resp.status_code,resp.text)

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
    
def apply_configurations(stack_id: str,component_name: str,configurations: list[dict]):
    resp = requests.put(f"{base_url}/v1/stacks/{stack_id}/components/{component_name}/configs",json={
        "configs": configurations,
        "message": f"update configurations {datetime.now().strftime("%Y%m%d%H%M%S")}"
    })
    if resp.status_code in range(200,300):
        print(f"update configuration for component: {component_name} in stack: {stack_id} successful")
        clear_cache_for_stacks(only_component_change=True)
    else:
        raise RuntimeError(resp.status_code,resp.text)
