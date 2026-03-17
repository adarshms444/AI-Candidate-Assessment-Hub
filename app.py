# #working code

# import gradio as gr
# import time
# import os
# import shutil
# import re

# # Import your working backend modules
# from main import build_graph
# from ingestion.resume_loader import load_resumes, read_pdf, read_docx
# from ingestion.job_parser import parse_job_description
# from retrieval.vector_store import index_resumes

# def setup_directories():
#     os.makedirs("data/resumes", exist_ok=True)

# def process_resumes(uploaded_files):
#     save_dir = "data/resumes"
#     setup_directories()
#     for filename in os.listdir(save_dir):
#         filepath = os.path.join(save_dir, filename)
#         if os.path.isfile(filepath):
#             os.remove(filepath)
#     if uploaded_files:
#         for file in uploaded_files:
#             filename = os.path.basename(file.name)
#             shutil.copy(file.name, os.path.join(save_dir, filename))

# def process_jd(jd_file):
#     setup_directories()
#     if not jd_file: return
#     ext = os.path.splitext(jd_file.name)[1].lower()
#     if ext == '.pdf': text = read_pdf(jd_file.name)
#     elif ext == '.docx': text = read_docx(jd_file.name)
#     else:
#         with open(jd_file.name, 'r', encoding='utf-8') as f:
#             text = f.read()
#     with open("data/job_description.txt", "w", encoding="utf-8") as f:
#         f.write(text)

# def chat_with_recruiter(user_message, history, resume_files, jd_file):
#     if not resume_files or not jd_file:
#         history.append({"role": "user", "content": user_message})
#         history.append({"role": "assistant", "content": "### ⚠️ System Alert\n**Missing Context:** Please upload both Candidate Resumes and the Job Description."})
#         yield "", history
#         return

#     history.append({"role": "user", "content": user_message})
    
#     # Initialize clean Markdown terminal block
#     agent_log = "### ⚙️ langgraph_execution_engine.sh\n```log\n[SYSTEM] Initializing AI Recruiter Agents...\n"
#     history.append({"role": "assistant", "content": agent_log + "```"})
#     yield "", history

#     start_time = time.time()
#     try:
#         process_resumes(resume_files)
#         process_jd(jd_file)
        
#         exp_match = re.search(r'(\d+)\s*(?:years|yrs|year)', user_message.lower())
#         min_exp = int(exp_match.group(1)) if exp_match else 0
        
#         resumes = load_resumes("data/resumes")
#         job_clusters = parse_job_description("data/job_description.txt")
#         index_resumes(resumes)
#         app_graph = build_graph()
        
#         initial_state = {
#             "query": user_message, 
#             "min_experience": min_exp,
#             "resumes": resumes,
#             "job_clusters": job_clusters,
#             "retrieved": [],
#             "scores": [],
#             "route": "",
#             "comparison_prob": 0.0,
#             "reports": []
#         }
        
#         final_reports = []
        
#         # Stream Agent Updates using PURE text (No HTML tags!)
#         for output in app_graph.stream(initial_state):
#             for node_name, state_update in output.items():
#                 agent_name = node_name.replace("_node", "").replace("_agent", "").upper()
                
#                 # Append pure text line to the log
#                 agent_log += f"[SUCCESS] {agent_name}_AGENT execution completed.\n"
                
#                 # Close the markdown block temporarily so Gradio renders it
#                 history[-1]["content"] = agent_log + "```"
#                 yield "", history
                
#                 if "reports" in state_update:
#                     final_reports = state_update["reports"]
        
#         # Finish the terminal log
#         agent_log += "[SYSTEM] Pipeline finished. Outputting results...\n```"
#         end_time = time.time()
        
