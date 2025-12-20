from groq import Groq
from app.utils.chunker import split_text
from app.services.text_cleaner import clean_text
from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def summarize_text(text: str) -> str:
    # 1. Clean text
    cleaned_text = clean_text(text)

    # 2. Split long document
    chunks = split_text(cleaned_text)

    summaries = []

    # 3. Send each chunk to Groq
    for chunk in chunks:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "You summarize documents clearly and concisely."
                },
                {
                    "role": "user",
                    "content": chunk
                }
            ],
            max_tokens=150
        )

        summaries.append(response.choices[0].message.content)

    # 4. Merge summaries
    return " ".join(summaries)
