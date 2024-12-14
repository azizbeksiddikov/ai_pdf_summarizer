from pdf_utils import extract_text_from_pdf, find_section
from llm_utils import summarize_text, answer_question, summarize_full_text

import os

if __name__ == "__main__":
    # Specify the path to your input PDF file
    pdf_path = "input/Customer trust and willingness to use shopping assistant humanoid chatbot.pdf"
    
    # Extract the full text
    full_text = extract_text_from_pdf(pdf_path)
    
    # Identify sections
    abstract_text = find_section(full_text, "Abstract")
    methods_text = find_section(full_text, "Methods")
    results_text = find_section(full_text, "Results")
    
    # Summarize each section if found
    abstract_summary = summarize_text(abstract_text, "Abstract")
    methods_summary = summarize_text(methods_text, "Methods")
    results_summary = summarize_text(results_text, "Results")
    
    # Generate a top-level summary of the entire paper
    full_summary = summarize_full_text(full_text)
    
    # Print out the summaries
    print("=== Summaries ===")
    print("Abstract Summary:\n", abstract_summary, "\n")
    print("Methods Summary:\n", methods_summary, "\n")
    print("Results Summary:\n", results_summary, "\n")
    print("Full Paper Summary:\n", full_summary, "\n")

    # Q&A loop
    while True:
        user_q = input("Ask a question about the paper (or type 'exit' to quit): ")
        if user_q.lower() == 'exit':
            break
        answer = answer_question(user_q, full_text, full_summary)
        print("Answer:", answer, "\n")
        print("==========================")
"""
    
What are the real suggestions for businesses from this paper?
If I am a businessman, how can I use chatbots effectively?
"""