#         # Format the final output cards
#         if not final_reports:
#             bot_response = agent_log + f"\n\n### ⚠️ No Matches Found\nNone of the candidates passed the semantic thresholds or the **{min_exp}-year** experience requirement."
#         else:
#             bot_response = agent_log + f"\n\n### 📊 Final Evaluation Report\n*Analyzed **{len(resumes)}** candidates in **{end_time - start_time:.2f}s**.*\n\n---\n\n"
#             for report in final_reports:
#                 # We can safely use HTML here because it's OUTSIDE the Markdown code block
#                 if "Fit: High" in report:
#                     report = report.replace("Fit: High", "<span style='color: #10B981; font-weight: bold;'>Fit: High 🟢</span>")
#                 elif "Fit: Medium" in report:
#                     report = report.replace("Fit: Medium", "<span style='color: #F59E0B; font-weight: bold;'>Fit: Medium 🟡</span>")
#                 else:
#                     report = report.replace("Fit: Low", "<span style='color: #EF4444; font-weight: bold;'>Fit: Low 🔴</span>")
                
#                 bot_response += f"{report}\n\n---\n\n"

#         history[-1]["content"] = bot_response
#         yield "", history

#     except Exception as e:
#         history[-1]["content"] = f"### ❌ System Error\n`{str(e)}`"
#         yield "", history


# # --- ENTERPRISE DARK MODE CSS ---
# custom_css = """
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

# /* Force Global Dark Background */
# body, .gradio-container {
#     font-family: 'Inter', sans-serif !important;
#     background-color: #0B0F19 !important; /* Deep Midnight Blue */
#     color: #E5E7EB !important;
# }

# /* App Header Gradient */
# .app-header {
#     background: linear-gradient(90deg, #111827 0%, #1F2937 100%);
#     padding: 24px;
#     border-radius: 12px;
#     margin-bottom: 24px;
#     border: 1px solid #374151;
#     box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
# }
# .app-header h1 {
#     color: #F9FAFB !important;
#     margin: 0 !important;
#     font-size: 1.8rem !important;
#     font-weight: 700 !important;
# }
# .app-header p {
#     color: #9CA3AF !important;
#     margin: 4px 0 0 0 !important;
# }

# /* Dark Floating Panels */
# .panel-card {
#     background-color: #111827 !important;
#     border: 1px solid #374151 !important;
#     border-radius: 12px !important;
#     padding: 20px !important;
#     box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
# }

# /* Chatbot Specifics */
# .message-wrap .bot {
#     background-color: #1F2937 !important; 
#     border: 1px solid #374151 !important;
#     color: #F3F4F6 !important;
# }
# .message-wrap .user {
#     background-color: #2563EB !important; 
#     color: #FFFFFF !important;
#     border: none !important;
# }
# """

# # Force Dark Mode Theme overrides
# enterprise_theme = gr.themes.Base(
#     primary_hue="blue",
#     neutral_hue="slate",
#     font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
# ).set(
#     body_background_fill="#0B0F19",
#     block_background_fill="#111827",
#     block_border_color="#374151",
#     block_label_text_color="#9CA3AF",
#     body_text_color="#F3F4F6",
#     color_accent_soft="#1E3A8A"
# )

# # --- UI LAYOUT ---
# with gr.Blocks(title="AI Recruiter Copilot") as demo:
    
#     with gr.Row(elem_classes="app-header"):
#         gr.Markdown(
#             """
#             # ⚡ AI Candidate Assessment Hub
#             *Enterprise-grade hybrid retrieval and LangGraph evaluation engine.*
#             """
#         )
    
#     with gr.Row():
#         with gr.Column(scale=3, elem_classes="panel-card"):
#             gr.Markdown("### 🗂️ Workspace Context")
#             gr.Markdown("<span style='color: #9CA3AF; font-size: 0.9em;'>Supply the system with the targeted job description and the raw candidate pool.</span><br><br>")
            
#             jd_upload = gr.File(
#                 label="Target Job Description (JD)", 
#                 file_count="single",
#                 file_types=[".pdf", ".docx", ".txt"]
#             )
            
