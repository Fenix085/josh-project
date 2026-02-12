import streamlit as st
from common import load_json, json

conf = load_json("config.json")

st.title("News Pipeline")
for source in conf["sources"]:
    source["active"] = st.checkbox(source["name"], value=source["active"])
    st.text(source["url"])
if st.button(label="Save changes"):
    with open("config.json", 'w', encoding='utf-8') as f:
        json.dump(conf, f, indent=4)