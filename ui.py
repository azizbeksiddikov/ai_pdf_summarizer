# ui.py
import gradio as gr
import os
from pdf_utils import extract_text_from_pdf, find_section
from llm_utils import summarize_text, answer_question, summarize_full_text

full_text_global = {"text": "", "full_summary": ""}

def process_pdf(file):
    if file is None:
        return "Please upload a PDF.", "", "", "", "", ""
    # Display loading status
    status = "Processing the PDF. Please wait..."
    yield status, "", "", "", "", ""  # Show immediate feedback

    file_path = file.name
    full_text = extract_text_from_pdf(file_path)
    full_text_global["text"] = full_text

    # Extract sections
    abstract_text = find_section(full_text, "Abstract")
    methods_text = find_section(full_text, "Methods")
    results_text = find_section(full_text, "Results")

    # Summarize sections
    status = "Summarizing sections..."
    yield status, "", "", "", "", ""
    abstract_summary = summarize_text(abstract_text, "Abstract")
    methods_summary = summarize_text(methods_text, "Methods")
    results_summary = summarize_text(results_text, "Results")

    # Summarize full text for better Q&A retrieval
    status = "Creating a top-level summary of the entire paper..."
    yield status, abstract_summary, methods_summary, results_summary, "", ""

    full_summary = summarize_full_text(full_text)
    full_text_global["full_summary"] = full_summary

    status = "Upload and processing complete. You can now ask questions."
    return status, abstract_summary, methods_summary, results_summary, full_summary, ""

def ask_question(question):
    if not full_text_global["text"]:
        return "Please upload and process a paper first."
    if not question.strip():
        return "Please ask a valid question."

    answer = answer_question(question, full_text_global["text"], full_text_global["full_summary"])
    return answer

def launch_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# Academic Paper Q&A Helper")
        gr.Markdown("""
        **Instructions**:
        1. Upload a PDF academic paper.
        2. The system will extract key sections and summarize them.
        3. A top-level summary of the entire paper will also be generated.
        4. Once processing is complete, you can ask questions about the paper.
        """)

        with gr.Row():
            pdf_input = gr.File(label="Upload PDF")

        status = gr.Markdown("Status will appear here...")
        abstract_output = gr.Markdown(label="Abstract Summary")
        methods_output = gr.Markdown(label="Methods Summary")
        results_output = gr.Markdown(label="Results Summary")
        full_summary_output = gr.Markdown(label="Full Paper Summary")

        process_button = gr.Button("Process PDF")
        
        process_button.click(
            process_pdf,
            inputs=[pdf_input],
            outputs=[status, abstract_output, methods_output, results_output, full_summary_output, gr.Textbox(visible=False)],
            api_name="process_pdf"
        )

        question_input = gr.Textbox(label="Ask a question about the paper:")
        answer_output = gr.Markdown(label="Answer")
        ask_button = gr.Button("Ask")

        ask_button.click(
            ask_question,
            inputs=[question_input],
            outputs=[answer_output]
        )

    demo.launch()

if __name__ == "__main__":
    launch_ui()
