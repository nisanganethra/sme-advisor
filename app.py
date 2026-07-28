import streamlit as st
import os
import io
from dotenv import load_dotenv

# --- ReportLab imports for PDF generation ---
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

load_dotenv()

st.set_page_config(
    page_title="LK SME Advisor | Enterprise AI",
    page_icon="🇱🇰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Import Modern Font Stack */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    /* Hero Header Card */
    .hero-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: #FFFFFF;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        margin-bottom: 2rem;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(79, 70, 229, 0.2);
        border: 1px solid rgba(129, 140, 248, 0.3);
        color: #A5B4FC;
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        color: #FFFFFF;
        margin: 0 0 0.5rem 0;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #94A3B8;
        line-height: 1.6;
        margin: 0;
    }

    /* Input & Interactive Cards */
    .stTextArea textarea {
        border-radius: 12px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 1rem !important;
        font-size: 0.95rem !important;
        transition: all 200ms ease-in-out !important;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
    }

    .stTextArea textarea:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15) !important;
    }

    /* Primary Action Buttons */
    .stButton>button[kind="primary"] {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25) !important;
        transition: all 200ms ease-in-out !important;
    }

    .stButton>button[kind="primary"]:hover {
        background-color: #4338CA !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 16px rgba(79, 70, 229, 0.35) !important;
    }

    /* Output Card */
    .report-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 16px;
        padding: 2.5rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.05);
        margin-top: 1.5rem;
    }

    /* Sidebar Clean styling */
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

def generate_pdf_report(markdown_text: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=12
    )
    heading_style = ParagraphStyle(
        'ReportHeading',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'ReportBody',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    story = []
    story.append(Paragraph("🇱🇰 Sri Lankan SME Advisory Report", title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=12))

    for line in markdown_text.split('\n'):
        clean_line = line.strip()
        if not clean_line:
            continue
        
        # Simple Markdown Bold replacement for PDF Paragraphs
        formatted_line = clean_line.replace('**', '<b>', 1)
        while '**' in formatted_line:
            formatted_line = formatted_line.replace('**', '</b>', 1)
        
        if clean_line.startswith('# '):
            story.append(Paragraph(formatted_line[2:], title_style))
        elif clean_line.startswith('## ') or clean_line.startswith('### '):
            h_text = formatted_line.lstrip('#').strip()
            story.append(Paragraph(h_text, heading_style))
        elif clean_line.startswith('* ') or clean_line.startswith('- '):
            bullet_txt = f"• {formatted_line[2:]}"
            story.append(Paragraph(bullet_txt, body_style))
        else:
            story.append(Paragraph(formatted_line, body_style))
        
        story.append(Spacer(1, 3))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


with st.spinner("⚡ Initializing Advisory Graph & Cloud Vector Index..."):
    from graph import app_graph


with st.sidebar:
    st.markdown("### 🛠️ Architecture Overview")
    st.caption("Agentic workflow grounded in official Sri Lankan Inland Revenue Department (IRD) & Central Bank (CBSL) regulations.")
    
    st.divider()
    st.markdown("#### ⚡ AI Engine Stack")
    st.markdown("""
    * **Orchestrator:** Llama 3.1 8B (Groq)
    * **Reasoning Agent:** Llama 3.3 70B (OpenRouter)
    * **Vector Database:** Pinecone Serverless
    * **Embeddings:** BAAI/bge-small-en-v1.5
    """)
    
    st.divider()
    st.markdown("#### 💡 Preset Query Templates")
    
    preset_1 = "I operate a registered IT service firm in Colombo with 8 employees. How do I apply for a CBSL technology modernization loan and calculate tax obligations?"
    preset_2 = "What are the mandatory tax registration steps and IRD TIN requirements for a new agricultural export SME in Kandy?"
    
    if st.button("📌 Preset: Tech SME Loan & Tax", use_container_width=True):
        st.session_state["query_input"] = preset_1
        
    if st.button("📌 Preset: Agro Export TIN Guide", use_container_width=True):
        st.session_state["query_input"] = preset_2


st.markdown("""
<div class="hero-card">
    <div class="hero-badge">🇱🇰 Agentic RAG Platform</div>
    <h1 class="hero-title">Sri Lankan SME Business & Tax Advisor</h1>
    <p class="hero-subtitle">Production-grade multi-agent intelligence providing tax liability calculations, registration roadmaps, and financial guidance grounded in official Sri Lankan legal frameworks.</p>
</div>
""", unsafe_allow_html=True)


if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""

user_query = st.text_area(
    "Describe your business query or operational requirement:",
    value=st.session_state["query_input"],
    placeholder="e.g., I run a manufacturing business in Gampaha with 12 workers. What are my tax obligations under the latest IRD guidelines, and how can I access SME credit lines?",
    height=120
)

col_run, col_clear = st.columns([4, 1])

with col_run:
    run_button = st.button("Run Multi-Agent Advisory Pipeline", type="primary", use_container_width=True)

with col_clear:
    if st.button("Clear", use_container_width=True):
        st.session_state["query_input"] = ""
        st.rerun()


if run_button:
    if not user_query.strip():
        st.warning("Please provide a valid query before executing the pipeline.")
    else:
        initial_state = {
            "user_query": user_query,
            "intent": "",
            "retrieved_docs": [],
            "financial_analysis": "",
            "final_report": "",
            "messages": []
        }
        
        st.markdown("---")
        
        with st.status("Multi-Agent Pipeline Executing...", expanded=True) as status_box:
            final_state = initial_state
            
            for output in app_graph.stream(initial_state):
                for node, state_update in output.items():
                    st.write(f"✓ **Agent Executed:** `{node}`")
                    
                    if "messages" in state_update and state_update["messages"]:
                        st.info(state_update["messages"][-1])
                        
                    final_state.update(state_update)
                    
            status_box.update(label="✅ Advisory Compilation Complete!", state="complete", expanded=False)
        
        st.markdown("### Executive Advisory Report")
        
        report_markdown = final_state.get("final_report", "No report generated.")
        
        st.markdown(f'<div class="report-container">', unsafe_allow_html=True)
        st.markdown(report_markdown)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        pdf_bytes = generate_pdf_report(report_markdown)
        
        col_download, col_spacer = st.columns([2, 3])
        with col_download:
            st.download_button(
                label="Download Official Advisory Report (PDF)",
                data=pdf_bytes,
                file_name="Sri_Lanka_SME_Advisory_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )