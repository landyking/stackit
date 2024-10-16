import streamlit as st
import api
import json
import utils
from datetime import datetime

def component_remove(stack_id: str):
    def handle_remove_component(stack_id,component_name):
        api.delete_component(stack_id=stack_id,component_name=component_name)
        st.session_state['component_remove_success'] = True
        st.rerun()

    if st.session_state.pop("component_remove_success",False):
        st.success("Remove component successful!")

    

    selected_stack = stack_id

    single_stack = api.get_stack(stack_id=selected_stack)
    all_components = single_stack.get('spec',{}).get('components',[])

    if not all_components:
        st.error(f"No component in stack: {selected_stack}")
        st.stop()

    options_comp = [it['name'] for it in all_components]
    if st.session_state['search_component_name'] not in options_comp:
        utils.correct_state(name='search_component_name',value=options_comp[0],sync_query_param=True)

    def format_comp_with_img(name: str):
        it: dict = next(it for it in all_components if it['name'] == name)
        return f"{it['name']} ({it['image']}:{it.get('image_version','latest')})"

    selected_component_name: str = st.selectbox(label="Component",options=options_comp,format_func=format_comp_with_img,key="search_component_name")

    selected_component = next(it for it in all_components if it['name'] == selected_component_name)

    input_component = st.text_input("Retype Component Name")

    same = selected_component['name'] == input_component
    download_data = json.dumps(selected_component,indent=4)

    left,right = st.columns(2)

    if left.button(label="Remove Component",disabled=not same,type="primary",use_container_width=True):
        utils.confirm_dialog(message=f"Do you want to remove component: {input_component} in stack: {selected_stack}",
                            yes_func=lambda: handle_remove_component(stack_id=selected_stack,component_name=input_component))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    right.download_button(label="Backup Current Spec",
                        data=download_data,
                        file_name=f"{selected_stack}@{input_component}.{timestamp}.json",mime="text/json",disabled=not same,type="secondary",
                        use_container_width=True)