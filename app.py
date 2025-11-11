"""
Streamlit web interface for the RAG Q&A system.
Mobile-responsive design optimized for Android phones.

Usage:
    streamlit run app.py
"""

import streamlit as st
from pathlib import Path
import time

from rag_system import RAGSystem
from config import PDF_PATH, DEMO_TOP_K

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Board Game Q&A Assistant",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="collapsed",  # Better for mobile
    menu_items={
        'Get Help': 'https://github.com/yourusername/rag-board-game-qa',
        'Report a bug': 'https://github.com/yourusername/rag-board-game-qa/issues',
        'About': "# RAG Q&A System\nPowered by GPT-3.5 and ChromaDB"
    }
)

# Default placeholder question
DEFAULT_QUESTION = "How do I trade with other players?"

# Custom CSS for mobile responsiveness
st.markdown("""
<style>            
    /* Mobile-first responsive design */
    .main {
        padding: 1rem;
    }
    
    /* Better text readability on mobile */
    .stMarkdown {
        font-size: 16px;
        line-height: 1.6;
    }
    
    /* Larger buttons for touch screens */
    .stButton>button {
        width: 100%;
        height: 3rem;
        font-size: 18px;
        margin: 0.5rem 0;
    }
    
    /* Better input fields on mobile */
    .stTextInput>div>div>input {
        font-size: 16px;
        padding: 0.75rem;
    }
    
    /* Expandable sections for better mobile UX */
    .streamlit-expanderHeader {
        font-size: 18px;
        font-weight: 600;
    }
    
    /* Question cards */
    .question-card {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    
    .question-card:hover {
        background-color: #e0e2e6;
    }
    
    /* Answer styling */
    .answer-box {
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* Source passages */
    .source-box {
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 1rem;
        margin: 0.5rem 0;
        font-size: 14px;
    }
    
    /* Hide Streamlit branding on mobile for cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Loading spinner styling */
    .stSpinner > div {
        text-align: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'rag_system' not in st.session_state:
    st.session_state.rag_system = None
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
if 'process_question' not in st.session_state:
    st.session_state.process_question = False

@st.cache_resource
def load_rag_system():
    """Load RAG system (cached to avoid reloading on every interaction)"""
    try:
        with st.spinner("🔄 Initializing AI system... This may take a minute."):
            rag = RAGSystem(
                pdf_path=str(PDF_PATH),
                chunk_size=300,
                chunk_overlap=30
            )
        return rag, None
    except Exception as e:
        return None, str(e)


def format_answer_with_sources(question, answer, context):
    """Format question, answer and sources in a mobile-friendly way"""
    # Display question and answer in the same container
    st.markdown(f"""
    <div class="answer-box">
        <h4>❓ Question</h4>
        <p>{question}</p>
        <hr style="margin: 1rem 0; border: none; border-top: 1px solid #ccc;">
        <h4>💡 Answer</h4>
        <p>{answer}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display sources in expandable section
    with st.expander("📚 View Source Passages", expanded=False):
        for i, source in enumerate(context, 1):
            # Truncate long sources on mobile
            display_text = source if len(source) < 300 else source[:300] + "..."
            st.markdown(f"""
            <div class="source-box">
                <strong>Source {i}:</strong><br>
                {display_text}
            </div>
            """, unsafe_allow_html=True)

def handle_question_input():
    """Callback function when Enter is pressed in text input"""
    st.session_state.process_question = True

def process_query(query_text):
    """Process a question and display the answer"""
    with st.spinner("🤔 Thinking..."):
        try:
            answer, context = st.session_state.rag_system.answer_question(
                query_text,
                k=DEMO_TOP_K,
                return_context=True
            )
            
            # Display result with question
            format_answer_with_sources(query_text, answer, context)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

def main():
    # Header
    st.markdown("## 🎲 Board Game Q&A Assistant (CATAN)")
    st.markdown("*Ask me anything about CATAN rules!*")
    
    # Initialize system
    if not st.session_state.initialized:
        rag, error = load_rag_system()
        if error:
            st.error(f"❌ Failed to initialize system: {error}")
            st.info("💡 Make sure your PDF and .env file are configured correctly.")
            st.stop()
        st.session_state.rag_system = rag
        st.session_state.initialized = True
        st.success("✅ System ready!")
        time.sleep(0.5)  # Brief pause to show success message
        st.rerun()
    
    # Main input area
    st.markdown("#### 💬 What would you like to know about this game?")
    
    # Initialize current_question if not exists
    if 'current_question' not in st.session_state:
        st.session_state.current_question = ''
    
    # Text input
    user_question = st.text_input(
        "Type your question here...",
        value=st.session_state.current_question,
        placeholder=f"e.g., {DEFAULT_QUESTION}",
        label_visibility="collapsed",
        key="question_input",
        on_change=handle_question_input
    )
    
    # Search button
    search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)
    
    # Process question
    if search_clicked or st.session_state.process_question:
        # Reset the flag
        st.session_state.process_question = False
        
        # Use default question if input is empty
        query_to_process = user_question.strip() if user_question.strip() else DEFAULT_QUESTION
        
        # Process the query
        process_query(query_to_process)
        
        # Clear the input field after processing
        st.session_state.current_question = ''
        st.rerun()
    
    # Quick question suggestions (mobile-friendly cards)
    st.markdown("#### 🔍 Popular Questions:")
    
    example_questions = [
        "How do you win the game?",
        "What happens when you roll a 7?",
        "How do you build a settlement?",
        "What is the longest road?",
        "How many resource cards can you have?"
    ]
    
    # Create a grid of question buttons (2 per row on mobile)
    cols = st.columns(2)
    for idx, question in enumerate(example_questions):
        with cols[idx % 2]:
            if st.button(question, key=f"example_{idx}", use_container_width=True):
                # Update the current question
                st.session_state.current_question = question
                # Trigger processing
                st.session_state.process_question = True
                st.rerun()
    
    st.markdown("---")


if __name__ == "__main__":
    main()