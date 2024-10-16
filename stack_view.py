import streamlit as st
from streamlit_ace import st_ace
import api
import json
import utils

def stack_view():
   st.subheader("Stack List")
   result_stacks = api.get_stacks()
   result_stacks.sort(key=lambda st: st.get('id'))
   for stack in result_stacks:
      with st.expander(label=stack.get('id')):
         st.json(stack,expanded=2)