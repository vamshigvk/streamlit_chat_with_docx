import streamlit as st
import PyPDF2
from huggingface_hub import InferenceClient

# Initialize DeepSeek client
client = InferenceClient()
model_id = "deepseek-ai/DeepSeek-V3-0324"

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def ask_deepseek(context, question):
    system_prompt = (
        "You are a helpful assistant. Use the provided context to answer the question."
        " If the answer is not in the context, say 'Not found in document'."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    completion = client.chat.completions.create(
        model=model_id,
        messages=messages,
    )
    return completion.choices[0].message.content

st.title("📄 PDF QnA using DeepSeek")

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    st.success("PDF uploaded successfully!")
    pdf_text = extract_text_from_pdf(uploaded_file)
    
    st.text_area(
        "Extracted Text (truncated)",
        pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text,
        height=300,
        key="pdf_text_area"  # ✅ Unique key added
    )

    question = st.text_input("Ask a question based on the PDF")

    if st.button("Get Answer") and question:
        with st.spinner("Thinking..."):
            answer = ask_deepseek(pdf_text, question)
        st.markdown("### ✅ Answer:")
        st.write(answer)