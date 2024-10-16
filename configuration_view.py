import streamlit as st

def configuration_view(stack_id,component: dict):
   configs = component.get('configurations',[])
   for cfg in configs:
      with st.expander(label=f":blue[{cfg.get('use_as_file','')}] - {cfg.get('key')}"):
         st.json(cfg,expanded=1)
   if not configs:
      st.info("No Data")