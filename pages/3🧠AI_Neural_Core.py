import streamlit as st
import time
from src.ui.styles import apply_terminal_style

apply_terminal_style()
st.title("🧠 NEURAL CORE: AI ANALYST")

# Mock AI Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages =

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

prompt = st.chat_input("Query the Neural Core (e.g., 'Analyze TSLA volatility')...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Processing neural weights..."):
            time.sleep(1) # Giả lập độ trễ suy nghĩ
            response = f"****: Analysis for '{prompt}' initiated.\n\nBased on current market vectors, the volatility index indicates a standard deviation shift of 2.4 sigma. Recommendation: Hedge with put options if beta exposure exceeds 1.5. (This is a simulation)"
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
