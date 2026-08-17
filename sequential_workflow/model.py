from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# 1. Create the Hugging Face LLM
# -----------------------------

llm = HuggingFaceEndpoint(
    repo_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.2
)

model = ChatHuggingFace(llm=llm)
