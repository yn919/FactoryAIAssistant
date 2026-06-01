import os
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

SYSTEM_PROMPT = """
あなたは工場設備の専門家HMIアシスタントです。
作業者からの質問に対して、簡潔かつ実用的に日本語で回答してください。
回答は3行以内で、専門用語はわかりやすく説明してください。
"""
model = genai.GenerativeModel(
    "gemini-2.0-flash",
    system_instruction=SYSTEM_PROMPT
)

class Question(BaseModel):
    message: str

@app.post("/ask")
def ask(question: Question):
    response = model.generate_content(question.message)
    return {"answer": response.text}

@app.get("/sensor")
def sensor():
    return {
        "temperature": round(random.uniform(60.0, 85.0), 1),
        "pressure": round(random.uniform(1.8, 2.5), 2),
        "vibration": round(random.uniform(0.1, 0.8), 2),
        "status": "normal" if random.random() > 0.2 else "warning"
    }

@app.get("/")
def root():
    return {"message": "Welcome to the Factory HMI API"}