from groq import Groq
from app.utils.chunker import split_text
from app.services.text_cleaner import clean_text
from app.core.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

# Define token length for different summary types
LENGTH_CONFIG = {
    "short": 80,
    "medium": 150,
    "long": 300
}

def summarize_text(text: str, length: str = "medium") -> str:
    """
    Summarizes the input text using Groq API.
    
    Args:
        text (str): The input text to summarize.
        length (str): Length of summary ('short', 'medium', 'long').
    
    Returns:
        str: The combined summarized text.
    """

    if not text.strip():
        return "No text provided for summarization."

    # Clean the text (remove unwanted spaces, characters, etc.)
    cleaned_text = clean_text(text)

    # Split text into smaller chunks for large documents
    chunks = split_text(cleaned_text)

    # Set max tokens based on length
    max_tokens = LENGTH_CONFIG.get(length.lower(), 150)

    summaries = []

    for idx, chunk in enumerate(chunks, start=1):
        try:
            response = client.chat.completions.create(
                model="qwen/qwen3-32b",  # Make sure your API key has access to this model
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a helpful assistant. Summarize the document in {length} length."
                    },
                    {
                        "role": "user",
                        "content": chunk
                    }
                ],
                max_tokens=max_tokens,
            )

            # Extract the assistant's response
            summary_chunk = response.choices[0].message.content
            summaries.append(summary_chunk.strip())

        except Exception as e:
            # Log the error and continue with next chunk
            summaries.append(f"[Error summarizing chunk {idx}: {e}]")

    # Combine all chunk summaries into a single text
    final_summary = " ".join(summaries)
    return final_summary if final_summary else "Unable to generate summary."
