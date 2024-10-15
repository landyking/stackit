import requests
import streamlit as st
import api
import plotly.express as px
import pandas as pd
from annotated_text import annotated_text
import duckdb
from datetime import datetime,timezone,timedelta

selected_auto_refresh = st.sidebar.checkbox(label="Auto Refresh",value=True)
@st.fragment(run_every="10s" if selected_auto_refresh else None)
def main_fragment():
    result_stacks = api.get_stacks()
    # st.dataframe(pd.json_normalize(result_stacks))

    tmp_stacks = [ {
        **{
            k:v for (k,v) in stack.get('spec',{}).items()
        },
        **{
            k:v for (k,v) in stack.get('stack_status',{}).items() if k not in ['event',"components"]
        },
        "last_modified": max([comp["last_modified"] for comp in stack.get('stack_status',{}).get('components',[])])
    } for stack in result_stacks]

    tz_est8 = timezone(timedelta(hours=8))
    all_stacks = pd.DataFrame([
        {
            **stack,
            "last_modified_str": pd.to_datetime(stack['last_modified']).astimezone(tz_est8).strftime("%y-%m-%d %H:%M:%S"),
        }
        for stack in tmp_stacks
    ])

    all_stacks = all_stacks.sort_values(by="last_modified_str",ascending=False).sort_values(by="state",ascending=False)

    # st.dataframe(all_stacks)

    all_component_spec =pd.DataFrame([ {
        "stack_id": stack['id'],
        **{key: value for (key,value) in comp.items()}
        }
        for stack in result_stacks 
        for comp in stack.get('spec',{}).get('components',[])
    ])
    # st.dataframe(all_component_spec)

    all_component_status =pd.DataFrame([ {
        "stack_id": stack['id'],
        **{key: value for (key,value) in comp.items()}
        }
        for stack in result_stacks 
        for comp in stack.get('stack_status',{}).get('components',[])
    ])
    # st.dataframe(all_component_status)

    result_clusters =  api.get_clusterconfigs()
    result_sshtunnels = api.get_sshtunnels()

    col1,col2,col3,col4 = st.columns([1,1,2,2],vertical_alignment="center")

    with col1:
        st.container(border=True).metric(label="Cluster Count",value=len(result_clusters))
        st.container(border=True).metric(label="SSH Tunnel Count",value=len(result_sshtunnels))
    with col2:
        st.container(border=True).metric(label="Stack Count",value=len(result_stacks))
        st.container(border=True).metric(label="Component Count",value=len(all_component_spec))

    config = {'displayModeBar': False}

    pie_data_stack_status = duckdb.sql("select state as 状态, count(*) as 数量 from all_stacks group by state").df()
    with col3:
        fig = px.pie(
            pie_data_stack_status,
            names='状态',
            values='数量',
            title="Status of Stacks",
            # hole=0.3,  # 设置中间洞的大小，形成环形图。去掉此参数即可显示传统饼图
            # color_discrete_sequence=px.colors.qualitative.Set3  # 设置颜色序列
        )
        st.plotly_chart(fig, config=config, use_container_width=True)

    pie_data_component_status = duckdb.sql("""
        select condition as 状态, count(*) as 数量 from (
            select sp.stack_id,sp.name,sp.enable,st.healthy,
            case
                when sp.enable = 'true' and st.healthy = 'true' then 'normal'
                when sp.enable = 'true' and st.healthy != 'true' then 'abnormal'
                else 'disabled'
            end as condition 
            from all_component_spec sp 
            left join all_component_status st on sp.stack_id = st.stack_id and sp.name = st.name
        ) group by condition""").df()
    with col4:
        fig = px.pie(
            pie_data_component_status,
            names='状态',
            values='数量',
            title="Status of Components",
            # hole=0.3,  # 设置中间洞的大小，形成环形图。去掉此参数即可显示传统饼图
            # color_discrete_sequence=px.colors.qualitative.Set3  # 设置颜色序列
        )
        st.plotly_chart(fig, config=config, use_container_width=True)
    stack_list = all_stacks.to_dict(orient="records")
    while stack_list:
        cols = st.columns(3)
        for i in range(3):
            if not stack_list:
                break
            stack = stack_list.pop(0)
            with cols[i].container(border=True):
                state = stack['state']
                color = "green" if state == 'StackConsistency' else 'red'
                st.markdown(f"##### :{color}[{stack['id']}]")
                st.markdown(f" **State**: :{color}[{stack['state']}]")
                st.markdown(f" **Last Modified**: `{stack['last_modified_str']}`")
                comps_md =" ".join([f"`{it['name']}`" for it in stack['components']])
                st.markdown(f" **Components**: {comps_md}")
                if st.button(label="View",type="secondary",use_container_width=True,key=f"comp_btn_{stack['id']}"):
                    st.session_state['search_stack_id'] = stack['id']
                    st.switch_page("stacks.py")

main_fragment()