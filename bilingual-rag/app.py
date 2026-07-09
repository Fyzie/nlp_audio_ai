import streamlit as st
import os
from llama_index.core import StorageContext, VectorStoreIndex

# load gemini key from .env directly or from config.py(gemini key checking have to be after import config)
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Bilingual Assistant", layout="wide", page_icon="")

@st.cache_resource
def initialize_rag_system():
    from config import client, vector_store, Settings
    
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)
    
    return index.as_query_engine(similarity_top_k=2)

if "GEMINI_API_KEY" not in os.environ:
    st.error("Error: GEMINI_API_KEY environment variable is not set on this machine.")
    st.stop()

try:
    engine = initialize_rag_system()
except Exception as e:
    st.error(f"Failed to wake vector pipeline engine: {e}")
    st.stop()

# language handling
if "app_language" not in st.session_state:
    st.session_state.app_language = "EN"

def switch_language():
    st.session_state.app_language = "BM" if st.session_state.app_language == "EN" else "EN"

# blingual dict for UI
ui_dictionary = {
    "EN": {
        "title": "Industrial Vision System Assistant",
        "subtitle": "Query technical documentation smoothly in English or Bahasa Melayu.",
        "input_hdr": "Enter technical question or command query below:",
        "placeholder": "e.g., How do I reset the camera feed?",
        "btn_run": "Execute Vector Query",
        "lbl_ans": "Generated System Answer:",
        "lbl_src": "Retrieved Document Reference Context Blocks",
        "lbl_meta": "Source Score Match"
    },
    "BM": {
        "title": "Asisten Sistem Visi Industri",
        "subtitle": "Cari maklumat dokumentasi teknikal dalam Bahasa Inggeris atau Bahasa Melayu.",
        "input_hdr": "Masukkan pertanyaan teknikal atau arahan sistem di bawah:",
        "placeholder": "e.g., Apakah kegunaan penapis Canny?",
        "btn_run": "Proses Pertanyaan Vektor",
        "lbl_ans": "Jawapan Sistem Dijana:",
        "lbl_src": "Blok Rujukan Dokumentasi Sumber yang Diambil",
        "lbl_meta": "Skor Padanan Sumber"
    }
}

current_lang = st.session_state.app_language
text = ui_dictionary[current_lang]

st.title(text["title"])
st.caption(text["subtitle"])
st.markdown("---")

# layout split
col_main, col_spacer, col_side = st.columns([7, 0.5, 2.5])

with col_side:
    st.subheader("System Adjustments")
    st.button(f"Tukar Bahasa (Current: {current_lang})", on_click=switch_language, use_container_width=True)
    st.markdown("---")
    st.markdown("**Infrastructure Status:**")
    st.success("Qdrant Storage: Online")
    st.success("Gemini GenAI: Connected")

with col_main:
    user_query = st.text_input(text["input_hdr"], placeholder=text["placeholder"])
    
    if st.button(text["btn_run"], type="primary"):
        if not user_query.strip():
            st.warning("Please enter some text queries first.")
        else:
            with st.spinner("Processing vectors..."):
                # send query
                response = engine.query(user_query)
                
                # show response box
                st.markdown(f"### {text['lbl_ans']}")
                st.info(response.response)
                
                # show reference docs
                st.markdown("---")
                with st.expander(text["lbl_src"]):
                    for idx, node in enumerate(response.source_nodes):
                        st.markdown(f"**Chunk Reference {idx+1} | {text['lbl_meta']}: `{node.score:.4f}`**")
                        st.code(node.node.get_content())