#             resume_uploads = gr.File(
#                 label="Candidate Resumes (Batch Upload)", 
#                 file_count="multiple",
#                 file_types=[".pdf", ".docx", ".txt"]
#             )
            
#         with gr.Column(scale=7, elem_classes="panel-card"):
#             # FIX: Removed the avatar_images parameter completely to avoid Windows OS path conflicts
#             chatbot = gr.Chatbot(
#                 label="Recruitment Copilot Agent", 
#                 height=600
#             )
            
#             with gr.Row():
#                 chat_input = gr.Textbox(
#                     label="Command Prompt",
#                     placeholder="e.g., Evaluate these candidates for a role requiring 3 years of experience...",
#                     lines=1,
#                     scale=5
#                 )
#                 submit_btn = gr.Button("Analyze 🚀", variant="primary", scale=1)
#                 clear_btn = gr.ClearButton([chat_input, chatbot], value="Clear", scale=1)

#     # Wire logic
#     chat_input.submit(
#         fn=chat_with_recruiter, 
#         inputs=[chat_input, chatbot, resume_uploads, jd_upload], 
#         outputs=[chat_input, chatbot]
#     )
#     submit_btn.click(
#         fn=chat_with_recruiter, 
#         inputs=[chat_input, chatbot, resume_uploads, jd_upload], 
#         outputs=[chat_input, chatbot]
#     )

# if __name__ == "__main__":
#     demo.launch(theme=enterprise_theme, css=custom_css)



import gradio as gr
import time
import os
import shutil
import re

# Import your working backend modules
from main import build_graph
from ingestion.resume_loader import load_resumes, read_pdf, read_docx
from ingestion.job_parser import parse_job_description
from retrieval.vector_store import index_resumes

def setup_directories():
    os.makedirs("data/resumes", exist_ok=True)

