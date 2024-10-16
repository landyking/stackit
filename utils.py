import streamlit as st
from sqlalchemy.sql import text

@st.dialog("Confirm")
def confirm_dialog(message: str,yes_func:callable = st.rerun,no_func: callable = st.rerun):
    st.write(message)
    col1,col2 = st.columns(2)
    if col1.button(label="Yes",type="primary",use_container_width=True):
        yes_func()
    if col2.button(label="No",type="secondary",use_container_width=True):
        no_func()

def get_language_by_filename(filename: str):
    filename = filename.lower()
    if filename.endswith('.yaml') or filename.endswith('.yml'):
        return "yaml"
    if filename.endswith('.json'):
        return "json5"
    if filename.endswith('.ini'):
        return "ini"
    if filename.endswith('.toml'):
        return "toml"
    if filename.endswith('.xml'):
        return "xml"
    return "plain_text"

def keep_state(name: str, sync_query_param: bool = False):
    old_value = st.session_state.get(name, None)
    if old_value != None:
        st.session_state[name] = old_value
    elif sync_query_param:
        st.session_state[name] = st.query_params.get(name,None)
    else:
        st.session_state[name] = None

    if sync_query_param:
        st.query_params[name] = st.session_state[name]

def correct_state(name: str,value, sync_query_param: bool = False):
    st.session_state[name] = value
    if sync_query_param:
        st.query_params[name] = st.session_state[name]

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def initial_db():
    conn = st.connection('stackit_db', type='sql')
    with conn.session as s:
        rst = s.execute(text("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='t_settings'")).first()
        if not rst[0]:
            print(f"start to initial database")
            s.execute(text("CREATE TABLE IF NOT EXISTS t_settings (name TEXT UNIQUE NOT NULL, value TEXT NOT NULL);"))
            s.commit()
        
@st.cache_data
def load_settings() -> dict:
    conn = st.connection('stackit_db', type='sql')
    settings = conn.query('select * from t_settings',ttl=0)
    rst = settings.to_dict("records")
    return {it['name']:it['value'] for it in rst}

def save_settings(settings: dict):
    conn = st.connection('stackit_db', type='sql')
    with conn.session as s:
        for k,v in settings.items():
            s.execute(text("INSERT or REPLACE INTO t_settings (name, value) VALUES (:name, :value)"),{"name":k,"value":v})
        s.commit()
    load_settings.clear()