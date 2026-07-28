import streamlit as st
import io
import xml.sax.saxutils as saxutils
from dotenv import load_dotenv

#ReportLab Imports for PDF Export
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

load_dotenv()

#Page Config
st.set_page_config(
    page_title="SME Advisor",
    layout="centered"
)


#Safe PDF Generator Function
def generate_pdf(text: str) -> bytes:
    """Safely converts Markdown/Text into a formatted PDF without parsing crashes."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = getSampleStyleSheet()
    
    body_style = ParagraphStyle(
        'PDFBody',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1E293B')
    )
    heading_style = ParagraphStyle(
        'PDFHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=10,
        spaceAfter=4
    )
    
    story = []
    
    for line in text.split('\n'):
        line_str = line.strip()
        if not line_str:
            continue
        
        # Escape XML characters to prevent ReportLab parsing crashes
        escaped_line = saxutils.escape(line_str)
        # Strip bold/code markup for clean plain-text PDF rendering
        clean_line = escaped_line.replace('**', '').replace('*', '').replace('`', '')
        
        if line_str.startswith('#'):
            story.append(Paragraph(clean_line.lstrip('#').strip(), heading_style))
        else:
            story.append(Paragraph(clean_line, body_style))
            
        story.append(Spacer(1, 4))
        
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


#Cached Graph Loader
@st.cache_resource
def load_agent_graph():
    from graph import app_graph
    return app_graph

try:
    app_graph = load_agent_graph()
except Exception as e:
    st.error(f"Failed to initialize Agent Graph: {e}")
    st.stop()


#Sidebar Navigation
with st.sidebar:
    st.title("🇱🇰 SME Advisor")
    st.caption("Agentic AI grounded in official IRD & CBSL regulatory frameworks.")
    
    st.divider()
    st.subheader("Preset Queries")
    
    preset_1 = "I operate an IT service company near Colombo with 8 employees. How do I apply for a technology loan and handle IRD tax filings?"
    preset_2 = "What are the tax registration steps and IRD TIN requirements for a new agricultural business in Kandy?"
    
    if st.button("Tech SME Loan & Tax"):
        st.session_state["query_input"] = preset_1
        st.rerun()
        
    if st.button("Agro Business TIN Guide"):
        st.session_state["query_input"] = preset_2
        st.rerun()


#Main UI
st.title("Sri Lankan SME Business & Tax Advisor")
st.caption("Provide your business scenario below to run the multi-agent analysis pipeline.")

if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""

query = st.text_area(
    "Business Query or Scenario:",
    value=st.session_state["query_input"],
    placeholder="Describe your situation (e.g., location, employee count, tax question, or loan requirement)...",
    height=130
)

col_run, col_clear = st.columns([5, 1])

with col_run:
    run_button = st.button("Run Advisory Pipeline", type="primary", use_container_width=True)

with col_clear:
    if st.button("Clear", use_container_width=True):
        st.session_state["query_input"] = ""
        st.rerun()


# --- Execution Logic ---
if run_button:
    if not query.strip():
        st.warning("Please enter a query before running.")
    else:
        initial_state = {
            "user_query": query,
            "intent": "",
            "retrieved_docs": [],
            "financial_analysis": "",
            "final_report": "",
            "messages": []
        }
        
        st.divider()
        
        with st.status("Executing AI Agents...", expanded=True) as status_box:
            final_state = initial_state
            try:
                for output in app_graph.stream(initial_state):
                    for node, state_update in output.items():
                        st.write(f"✓ **Agent Executed:** `{node}`")
                        
                        if "messages" in state_update and state_update["messages"]:
                            st.info(state_update["messages"][-1])
                            
                        final_state.update(state_update)
                        
                status_box.update(label="Advisory Generation Complete!", state="complete", expanded=False)
            except Exception as pipeline_err:
                status_box.update(label="Pipeline Failed", state="error", expanded=True)
                st.error(f"An error occurred during agent execution: {pipeline_err}")
                st.stop()
        
        # Output Section
        report = final_state.get("final_report", "")
        if report:
            st.subheader("Executive Advisory Report")
            st.markdown(report)
            
            st.divider()
            
            # PDF Download Button
            try:
                pdf_data = generate_pdf(report)
                st.download_button(
                    label="Download Report as PDF",
                    data=pdf_data,
                    file_name="Sri_Lanka_SME_Advisory_Report.pdf",
                    mime="application/pdf"
                )
            except Exception as pdf_err:
                st.warning(f"Report generated, but PDF creation encountered an error: {pdf_err}")