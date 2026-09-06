import os
from dotenv import load_dotenv
from google import genai

def chunk_text(text, max_chunk_chars=500):
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current_chunk = []
    current_length = 0

    for paragraph in paragraphs:
        paragraph_length = len(paragraph)
        if current_length + paragraph_length > max_chunk_chars and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_length = 0
        current_chunk.append(paragraph)
        current_length += paragraph_length

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks

with open("report_operations.txt") as f:
    text = f.read()

chunks = chunk_text(text, max_chunk_chars=500)
print(f"Split into {len(chunks)} chunks")
for i, chunk in enumerate(chunks):
    print(f"--- Chunk {i+1} ({len(chunk)} chars) ---")
    print(chunk[:100] + "...")
    
chunks = chunk_text(text, max_chunk_chars=1000)
print(f"With larger limit: {len(chunks)} chunks")
for i, chunk in enumerate(chunks):
    paragraph_count = chunk.count("\n\n") + 1
    print(f"Chunk {i+1}: {len(chunk)} chars, {paragraph_count} paragraph(s)")

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def summarize_chunk(chunk_text):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=f"Summarize the key points from this section in 2-3 sentences:\n\n{chunk_text}"
    )
    return response.text

chunk_summaries = [summarize_chunk(chunk) for chunk in chunks]

def combine_summaries(chunk_summaries, source_label):
    combined_text = "\n\n".join(chunk_summaries)
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=(
            f"Combine these section summaries from a report titled '{source_label}' "
            f"into one cohesive paragraph, removing repetition:\n\n{combined_text}"
        )
    )
    return response.text

operations_digest = combine_summaries(chunk_summaries, "Operations Update")
print(operations_digest)

def summarize_document(filepath, label):
    with open(filepath) as f:
        text = f.read()
    chunks = chunk_text(text, max_chunk_chars=500)
    chunk_summaries = [summarize_chunk(chunk) for chunk in chunks]
    return combine_summaries(chunk_summaries, label)

documents = [
    ("report_operations.txt", "Operations Update"),
    ("report_marketing.txt", "Marketing Update"),
]

section_digests = []
for filepath, label in documents:
    digest = summarize_document(filepath, label)
    section_digests.append(f"{label}:\n{digest}")

full_digest = "\n\n".join(section_digests)
print(full_digest)