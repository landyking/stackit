import streamlit as st
import requests
import json
from datetime import datetime
import os
import utils
import base64


cache_ttl = 10

def generate_basic_auth_header(username: str, password: str) -> dict:
   
    # 1. 组合用户名和密码
    credentials = f"{username}:{password}"
    
    # 2. 进行 Base64 编码
    credentials_bytes = credentials.encode('utf-8')  # 转换为字节
    base64_bytes = base64.b64encode(credentials_bytes)  # Base64 编码
    base64_credentials = base64_bytes.decode('utf-8')  # 转回字符串
    return base64_credentials

def get_request_params():
    settings = utils.load_settings()
    address: str = settings.get('address','address-not-set')
    need_auth: bool = settings.get('need_auth','0') == '1'
    user = settings.get('user','')
    password = settings.get('password','')
    headers = {"Content-Type": "application/json"}
    if need_auth:
        base64_credentials = generate_basic_auth_header(username=user,password=password)
        headers["Authorization"]=f"Basic {base64_credentials}"
    return (address,headers)

@st.cache_data(ttl=cache_ttl)
def get_stacks() -> list[dict]:
    base_url,headers = get_request_params()
    resp = requests.get(f"{base_url}/v1/stacks",headers=headers)
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)

@st.cache_data(ttl=cache_ttl)
def get_stack_ids() -> list[str]:
    base_url,headers = get_request_params()
    resp = requests.get(f"{base_url}/v1/stacks/ids",headers=headers)
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return sorted(resp.json())
    else:
        raise RuntimeError(resp.status_code,resp.text)

@st.cache_data(ttl=cache_ttl)
def get_stack(stack_id) -> dict:
    base_url,headers = get_request_params()
    print(f"loading stack: {stack_id}")
    resp = requests.get(f"{base_url}/v1/stacks/{stack_id}",headers=headers)
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)
    
@st.cache_data(ttl=cache_ttl)
def get_clusterconfigs() -> list[dict]:
    base_url,headers = get_request_params()
    resp = requests.get(f"{base_url}/v1/clusterconfigs",headers=headers)
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)
@st.cache_data(ttl=cache_ttl)
def get_sshtunnels() -> list[dict]:
    base_url,headers = get_request_params()
    resp = requests.get(f"{base_url}/v1/sshtunnels",headers=headers)
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)
@st.cache_data(ttl=cache_ttl)
def get_stack_versions(stack_id:str) -> dict:
    base_url,headers = get_request_params()
    resp = requests.get(f"{base_url}/v1/stacks/{stack_id}/versions",headers=headers)
    if resp.status_code == 200:
        # st.toast("fetch stacks successful!")
        return resp.json()
    else:
        raise RuntimeError(resp.status_code,resp.text)
    
@st.cache_data(ttl=cache_ttl)
def get_stack_events(stack_id:str) -> dict:
    base_url,headers = get_request_params()
    resp = requests.get(f"{base_url}/v1/stacks/{stack_id}/events",headers=headers)
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
    base_url,headers = get_request_params()
    resp = requests.post(f"{base_url}/v1/stacks",json=spec,headers=headers)
    if resp.status_code == 200:
        print(f"create stack: {spec['name']}, cluster_name: {spec['cluster_name']}, namespace: {spec['namespace']} successful")
        clear_cache_for_stacks()
    else:
        raise RuntimeError(resp.status_code,resp.text)

def delete_stack(stack_id):
    base_url,headers = get_request_params()
    resp = requests.delete(f"{base_url}/v1/stacks/{stack_id}",headers=headers)
    if resp.status_code in range(200,300):
        print(f"delete stack[{stack_id}] successful!")
        clear_cache_for_stacks()
    else:
        clear_cache_for_stacks()
        raise RuntimeError(resp.status_code,resp.text)
    
def revert_stack(stack_id: str,version: str):
    base_url,headers = get_request_params()
    url = f"{base_url}/v1/stacks/{stack_id}/versions/{version}"
    print(f"url: {url}")
    resp = requests.put(url,headers=headers)
    if resp.status_code in range(200,300):
        print(f"revert stack[{stack_id}] with version[{version}] successful!")
        clear_cache_for_stacks()
    else:
        clear_cache_for_stacks()
        raise RuntimeError(resp.status_code,resp.text)
    
def delete_component(stack_id,component_name):
    base_url,headers = get_request_params()
    resp = requests.delete(f"{base_url}/v1/stacks/{stack_id}/components/{component_name}",headers=headers)
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
    base_url,headers = get_request_params()
    resp = requests.put(f"{base_url}/v1/stacks/{stack_id}",headers=headers,json={
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
    base_url,headers = get_request_params()
    resp = requests.put(f"{base_url}/v1/stacks/{stack_id}/components/{component_name}/configs",headers=headers,json={
        "configs": configurations,
        "message": f"update configurations {datetime.now().strftime("%Y%m%d%H%M%S")}"
    })
    if resp.status_code in range(200,300):
        print(f"update configuration for component: {component_name} in stack: {stack_id} successful")
        clear_cache_for_stacks(only_component_change=True)
    else:
        raise RuntimeError(resp.status_code,resp.text)
