# 📚 LearnSphere AI Tutor & Quiz Generator (Mistral / LLaMA 2)

An AI-powered learning assistant for **LearnSphere Academy**. Paste any lesson content and instantly get a student-friendly explanation, a 5-question quiz with answers, and a list of key concepts for revision — all running locally with no API keys.

---

## 🧠 Tech Stack

| Layer     | Technology                     |
|-----------|--------------------------------|
| LLM       | Mistral or LLaMA 2 (via Ollama)|
| Backend   | FastAPI + Uvicorn              |
| Frontend  | Streamlit                      |
| Language  | Python 3.10+                   |

---

## 📁 Project Structure

```
ai-tutor-learnsphere/
│
├── backend/
│   ├── __init__.py
│   └── main.py               # FastAPI: /generate/ with 3 educational prompts
│
├── frontend/
│   └── app.py                # Streamlit UI with tabs, model switcher, study pack download
│
├── data/
│   └── sample_lesson.txt     # Full Water Cycle lesson with 5 stages and key facts
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-tutor-learnsphere.git
cd ai-tutor-learnsphere
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama & Pull a Model

```bash
ollama pull mistral    # Default (recommended)
ollama pull llama2     # Optional alternative
```

---

## 🚀 Running the App

**Terminal 1 — Start the Backend:**

```bash
uvicorn backend.main:app --reload
```

**Terminal 2 — Start the Frontend:**

```bash
streamlit run frontend/app.py
```

Open `http://localhost:8501`. Click **Load Water Cycle Lesson** in the sidebar to test immediately.

---

## 📌 API Endpoint

| Method | Endpoint     | Description                                         |
|--------|--------------|-----------------------------------------------------|
| GET    | `/`          | Health check                                        |
| POST   | `/generate/` | Generate explanation, quiz, and concepts from text  |

### Example Response

```json
{
  "explanation": "The water cycle is nature's way of recycling water...",
  "quiz": "1. What is evaporation?\nA) Water falling from clouds ✓...",
  "concepts": "1. **Evaporation** — The process by which liquid water...",
  "model_used": "mistral",
  "word_count": 318
}
```

---

## ✅ Features

- Paste text or upload a `.txt` lesson file from the sidebar
- Model switcher — toggle between Mistral and LLaMA 2
- Tabbed output — Explanation, Quiz, and Key Concepts on separate tabs
- Per-tab download buttons + full Study Pack download
- Quiz prompt generates mixed MCQ and short-answer questions with answers
- Concepts prompt returns 8–10 numbered terms with one-sentence definitions
- Document size guard — rejects content over 40,000 characters
- Word count display
- CORS-enabled FastAPI backend with proper error handling

---

## 🛠️ Troubleshooting

| Issue | Fix |
|---|---|
| Backend not connecting | Run `uvicorn backend.main:app --reload` |
| Ollama not responding | Run `ollama serve` and check `ollama list` |
| Quiz format is inconsistent | Mistral follows the prompt well; LLaMA 2 may vary slightly |
| Analysis times out | 3 sequential LLM calls can take time — try a shorter passage |
| Sample file not loading | Ensure `data/sample_lesson.txt` is in the project folder |
