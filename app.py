import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="SME Advisor", page_icon="🇱🇰", layout="centered")

with st.spinner("Initializing Database & Agents..."):
    from graph import app_graph

st.title("Sri Lankan SME Business & Tax Advisor")
st.caption("Agentic AI-driven regulatory, registration, and financial guidance grounded in official Sri Lankan frameworks.")
st.divider()

user_query = st.text_area(
    "Describe your business query or problem:",
    placeholder="e.g., I have an IT company near Colombo with 8 working employees and I need to apply for a bank loan...",
    height=100
)

run_button = st.button("Run Multi-Agent Advisory Pipeline", type="primary", use_container_width=True)

if run_button:
    if not user_query.strip():
        st.warning("Please enter a query to begin.")
    else:
        initial_state = {
            "user_query": user_query,
            "intent": "",
            "retrieved_docs": [],
            "financial_analysis": "",
            "final_report": "",
            "messages": []
        }
        
        with st.status("🤖 Agents Collaborating...", expanded=True) as status_box:
            final_state = initial_state
            
            for output in app_graph.stream(initial_state):
                for node, state_update in output.items():
                    st.write(f"**Agent Executed:** `{node}`")
                    
                    if "messages" in state_update and state_update["messages"]:
                        st.info(state_update["messages"][-1])
                        
                    final_state.update(state_update)
                    
            status_box.update(label="Advisory Process Complete!", state="complete", expanded=False)
        
        st.divider()
        st.subheader("Generated Business Advisory Report")
        st.markdown(final_state.get("final_report", "No report generated."))