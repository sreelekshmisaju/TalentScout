#  TalentScout - Intelligent Hiring Assistant

TalentScout is a smart, interactive hiring assistant built using **Streamlit** and powered by **Google's Gemini API**. It helps recruiters automatically screen tech candidates by generating tailored technical questions based on their profile.

##  Project Overview

TalentScout is built to:

* Greet and guide candidates through a conversational flow
* Collect candidate details (name, contact, experience, tech stack, etc.)
* Dynamically generate **beginner to advanced level technical questions** based on the candidate's tech stack
* Ask **questions one-by-one**, just like a real interviewer
* Handle conversation context and flow smoothly
* Support **skip and exit** options gracefully
* Save anonymized candidate responses for later review

---
##  Folder Structure

```
├── app.py                 # Main Streamlit app
├── prompt.py              # Prompt building logic
├── utils.py               # LLM question generation logic
├── data_handler.py        # Candidate data storage
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

---
##  Installation Instructions

### Prerequisites
- Python 3.8+
- Google Gemini API key
- Streamlit
- 
### 1. **Clone the repository**

```bash
git clone https://github.com/yourusername/talent-scout-chatbot.git
cd talent-scout-chatbot
```

### 2. **Set up a virtual environment (optional but recommended)**

```bash
python -m venv venv
source venv/Scripts/activate
source venv/Scripts/activate

source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. **Install dependencies**

```bash
pip install -r requirements.txt
```
### 4. Create .env file:

GEMINI_API_KEY= api_key_here

### 5. **Run the application**

```bash
streamlit run app.py
```



---

##  Usage Guide

1. Launch the app using the command above.
2. The chatbot will greet the candidate and present a **privacy notice**.
3. The candidate will be asked for:

   * Full name
   * Email
   * Phone number
   * Years of experience
   * Desired position
   * Current location
   * Tech stack
4. Based on the input, **technical questions** are generated dynamically using a prompt to a language model.
5. Questions are asked **one by one**, and the candidate can:

   * Answer
   * Skip
   * Exit anytime
6. After the final question, the bot gracefully **thanks the candidate** and ends the session.
7. Data is securely stored via the `data_handler.py` utility.

---


##  Technical Details

* **Frontend**: [Streamlit](https://streamlit.io/)
* **LLM Integration**: OpenAI GPT (via `prompt.py`)
* **Data Handling**: Custom local storage in `data_handler.py`
* **UI Enhancements**: Custom CSS for a modern, clean interface
* **Session Management**: Maintains chat context using `st.session_state`
* **Skip & Exit Support**: Intuitive logic for skipping questions or ending chat gracefully

---

### Key Libraries
| Library | Purpose | Version |
|---------|---------|---------|
| Streamlit | Web interface | 1.30.0 |
| Google Generative AI | Question generation | 0.4.1 |
| python-dotenv | Environment management | 1.0.0 |
| hashlib | Data anonymization | Built-in |

### Model Specifications
- Google Gemini 1.5 Flash
- 128K context window
- Optimized for conversational AI

##  Prompt Design

Prompts are structured to:

1. Collect clear user input (e.g., name, email, tech stack).
2. Construct a **customized prompt** using `prompt.py` for dynamic technical question generation:

   * Categorize questions from beginner → intermediate → advanced.
   * Focused on candidate’s specified tools, frameworks, or languages.
3. Ensure instructions like "Ask one question at a time", "Vary question complexity", and "Avoid repeating similar types" are embedded in the prompt.

---

## Demo

A live demo link : https://drive.google.com/file/d/1ZYLZ97dcfZj9NKAjM5qKUL04V3ZPlQBv/view?usp=sharing

## 🧗 Challenges & Solutions

| Challenge                               | Solution                                                                                 |
| --------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Repeated technical questions**        | Enforced uniqueness via better prompt engineering and filtering.                         |
| **Too-short or vague responses**        | Added minimum response length checks and encouraged more detailed answers.               |
| **Broken flow when skipping questions** | Built confirmation logic before skipping and managed skipped state.                      |
| **Session context loss**                | Used `st.session_state` to track the complete flow and user data.                        |
| **UI responsiveness issues**            | Applied consistent styling via injected CSS for mobile-friendliness and desktop support. |
| **Conversation State Management**        |Implemented Streamlit session state with nested dictionaries                             |                                             |
| **Inconsistent technical question difficulty**|Created tiered prompt templates with difficulty parameters                          |                                                  |
| **API failures breaking conversation**   | Added  fallback handling                                                                |


---

