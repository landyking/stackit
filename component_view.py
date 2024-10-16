import streamlit as st
from streamlit_ace import st_ace
import api
import json
import utils

def component_view(stack_id: str):
   result_stack = api.get_stack(stack_id=stack_id)
   components = result_stack.get("spec",{}).get('components',[])
   for comp in components:
      with st.expander(label=comp.get('name')):
         st.json(comp,expanded=1)
   if not components:
      st.info("No Data")