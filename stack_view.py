import streamlit as st
import api

def stack_view():
   st.subheader("Stack List")
   result_stacks = api.get_stacks()
   result_stacks.sort(key=lambda st: st.get('id'))
   for stack in result_stacks:
      with st.expander(label=stack.get('id')):
         st.json(stack,expanded=2)
   if not result_stacks:
      st.info("No Data")