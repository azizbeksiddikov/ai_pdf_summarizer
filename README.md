README
Overview
This project provides a tool for interacting with academic PDFs using OpenAI’s GPT models. The application allows you to:

Extract text from a PDF:
Parse the PDF content into text for analysis.

Identify and Summarize Key Sections (Abstract, Methods, Results):
Automatically locate these sections in the paper and summarize them using the LLM.

Generate a Full Paper Summary:
Produce a top-level summary of the entire paper, even for very large documents (via chunked summarization).

Question & Answer Interface:
Ask the system questions about the paper, leveraging both the full text and the top-level summary to provide concise and accurate answers.

User Interface (UI):
An optional Gradio-based UI enables a user-friendly interface for uploading PDFs, viewing summaries, and asking questions interactively.

Project Structure
graphql
Copy code
project/
│
├─ pdf_utils.py # Functions for PDF text extraction and section identification
├─ llm_utils.py # Functions to summarize text, summarize full papers, and answer questions
├─ main.py # Console-based interface to process a PDF and interact via Q&A
├─ ui.py # Gradio-based graphical interface for file upload, summaries, and Q&A
├─ .env # Store your OpenAI API key (not committed to version control)
├─ .gitignore # Ignore secrets and other non-committed files (e.g., .env)
└─ input/
└─ input.pdf # Example input PDF file
Requirements
Python 3.9 or newer (recommended)
openai Python library
pdfplumber for PDF extraction
python-dotenv for loading environment variables
tiktoken for token counting
gradio for the optional web UI
Installation
Clone the repository (if using version control):

bash
Copy code
git clone https://example.com/your-repo.git
cd project
Create and activate a virtual environment (optional but recommended):

bash
Copy code
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
If you don't have a requirements.txt, install packages manually:

bash
Copy code
pip install openai pdfplumber python-dotenv gradio tiktoken
Set your OpenAI API key:
Create a .env file at the project root:

bash
Copy code
echo "OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxx" > .env
Replace sk-xxxxxxxx... with your actual API key.

Usage

1. Console Mode
   Place your PDF in the input directory (e.g., input.pdf).
   Adjust main.py if needed (e.g., change the PDF filename).
   Run:
   bash
   Copy code
   python main.py
   You will see:

Summaries of Abstract, Methods, Results
A full paper summary
A prompt to ask questions interactively in the console.
Type your questions and press enter. Type exit to quit.

2. Web UI Mode
   Run:
   bash
   Copy code
   python ui.py
   This will launch a local Gradio interface. Open the given URL in your web browser.
   Upload a PDF in the UI.
   The application will display summaries and a full paper summary.
   You can then ask questions about the paper through the text box.

Handling Large Documents
If you encounter errors about the model’s maximum context length, the code attempts to chunk and summarize the text. For extremely large PDFs, consider further reducing the chunk sizes or using a more advanced retrieval method (e.g., embeddings + vector databases).

Customizing Section Detection
In pdf_utils.py, you can modify the SECTION_VARIANTS dictionary to include other synonyms for the sections, making the extraction more robust to formatting differences.

Additional Notes
Make sure your API key is valid and you have the right access to the OpenAI model (gpt-3.5-turbo or gpt-4).
The chunking and summarization strategy in llm_utils.py can be refined if you have very large documents.
The Q&A strategy currently uses a simple keyword search to find relevant paragraphs. For more advanced retrieval, integrate embeddings and a vector database.
