import streamlit as st
import pathlib

base = pathlib.Path(__file__).parent
html_dir = base / "notebooks_html"

st.title("Notebooks")

files = sorted([p for p in html_dir.glob("*.html")])
choice = st.selectbox("Selecciona notebook", [p.name for p in files])
html = (html_dir / choice).read_text(encoding="utf-8")
st.components.v1.html(html, height=800, scrolling=True)

