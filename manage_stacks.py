import streamlit as st
from datetime import datetime
from stack_new import stack_new
from stack_remove import stack_remove
from stack_view import stack_view    

actions = [
    ("View",lambda: stack_view()),
    ("New",lambda: stack_new()),
    ("Remove",lambda: stack_remove())
]
selected_action = st.sidebar.radio(label="Action",options=[it[0] for it in actions],horizontal=True)

for (name,callback) in actions:
    if selected_action == name:
        callback()
