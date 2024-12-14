import os
import openai
from dotenv import load_dotenv
import heapq
import tiktoken

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Utility function to count tokens using tiktoken (for gpt-3.5-turbo)
def count_tokens(text: str, model="gpt-3.5-turbo") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def chat_completion_request(messages, max_tokens=300, temperature=0.7):
    return openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

def summarize_text(section_text: str, section_name: str) -> str:
    if not section_text.strip():
        return f"No {section_name} section found."

    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes academic text."},
        {"role": "user", "content": f"Please provide a concise summary of the following {section_name} section:\n\n{section_text}\n\nSummary:"}
    ]
    response = chat_completion_request(messages, max_tokens=200)
    return response.choices[0].message.content.strip()

def chunk_text(full_text: str, max_tokens_per_chunk=3000) -> list:
    """
    Split the text into manageable chunks based on token count.
    Adjust `max_tokens_per_chunk` as needed.
    """
    words = full_text.split()
    chunks = []
    current_chunk = []
    current_count = 0

    for w in words:
        # Rough token estimate (approximate words to tokens ratio for English is ~1.3, but this is a simplification)
        # For better accuracy, you could dynamically count tokens with tiktoken as you add words.
        current_count += 1
        current_chunk.append(w)
        if current_count >= max_tokens_per_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(chunk_text)
            current_chunk = []
            current_count = 0

    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append(chunk_text)

    return chunks

def summarize_large_text(full_text: str) -> str:
    """
    For very large texts, chunk the text, summarize each chunk, then summarize the summaries.
    """
    # First, chunk the text
    chunks = chunk_text(full_text, max_tokens_per_chunk=2000)

    # Summarize each chunk
    chunk_summaries = []
    for i, ctext in enumerate(chunks):
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes academic text."},
            {"role": "user", "content": f"Summarize the following part of a paper:\n\n{ctext}\n\nSummary:"}
        ]
        response = chat_completion_request(messages, max_tokens=500)
        chunk_summaries.append(response.choices[0].message.content.strip())

    # Now summarize all chunk summaries into a final summary
    combined_summary = "\n\n".join(chunk_summaries)
    messages = [
        {"role": "system", "content": "You are a helpful assistant that summarizes academic text."},
        {"role": "user", "content": f"Combine and summarize these chunk summaries into a final concise summary:\n\n{combined_summary}\n\nFinal Summary:"}
    ]
    final_response = chat_completion_request(messages, max_tokens=500)
    final_summary = final_response.choices[0].message.content.strip()
    return final_summary

def summarize_full_text(full_text: str) -> str:
    """
    Summarize the entire paper. If the text is too large, use chunking strategy.
    """
    # If the text is small enough, try a direct summarization
    # Check token count
    if count_tokens(full_text) < 12000:
        # Summarize directly
        messages = [
            {"role": "system", "content": "You are a helpful assistant that summarizes academic papers."},
            {"role": "user", "content": f"Please provide a concise summary of the entire paper:\n\n{full_text}\n\nSummary:"}
        ]
        response = chat_completion_request(messages, max_tokens=500)
        return response.choices[0].message.content.strip()
    else:
        # Use the chunked summarization approach
        return summarize_large_text(full_text)

def answer_question(question: str, full_text: str, full_summary: str) -> str:
    # We still try to find relevant paragraphs, but we have a reliable full_summary
    paragraphs = [p.strip() for p in full_text.split("\n") if p.strip()]

    query_words = set(question.lower().split())
    scored_paragraphs = []
    for p in paragraphs:
        p_words = set(p.lower().split())
        score = len(query_words.intersection(p_words))
        if score > 0:
            scored_paragraphs.append((score, p))

    top_paragraphs = heapq.nlargest(5, scored_paragraphs, key=lambda x: x[0])
    context_paragraphs = "\n\n".join([p for _, p in top_paragraphs])

    if not context_paragraphs:
        context_paragraphs = full_summary
    else:
        context_paragraphs = full_summary + "\n\n" + context_paragraphs

    messages = [
        {"role": "system", "content": "You are a helpful assistant that accurately answers questions about academic paper content."},
        {"role": "user", "content": f"Use the following paper summary and context excerpts:\n\n{context_paragraphs}\n\nQuestion: {question}\n\nPlease answer concisely:"}
    ]

    response = chat_completion_request(messages, max_tokens=300)
    return response.choices[0].message.content.strip()