def process_resumes(uploaded_files):
    save_dir = "data/resumes"
    setup_directories()
    for filename in os.listdir(save_dir):
        filepath = os.path.join(save_dir, filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
    if uploaded_files:
        for file in uploaded_files:
            filename = os.path.basename(file.name)
            shutil.copy(file.name, os.path.join(save_dir, filename))

def process_jd(jd_file):
    setup_directories()
    if not jd_file: return
    ext = os.path.splitext(jd_file.name)[1].lower()
    if ext == '.pdf': text = read_pdf(jd_file.name)
    elif ext == '.docx': text = read_docx(jd_file.name)
    else:
        with open(jd_file.name, 'r', encoding='utf-8') as f:
            text = f.read()
    with open("data/job_description.txt", "w", encoding="utf-8") as f:
        f.write(text)

def chat_with_recruiter(user_message, history, resume_files, jd_file):
    if not resume_files or not jd_file:
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": "### ⚠️ System Alert\n**Missing Context:** Please upload both Candidate Resumes and the Job Description."})
        yield "", history
        return

    history.append({"role": "user", "content": user_message})
    
    agent_log = "### ⚙️ langgraph_execution_engine.sh\n```log\n[SYSTEM] Initializing AI Recruiter Agents...\n"
    history.append({"role": "assistant", "content": agent_log + "```"})
    yield "", history

    start_time = time.time()
    try:
        process_resumes(resume_files)
        process_jd(jd_file)
        
        exp_match = re.search(r'(\d+)\s*(?:years|yrs|year)', user_message.lower())
        min_exp = int(exp_match.group(1)) if exp_match else 0
        
        resumes = load_resumes("data/resumes")
        job_clusters = parse_job_description("data/job_description.txt")
        index_resumes(resumes)
        app_graph = build_graph()
        
        initial_state = {
            "query": user_message, 
            "min_experience": min_exp,
            "resumes": resumes,
            "job_clusters": job_clusters,
            "retrieved": [],
            "scores": [],
            "route": "",
            "comparison_prob": 0.0,
            "reports": []
        }
        
        final_reports = []
        
        for output in app_graph.stream(initial_state):
            for node_name, state_update in output.items():
                agent_name = node_name.replace("_node", "").replace("_agent", "").upper()
                agent_log += f"[SUCCESS] {agent_name}_AGENT execution completed.\n"
                
                history[-1]["content"] = agent_log + "```"
                yield "", history
                
                if "reports" in state_update:
                    final_reports = state_update["reports"]
        
        agent_log += "[SYSTEM] Pipeline finished. Outputting results...\n```"
        end_time = time.time()
        
        if not final_reports:
            bot_response = agent_log + f"\n\n### ⚠️ No Matches Found\nNone of the candidates passed the semantic thresholds or the **{min_exp}-year** experience requirement."
        else:
            bot_response = agent_log + f"\n\n### 📊 Final Evaluation Report\n*Analyzed **{len(resumes)}** candidates in **{end_time - start_time:.2f}s**.*\n\n---\n\n"
            for report in final_reports:
                if "Fit: High" in report:
                    report = report.replace("Fit: High", "<span style='color: #10B981; font-weight: bold;'>Fit: High 🟢</span>")
                elif "Fit: Medium" in report:
                    report = report.replace("Fit: Medium", "<span style='color: #F59E0B; font-weight: bold;'>Fit: Medium 🟡</span>")
                else:
                    report = report.replace("Fit: Low", "<span style='color: #EF4444; font-weight: bold;'>Fit: Low 🔴</span>")
                
                bot_response += f"{report}\n\n---\n\n"

        history[-1]["content"] = bot_response
        yield "", history

    except Exception as e:
        history[-1]["content"] = f"### ❌ System Error\n`{str(e)}`"
        yield "", history


# --- ENTERPRISE DARK MODE CSS WITH HIGH CONTRAST ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* Deep, immersive background */
body, .gradio-container {
    font-family: 'Inter', sans-serif !important;
    background-color: #0f172a !important; /* Slate 900 */
    color: #f8fafc !important;
}

/* Gradient Header */
.app-header {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
    padding: 24px 32px;
    border-radius: 16px;
    margin-bottom: 16px;
    border: 1px solid #4338ca;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
}
.app-header h1 {
    color: #ffffff !important;
    margin: 0 !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

/* System Status Bar */
.status-bar {
    background-color: #1e293b;
    border-radius: 8px;
    padding: 10px 20px;
    font-size: 0.85rem;
    color: #94a3b8;
    display: flex;
    justify-content: space-between;
    margin-bottom: 24px;
    border: 1px solid #334155;
}

/* High Contrast Floating Panels */
.panel-card {
    background-color: #1e293b !important; /* Lighter Slate for contrast */
    border: 1px solid #334155 !important;
    border-top: 4px solid #3b82f6 !important; /* Electric Blue Accent Line */
    border-radius: 12px !important;
    padding: 24px !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3) !important;
}

/* Enhancing the Chat Bubbles */
.message-wrap .bot {
    background-color: #0f172a !important; /* Dark contrast for bot */
    border: 1px solid #334155 !important;
    color: #f1f5f9 !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}
.message-wrap .user {
    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important; /* Vibrant Blue/Purple for User */
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 6px rgba(37, 99, 235, 0.3);
}

/* Styled Quick Action Buttons */
.quick-btn {
    background-color: #334155 !important;
    color: #f8fafc !important;
    border: 1px solid #475569 !important;
    transition: all 0.2s ease;
}
.quick-btn:hover {
    background-color: #475569 !important;
    border-color: #64748b !important;
    transform: translateY(-1px);
}
"""

# Force Dark Mode Theme overrides
enterprise_theme = gr.themes.Base(
    primary_hue="indigo",
    neutral_hue="slate",
    font=[gr.themes.GoogleFont("Inter"), "system-ui", "sans-serif"],
).set(
    body_background_fill="#0f172a",
    block_background_fill="#1e293b",
    block_border_color="#334155",
    block_label_text_color="#94a3b8",
    body_text_color="#f8fafc",
    color_accent_soft="#3b82f6"
)

# --- UI LAYOUT ---
with gr.Blocks(title="AI Recruiter Copilot", theme=enterprise_theme, css=custom_css) as demo:
    
    # 1. Header
    with gr.Row(elem_classes="app-header"):
        gr.Markdown(
            """
            # ⚡ AI Candidate Assessment Hub
            *Enterprise-grade hybrid retrieval and LangGraph evaluation engine.*
            """
        )
    
    # 2. System Status Bar (New Feature)
    gr.Markdown(
        """
        <div class="status-bar">
            <span>🟢 System Online</span>
            <span>🧠 LLM Engine: <b>NVIDIA Nim</b></span>
            <span>🗄️ Vector DB: <b>ChromaDB (Local)</b></span>
            <span>⚙️ Workflow: <b>LangGraph Multi-Agent</b></span>
        </div>
        """
    )
    
    with gr.Row():
        
        # LEFT COLUMN (Controls)
        with gr.Column(scale=3, elem_classes="panel-card"):
            gr.Markdown("### 🗂️ 1. Knowledge Base")
            gr.Markdown("<span style='color: #94a3b8; font-size: 0.85em;'>Supply context for the evaluation.</span>")
            
            with gr.Accordion("Upload Documents", open=True):
                jd_upload = gr.File(
                    label="Target Job Description (JD)", 
                    file_count="single",
                    file_types=[".pdf", ".docx", ".txt"]
                )
                resume_uploads = gr.File(
                    label="Candidate Resumes (Batch Upload)", 
                    file_count="multiple",
                    file_types=[".pdf", ".docx", ".txt"]
                )
            
            gr.Markdown("<br>### ⚡ 2. Quick Commands")
            gr.Markdown("<span style='color: #94a3b8; font-size: 0.85em;'>Use these templates to quickly query the system.</span>")
            
            # Quick Action Buttons (New Feature)
            btn_q1 = gr.Button("🔍 Find best overall fit", elem_classes="quick-btn")
            btn_q2 = gr.Button("⏱️ Filter for 3+ years experience", elem_classes="quick-btn")
            btn_q3 = gr.Button("🎯 Strict match for Vector Databases", elem_classes="quick-btn")

        # RIGHT COLUMN (Chatbot)
        with gr.Column(scale=7, elem_classes="panel-card"):
            chatbot = gr.Chatbot(
                label="Recruitment Copilot Agent", 
                height=550
            )
            
            with gr.Row():
                chat_input = gr.Textbox(
                    label="Command Prompt",
                    placeholder="Type your requirements here...",
                    lines=1,
                    scale=5
                )
                submit_btn = gr.Button("Analyze 🚀", variant="primary", scale=1)
                clear_btn = gr.ClearButton([chat_input, chatbot], value="Clear", scale=1)

    # --- WIRING THE LOGIC ---
    
    # Wire the Quick Prompts to automatically fill the text box
    btn_q1.click(lambda: "Evaluate all candidates and find the best overall fit based on the Job Description.", None, chat_input)
    btn_q2.click(lambda: "Find me the best candidates who have strictly 3 years of experience or more.", None, chat_input)
    btn_q3.click(lambda: "Evaluate candidates with a strong focus on Vector Databases, FAISS, and ChromaDB.", None, chat_input)

    # Wire the Chat Execution
    chat_input.submit(
        fn=chat_with_recruiter, 
        inputs=[chat_input, chatbot, resume_uploads, jd_upload], 
        outputs=[chat_input, chatbot]
    )
    submit_btn.click(
        fn=chat_with_recruiter, 
        inputs=[chat_input, chatbot, resume_uploads, jd_upload], 
        outputs=[chat_input, chatbot]
    )

if __name__ == "__main__":
    demo.launch()