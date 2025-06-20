# main.py
import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv

# Import styling function
from styling import apply_custom_css
# Import the new feature module
from file_analyzer_features import render_file_analyzer_section
# Import AI embedding logic (for semantic search, though currently placeholder)
from ai_embedding_logic import get_embedding # This import is to ensure the AI logic module is loaded and configured

# --- Page Configuration ---
st.set_page_config(
    page_title="Semantic Search for Databases",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Apply Custom CSS ---
apply_custom_css()

# --- Load Environment Variables ---
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)

# --- API Key Check ---
# Ensure get_embedding_model() and get_generative_model() from ai_embedding_logic are called
# and the API key is validated there. This check here is a redundancy for quick user feedback.
api_key_set = os.getenv("GEMINI_API_KEY") is not None and os.getenv("GEMINI_API_KEY") != "YOUR_ACTUAL_GEMINI_API_KEY_HERE"

if not api_key_set:
    st.warning("🚨 **Google Gemini API Key** not found or is the placeholder! "
               "AI features (like semantic search, when implemented) will not work.")
    st.info("💡 Please set your `GEMINI_API_KEY` in a `.env` file in your project root "
            "(`GEMINI_API_KEY=\"YOUR_API_KEY\"`) or as an environment variable.")
    # st.stop() # Removed st.stop() to allow app to load, just show warning


# --- Session State Initialization ---
if 'user_query' not in st.session_state:
    st.session_state['user_query'] = ""
if 'search_results' not in st.session_state:
    st.session_state['search_results'] = []
if 'metadata_loaded' not in st.session_state:
    st.session_state['metadata_loaded'] = False


# --- Hero Section ---
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title"><i class="fas fa-search"></i> Semantic Search & Data Analyzer</h1>
        <p class="hero-subtitle">Query your database metadata naturally and analyze file data quality.</p>
        <p class="hero-tagline"><strong>Find and understand your data, effortlessly.</strong></p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---") # Visual separator


# --- Main Application Logic (Tabs for different features) ---

# Create tabs for "Data Discovery" and "Data File Analyzer"
tab_data_discovery, tab_file_analyzer = st.tabs(["🔍 Data Discovery", "📊 Data File Analyzer"])

with tab_data_discovery:
    st.markdown("<h2>Data Discovery</h2>", unsafe_allow_html=True)
    st.write("Enter your natural language query below to find relevant tables and columns in your database metadata.")

    user_query_input = st.text_input(
        "Ask a question about your data:",
        placeholder="e.g., Where do we store customer emails and signup time?",
        key="user_query_input_area"
    )
    st.session_state['user_query'] = user_query_input

    if st.button("✨ Semantic Search", type="primary", use_container_width=True, key="perform_search_button"):
        if not api_key_set:
            st.error("Cannot perform search: Google Gemini API Key is not configured.")
        elif not user_query_input.strip():
            st.warning("Please enter a query to perform semantic search.")
            st.session_state['search_results'] = []
        else:
            # Placeholder for actual semantic search logic.
            # This will eventually use get_embedding from ai_embedding_logic.py
            # For now, it still uses mock data.
            st.info("Semantic search functionality will be implemented here, integrating AI embeddings and a vector store.")
            st.session_state['search_results'] = [
                {"table": "customer_profile", "columns": ["email", "created_at"], "description": "Stores registered users and their signup metadata"},
                {"table": "user_accounts", "columns": ["user_email", "registration_timestamp"], "description": "Details of user login and account creation"}
            ] # Mock results for now
            
            st.success("Search initiated (using mock data for now). See results below!")

    # --- Display Search Results (Placeholder) ---
    if st.session_state['search_results']:
        st.markdown("---")
        st.markdown("<h2>Search Results</h2>", unsafe_allow_html=True)
        for result in st.session_state['search_results']:
            st.markdown(f"""
            <div style="background-color: var(--bg-primary); padding: 15px; border-radius: var(--border-radius-md); margin-bottom: 10px; border: 1px solid var(--border-color); box-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                <h3><i class="fas fa-table"></i> Table: <span style="color: var(--accent-green);">{result['table']}</span></h3>
                <p><i class="fas fa-columns"></i> <strong>Columns:</strong> {', '.join([f'<code>{col}</code>' for col in result['columns']])}</p>
                <p><i class="fas fa-info-circle"></i> <strong>Description:</strong> {result['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

with tab_file_analyzer:
    render_file_analyzer_section() # Call the new function to render the file analyzer UI

st.caption("Semantic Search & Data Analyzer | Powered by Streamlit & Google Gemini AI")
