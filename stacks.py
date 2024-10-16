import requests
import streamlit as st
import api
import pandas as pd
import utils
from annotated_text import annotated_text


def part_stack(result_stack: dict):
    stack_id = result_stack['id']
    stack_status = result_stack.get('stack_status',{})
    state =  stack_status.get('state','')
    version = stack_status.get('version','')
    last_modified =  max([comp["last_modified"] for comp in stack_status.get('components',[])],
                         default=stack_status.get('last_modified'))
    update_spec_message = stack_status.get('update_spec_message','')
    error = stack_status.get('error',False)
    cause = stack_status.get('cause','')
    color = 'green' if state=="StackConsistency" else 'red'
    st.markdown(f"#### :{color}-background[{stack_id}]  :{color}[{state}]")
    text_list = [("version",version,"#eee")," ",("last_modified",last_modified,"#eee")]
    if update_spec_message:
        text_list.append(" ")
        text_list.append(("update_spec_message",update_spec_message,"#eee"))
    if error:
        text_list.append(" ")
        text_list.append(("error",f'{error}',"#eee"))
    if cause:
        text_list.append(" ")
        text_list.append(("cause",cause,"#eee"))

    annotated_text(text_list)

def categorize_components(full_comps: list[dict]):
    total = 0
    healthy = 0
    unhealthy = 0
    disabled = 0
    for comp in full_comps:
        total+=1
        if not comp.get('enable',False):
            disabled+=1
            comp['state'] = 'disabled'
            comp['color'] = 'gray'
        elif comp.get('healthy',False):
            healthy+=1
            comp['state'] = 'healthy'
            comp['color'] = 'green'
        else:
            unhealthy+=1
            comp['state'] = 'unhealthy'
            comp['color'] = 'red'
    return (total,healthy,unhealthy,disabled)

def build_component_title(total: int,healthy: int,unhealthy: int,disabled: int):
    title = f"###### Components: {total}"
    if healthy > 0:
        title+=f" :green-background[healthy: {healthy}]"
    if unhealthy > 0:
        title+=f" :red-background[unhealthy: {unhealthy}]"
    if disabled > 0:
        title+=f" :gray-background[disabled: {disabled}]"
    return title

def part_single_component(comp: dict):
    with st.expander(label=f":{comp['color']}-background[{comp['name']}] - :{comp['color']}[{comp['state']}]"):
        # st.markdown(f"###### :{comp['color']}-background[{comp['name']}] - :{comp['color']}[{comp['state']}]")
        annotated_text(('last modified',comp['last_modified'],"#fff"),
                        " ",("image",comp.get('image',''),"#fff"),
                        " ",("image version",comp.get('image_version',''),"#fff"),
                        " ",("instance count",f"{comp['instance_count']}","#fff"),
                        " ",("enable",f"{comp.get('enable',False)}","#fff"),
                        " ",("healthy",f"{comp.get('healthy',False)}","#fff"),)

def part_components(result_stack: dict):
    spec_comps: list[dict] = result_stack.get('spec',{}).get('components',[])
    stat_comps: list[dict] = result_stack.get('stack_status',{}).get('components',[])

    full_comps: list[dict] = [
        {
            **spc,
            **next(stc for stc in stat_comps if stc.get('name') == spc.get('name'))
        }
        for spc in spec_comps
    ]
    total,healthy,unhealthy,disabled = categorize_components(full_comps=full_comps)

    full_comps.sort(key=lambda it:it.get('last_modified'),reverse=True)
    full_comps.sort(key=lambda it:{"disabled":3,"unhealthy":1,"healthy":2}.get(it['state']))

    st.markdown(build_component_title(total=total,healthy=healthy,unhealthy=unhealthy,disabled=disabled))

    col_size = 3
    while full_comps:
        cols = st.columns(col_size)
        for col in range(col_size):
            if not full_comps:
                break
            comp = full_comps.pop(0)
            with cols[col]:
                part_single_component(comp)
            

def part_version_history(result_stack: dict):
    stack_id = result_stack['id']
    result_versions = api.get_stack_versions(stack_id)
    versions = result_versions.get('versions',[])
    pd_versions = pd.DataFrame(versions)
    pd_versions['time'] = pd.to_datetime(pd_versions['time'])
    st.markdown("###### Version History")
    st.dataframe(pd_versions.head(100),column_order=("time","version","message"),
                hide_index=True,
                use_container_width=True)

def part_event_history(result_stack: dict):
    stack_status = result_stack.get('stack_status',{})
    event_data = stack_status.get('event',[])
    pd_event = pd.DataFrame(event_data)
    pd_event['timestamp'] = pd.to_datetime(pd_event['timestamp'])
    # st.dataframe(pd_event,use_container_width=True)
    # with st.container(border=False):
    st.markdown("###### Event History")
    st.scatter_chart(
        pd_event.head(100),
        x="timestamp",
        y="type",
        color="subject",
        # size="col3",
        use_container_width=True
    )

stack_ids = api.get_stack_ids()
if not stack_ids:
    st.error("no available stacks.")
    st.stop()
with st.sidebar:
    if st.session_state['search_stack_id'] not in stack_ids:
        utils.correct_state(name='search_stack_id',value=stack_ids[0],sync_query_param=True)
    selected_stack_id = st.selectbox(label="Stack",options=stack_ids,key="search_stack_id")

selected_auto_refresh = st.sidebar.checkbox(label="Auto Refresh",value=True)

@st.fragment(run_every="10s" if selected_auto_refresh else None)
def main_fragment():

    result_stack = api.get_stack(stack_id=selected_stack_id)
    # st.json(result_stack,expanded=1)    
    part_stack(result_stack=result_stack)
        
    st.divider()

    part_components(result_stack=result_stack)

    # st.divider()

    part_version_history(result_stack=result_stack)

    # st.divider()

    part_event_history(result_stack=result_stack)

main_fragment()