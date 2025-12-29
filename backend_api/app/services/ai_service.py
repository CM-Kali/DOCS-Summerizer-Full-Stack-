from groq import Groq
from app.utils.chunker import split_text
from app.services.text_cleaner import clean_text
from app.core.config import GROQ_API_KEY



client = Groq(api_key=GROQ_API_KEY)

LENGTH_CONFIG = {
    "short": 80,
    "medium": 5000,
    "long": 800
}

def summarize_text(text: str, length: str = "medium") -> str:
    if not text.strip():
        return "No text provided for summarization."

    cleaned_text = clean_text(text)
    chunks = split_text(cleaned_text)
    max_tokens = LENGTH_CONFIG.get(length.lower(), 150)
    summaries = []

    for idx, chunk in enumerate(chunks, start=1):
        try:
            response = client.chat.completions.create(
                model="qwen/qwen3-32b",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            f"You are a professional  AI assistant that ONLY generates a concise {length} summary "
                            "of the text provided. Do NOT include thinking , reasong and  explanations, internal thoughts, "
                            "or phrases like '<think>' or 'Okay'. Output only the summary."
                        )
                    },
                    {
                        "role": "user",
                        "content": chunk
                    }
                ],
                max_tokens=max_tokens
            )

            summary_chunk = response.choices[0].message.content.strip()
            summaries.append(summary_chunk)

        except Exception as e:
            summaries.append(f"[Error summarizing chunk {idx}: {e}]")

    final_summary = " ".join(summaries)
    return final_summary if final_summary else "Unable to generate summary."
