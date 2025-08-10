## StackIt — Streamlit admin for internal backend APIs 🚀

StackIt is a Streamlit app for managing stacks, components, and configurations via REST APIs. It showcases building a polished internal tool with Streamlit: state, caching, charts, code editing, dialogs, and more.

### ✨ Key features

- 📊 Dashboard
	- Auto-refresh (every 10s) via `st.fragment(run_every=...)`.
	- Live metrics: stacks, components, clusters, SSH tunnels.
	- Plotly pie charts; DuckDB SQL on pandas for fast aggregations.
	- Interactive table that navigates to details on row select.
	- One-click JSON export for all stacks.

- 📦 Stacks
	- View: expanders with full stack JSON.
	- New: form + ACE JSON editor, validation, spec preview, confirm dialog.
	- Remove: retype-to-confirm, spec backup download, confirm dialog.
	- Revert: pick a historical version from a table and revert with confirm.

- 🧩 Components (per stack)
	- View: expanders for each component.
	- New: guided form (image, version, count, type, enable) + JSON properties editor; preview + confirm.
	- Update: edit core fields and advanced JSON while preserving configurations; preview + confirm.
	- Remove: select, retype name to confirm, backup spec, confirm dialog.

- ⚙️ Configurations (per component)
	- View: expanders for all configurations.
	- New: ACE editor with language auto-detect from filename, base64 toggle, sub-path, local filename; confirm dialog.
	- Update/Remove: edit in-place with language-aware editor; update or remove with confirm.

- 🧪 API test console (debug)
	- Quick viewer for stacks, cluster configs, SSH tunnels, versions, events.
	- Manual cache clear button for selected API.
	- Visible only with `?__debug=stackit` in URL.

- 🔧 Endpoint settings & persistence
	- Configure base URL and optional Basic Auth.
	- Persisted in local SQLite via `st.connection(..., type='sql')` and cached with `@st.cache_data`.
	- First run routes to Settings if no endpoint is set.

### 🧠 Streamlit techniques used

- Multi-page navigation with `st.Page` and `st.navigation`.
- Sidebar controls (selectbox, radio, checkboxes) to drive actions and refresh.
- `st.fragment(run_every=...)` for smooth timed updates.
- URL query params + `st.session_state` sync for deep linking.
- `st.dataframe` with custom columns, selection, and programmatic navigation.
- Plotly charts via `st.plotly_chart`.
- DuckDB SQL on DataFrames for quick aggregations.
- `st.dialog` confirms; layout with `st.expander`, `st.columns`, `st.metric`.
- `@st.cache_data` with targeted invalidation on writes.
- Local CSS injection for small style tweaks.
- ACE editor (`streamlit-ace`) for JSON/config editing with language highlighting.

### 🗂️ Architecture (modules)

- `stackit.py` — entrypoint, navigation, state bootstrap, CSS.
- `dashboard.py` — metrics, charts, interactive table.
- Stacks: `manage_stacks.py`, `stack_view.py`, `stack_new.py`, `stack_remove.py`, `stack_revert.py`.
- Components: `manage_components.py`, `component_view.py`, `component_new.py`, `component_update.py`, `component_remove.py`.
- Configurations: `manage_configurations.py`, `configuration_view.py`, `configuration_new.py`, `configuration_update.py`.
- `api.py` — requests client with caching + invalidation.
- `api_results.py` — debug API console.
- `endpoint.py` — endpoint/auth settings.
- `utils.py` — dialogs, state/query sync, settings, language detection, CSS.

### 🔌 Backend API surface used

- GET `/v1/stacks`, `/v1/stacks/ids`, `/v1/stacks/{id}`
- POST `/v1/stacks`
- DELETE `/v1/stacks/{id}`
- PUT `/v1/stacks/{id}/versions/{version}` (revert)
- PUT `/v1/stacks/{id}` (apply components)
- DELETE `/v1/stacks/{id}/components/{name}`
- PUT `/v1/stacks/{id}/components/{name}/configs`
- GET `/v1/stacks/{id}/versions`, `/v1/stacks/{id}/events`
- GET `/v1/clusterconfigs`, `/v1/sshtunnels`

### 🧰 Caching & state

- Reads use `@st.cache_data(ttl=10)` to keep the UI responsive.
- Writes (create/update/delete/apply/revert) clear only the necessary caches.
- `st.session_state` + URL query params keep selections stable across pages.

### 🔒 Security notes

- Optional Basic Auth; credentials stored locally in SQLite for convenience. Treat this as an internal tool and protect the environment.

---

## ▶️ Run locally

Prerequisites: Python 3.12+

1) Create/activate a virtualenv and install deps

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Start the app

```bash
streamlit run stackit.py
```

3) First run: open Settings → Endpoint, enter API URL and (optional) Basic Auth, then Save.

Tip: open Dashboard and enable Auto Refresh; add `?__debug=stackit` to the URL to reveal the API Test page.

## 🐳 Docker

Build the image:

```bash
docker build -t landykingdom/stackit .
```

Run the container:

```bash
docker run --rm -p 8501:8501 landykingdom/stackit
```

Healthcheck is enabled; the app listens on port 8501.

## 🛠️ Developer notes

- Updating dependencies (optional): tools like creosote can audit; then pin with `pip freeze > requirements.txt`.
- Dockerfile copies `.streamlit/` if present for app-wide config; optional.
- If you change write flows, clear the right caches in `api.py` to keep the UI consistent.

