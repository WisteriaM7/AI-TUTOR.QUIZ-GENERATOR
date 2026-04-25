from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI(title="LearnSphere AI Tutor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral"

PROMPTS = {
    "explanation": (
        "You are a friendly and patient teacher explaining a topic to a student aged 14–16. "
        "Rewrite the following educational content in simple, clear, engaging language. "
        "Use short sentences, everyday examples, and analogies where helpful. "
        "Avoid jargon unless you explain it first. Aim for 150–200 words.\n\n"
        "Content:\n{text}"
    ),
    "quiz": (
        "You are an experienced educator creating an assessment. "
        "Based on the following educational content, generate exactly 5 quiz questions. "
        "Mix question types: include at least 2 multiple-choice questions (with 4 options each, "
        "mark the correct answer with ✓) and at least 2 short-answer questions. "
        "Format each question clearly with a number, the question, options (if MCQ), "
        "and the correct answer on a new line starting with 'Answer:'.\n\n"
        "Content:\n{text}"
    ),
    "concepts": (
        "You are a curriculum designer identifying key learning objectives. "
        "From the following educational content, extract 8–10 key terms or concepts "
        "that a student must understand to master this topic. "
        "For each concept, provide: the term in bold, followed by a one-sentence definition. "
        "Format as a numbered list.\n\n"
        "Content:\n{text}"
    ),
}


def query_model(prompt: str, model: str = DEFAULT_MODEL, timeout: int = 120) -> str:
    """Send prompt to the local Ollama model."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=timeout
        )
        return response.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Could not connect to Ollama. Make sure it is running on port 11434."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")


@app.get("/")
def root():
    return {"message": "LearnSphere AI Tutor API is running!", "model": DEFAULT_MODEL}


@app.post("/generate/")
def generate_learning_aids(text: str = Form(...), model: str = Form(default=DEFAULT_MODEL)):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Lesson content cannot be empty.")

    if len(text) > 40000:
        raise HTTPException(
            status_code=413,
            detail="Content too large. Please limit to 40,000 characters."
        )

    results = {}
    for key, prompt_template in PROMPTS.items():
        prompt = prompt_template.format(text=text)
        results[key] = query_model(prompt, model=model)

    return {
        "explanation": results["explanation"],
        "quiz": results["quiz"],
        "concepts": results["concepts"],
        "model_used": model,
        "word_count": len(text.split()),
    }
