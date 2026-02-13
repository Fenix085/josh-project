import streamlit as st
from common import load_json, json
from main import run_scraper, run_filter, run_llm

conf = load_json("config.json")

st.title("News Pipeline")

st.subheader("Pipeline Execution")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button(label="Run Pipeline", type="primary"):
        with st.spinner("Pipeline is running..."):
            run_scraper()
            run_filter()
            run_llm()
        st.success("Pipeline executed successfully!")
with col2:
    if st.button(label="Run Scraper", type="secondary"):
        with st.spinner("Scraper is running..."):
            run_scraper()
        st.success("Scraper executed successfully!")
with col3:
    if st.button(label="Run Filter", type="secondary"):
        with st.spinner("Filter is running..."): 
            run_filter()
        st.success("Filter executed successfully!")
with col4:
    if st.button(label="Run LLM", type="secondary"):
        with st.spinner("LLM is running..."):
            run_llm()
        st.success("LLM executed successfully!")

st.subheader("Source Configuration")
for source in conf["sources"]:
    source["active"] = st.checkbox(source["name"], value=source["active"])
    st.text(source["url"])

if st.button(label="Save changes", type="primary"):
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(conf, f, indent=4)
    st.success("Configuration saved successfully!")
