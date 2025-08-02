import streamlit as st
import time
import random
from utils import get_technical_questions
from prompt import build_candidate_prompt
from data_handler import store_candidate_data
from utils import is_unexpected_input, get_fallback_response


# ----------------- Custom CSS Styling -----------------
def load_css():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(-45deg, #e6f2ff, #f0e6ff, #ffe6f2, #e6ffe6);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            padding: 20px;
            font-family: 'Segoe UI', sans-serif;
        }

        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        .stChatMessage {
            color: #000000 !important;
            font-weight: bold;
        }

        [data-testid="stChatMessage"][aria-label="You"] {
            background-color: #ffffff;
            color: #000;
            margin-left: 20%;
            border: 2px solid #4a90e2;
            border-radius: 20px 20px 0 20px;
            padding: 15px;
            box-shadow: 0 10px 15px rgba(74, 144, 226, 0.2);
            font-weight: bold;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        [data-testid="stChatMessage"][aria-label="You"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 20px rgba(74, 144, 226, 0.3);
        }

        [data-testid="stChatMessage"][aria-label="TalentScout"] {
            background-color: #ffffff;
            color: #000;
            margin-right: 20%;
            border: 2px solid #9c64ff;
            border-radius: 20px 20px 20px 0;
            padding: 15px;
            box-shadow: 0 10px 15px rgba(156, 100, 255, 0.2);
            font-weight: bold;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        [data-testid="stChatMessage"][aria-label="TalentScout"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 15px 20px rgba(156, 100, 255, 0.3);
        }

        .stMarkdown {
            color: #000000 !important;
            font-weight: bold;
        }

        .stChatInput {
            position: fixed;
            bottom: 20px;
            width: 80%;
            max-width: 800px;
            background: white;
            color: #000000;
            padding: 14px;
            border-radius: 14px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            border: 2px solid #4a90e2;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        .stChatInput:focus-within {
            border-color: #9c64ff;
            box-shadow: 0 10px 30px rgba(156, 100, 255, 0.4);
        }

        .typing {
            display: inline-block;
            padding-left: 5px;
        }
        .typing span {
            height: 10px;
            width: 10px;
            background: #9c64ff;
            border-radius: 50%;
            display: inline-block;
            margin-right: 4px;
            animation: typing 1.2s infinite ease-in-out;
        }

        @keyframes typing {
            0% { transform: translateY(0); opacity: 0.5; }
            50% { transform: translateY(-5px); opacity: 1; }
            100% { transform: translateY(0); opacity: 0.5; }
        }

        .quick-reply {
            display: inline-block;
            margin: 6px 8px;
            padding: 10px 20px;
            background-color: #fff;
            color: #000;
            border: 2px solid #9c64ff;
            border-radius: 25px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.25s ease;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        }

        .quick-reply:hover {
            background-color: #9c64ff;
            color: white;
            transform: translateY(-2px) scale(1.03);
            box-shadow: 0 6px 14px rgba(156, 100, 255, 0.3);
        }

        h1, h2, h3 {
            color: #2e1065;
            font-weight: bold;
            text-shadow: 1px 1px 0 #ddd, 2px 2px 0 #ccc;
            transform: rotate(-1deg);
            transition: transform 0.3s ease;
        }

        h1:hover, h2:hover, h3:hover {
            transform: rotate(0) scale(1.05);
        }

        .floating {
            animation: floating 3s ease-in-out infinite;
        }

        @keyframes floating {
            0% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
            100% { transform: translateY(0); }
        }
    </style>
    """, unsafe_allow_html=True)



# ----------------- Helper Functions -----------------
def typing_indicator():
    """Show typing animation"""
    with st.empty():
        st.markdown('<div class="typing"><span></span><span></span><span></span></div>', unsafe_allow_html=True)
        time.sleep(0.5)

def chat_output(role, message, quick_replies=None):
    """Enhanced chat output with quick reply options"""
    st.chat_message(role).markdown(message)
    st.session_state.chat_history.append({"role": role, "message": message})
    
    if quick_replies and role == "assistant":
        cols = st.columns([1]*len(quick_replies))
        for i, reply in enumerate(quick_replies):
            if cols[i].button(reply, key=f"quick_reply_{i}_{time.time()}"):  # Added timestamp to avoid duplicate key errors
                st.session_state.last_quick_reply = reply
                st.rerun()

def simulate_typing(role, message, delay=0.5):
    """Simulate typing effect for messages"""
    typing_indicator()
    time.sleep(delay)
    chat_output(role, message)

def show_quick_replies(replies):
    """Display quick reply buttons after a message"""
    cols = st.columns([1]*len(replies))
    for i, reply in enumerate(replies):
        if cols[i].button(reply, key=f"quick_reply_{i}_{time.time()}"):  # Added timestamp to avoid duplicate key errors
            st.session_state.last_quick_reply = reply
            st.rerun()

def end_interview():
    """Handle interview completion logic"""

    # Store anonymized candidate data
    responses = [entry for entry in st.session_state.chat_history if entry["role"] == "user"]
    store_candidate_data(st.session_state.data, responses)

    if st.session_state.skipped_questions:
        simulate_typing("assistant", f"📝 Note: {len(st.session_state.skipped_questions)} questions were skipped")

    simulate_typing("assistant", 
        "🙏💙 **Thank you  for taking the time to speak with us today.**\n\n"
        "It's been a pleasure learning more about your background and experience."
    )

    simulate_typing("assistant",
        "🤝 **That concludes our discussion.**\n\n"
        "Our team will now review your responses and be in touch shortly with next steps.\n\n"
        "We appreciate your interest in the opportunity and wish you the very best.\n"
        "Have a great day!"
    )
    st.session_state.chat_active = False


def show_next_question():
    """Display the next question with consistent numbering"""
    next_q = st.session_state.selected_questions[st.session_state.actual_question_idx]
    simulate_typing("assistant", f"**Question {st.session_state.current_question_num}:**\n\n{next_q}")

# ----------------- UI Setup -----------------
load_css()
st.set_page_config(
    page_title="TalentScout - Intelligent Hiring Assistant", 
    layout="centered",
    page_icon="💬"
)

# ----------------- Initialize State -----------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.chat_history = []
    st.session_state.chat_active = True
    st.session_state.all_questions = []
    st.session_state.selected_questions = []
    st.session_state.current_question_num = 0
    st.session_state.actual_question_idx = 0
    st.session_state.skipped_questions = []
    st.session_state.waiting_for_confirmation = False
    st.session_state.last_quick_reply = None

exit_keywords = ["exit", "quit", "bye", "stop", "end"]
skip_keywords = ["skip", "don't know", "not sure", "pass"]

# ----------------- Chat History Display -----------------
if st.session_state.chat_history:
    for entry in st.session_state.chat_history:
        st.chat_message(entry["role"]).markdown(entry["message"])

# ----------------- Initial Greeting -----------------
if st.session_state.step == 0:
    simulate_typing("assistant", 
        "ᯓ★𝙝𝙚𝙡𝙡𝙤｡𖦹°‧👋 **Hi! I'm TalentScout – your intelligent hiring assistant.**\n\n"
        "Thank you for taking the time to speak with us today. It's been a pleasure learning more about your background and experience.\n\n"
        "I'll help gather your candidate information and conduct a technical interview.\n\n"
        "You can type 'exit', 'quit', or 'bye' to end the chat anytime.\n\n"
        "Let's begin — What's your **full name**?"
    )
    show_quick_replies(["Ready to begin!", "I have questions first"])
    st.session_state.step = 1

# ----------------- Handle Quick Replies -----------------
if hasattr(st.session_state, 'last_quick_reply') and st.session_state.last_quick_reply:
    user_input = st.session_state.last_quick_reply
    st.session_state.last_quick_reply = None
else:
    user_input = st.chat_input(" ⌨👩🏻‍💻 Type your response...")

# ----------------- Chat Input Processing -----------------
if st.session_state.chat_active and user_input:
    # Check for exit keywords
    if any(word in user_input.lower() for word in exit_keywords):
        chat_output("user", user_input)
        simulate_typing("🧑🏻‍💼assistant", "☑ That concludes our discussion. Our team will now review your responses and be in touch shortly with the next steps. We appreciate your interest in the opportunity and wish you the very best. Have a great day!")
        st.session_state.chat_active = False
        st.stop()

    # Handle skip confirmation
    elif st.session_state.waiting_for_confirmation:
        if user_input.lower().strip() in ["yes", "y", "confirm"]:
            skipped_q = st.session_state.selected_questions[st.session_state.actual_question_idx]
            st.session_state.skipped_questions.append({
                "number": st.session_state.current_question_num,
                "question": skipped_q
            })
            chat_output("user", user_input)
            simulate_typing("🧑🏻‍💼assistant", "╰┈➤⏭ Moving to next question...")
            
            st.session_state.actual_question_idx += 1
            st.session_state.current_question_num += 1
            st.session_state.waiting_for_confirmation = False
            
            if st.session_state.current_question_num <= 5:
                show_next_question()
            else:
                end_interview()
        else:
            chat_output("user", user_input)
            current_q = st.session_state.selected_questions[st.session_state.actual_question_idx]
            simulate_typing("🧑🏻‍💼assistant", f"**Question {st.session_state.current_question_num}:**\n\n{current_q}")
            st.session_state.waiting_for_confirmation = False

    # Skip request logic
    elif st.session_state.step == 8 and any(word in user_input.lower() for word in skip_keywords):
        chat_output("user", user_input)
        simulate_typing("🧑🏻‍💼 assistant", "⃠⇄ ◀ 𓊕 ▶ ↻ Are you sure you want to skip this question?")
        show_quick_replies(["Yes, skip", "No, continue"])
        st.session_state.waiting_for_confirmation = True

    # Normal conversation flow (steps 1-7)
    elif st.session_state.step == 1:
        st.session_state.data["name"] = user_input
        chat_output("user", user_input)
        simulate_typing("🧑🏻‍💼assistant", "Thanks! What's your **email address**?")
        st.session_state.step = 2

    elif st.session_state.step == 2:
        st.session_state.data["email"] = user_input
        chat_output("user", user_input)
        simulate_typing("🧑🏻‍💼assistant", "Great. Please share your **phone number**.")
        st.session_state.step = 3

    elif st.session_state.step == 3:
        st.session_state.data["phone"] = user_input
        chat_output("user", user_input)
        simulate_typing("🧑🏻‍💼assistant", "How many **years of experience** do you have?")
        show_quick_replies(["0-2 years", "3-5 years", "5+ years"])
        st.session_state.step = 4

    elif st.session_state.step == 4:
        st.session_state.data["experience"] = user_input
        chat_output("user", user_input)
        simulate_typing("🧑🏻‍💼assistant", "What **position(s)** are you applying for?")
        st.session_state.step = 5

    elif st.session_state.step == 5:
        st.session_state.data["position"] = user_input
        chat_output("user", user_input)
        simulate_typing("🧑🏻‍💼assistant", "Where are you **currently located**?")
        st.session_state.step = 6

    elif st.session_state.step == 6:
        st.session_state.data["location"] = user_input
        chat_output("user", user_input)
        simulate_typing("🧑🏻‍💼assistant", "What is your **tech stack**? (e.g., Python, React, MySQL)")
        st.session_state.step = 7

    elif st.session_state.step == 7:
        st.session_state.data["tech_stack"] = user_input
        chat_output("user", user_input)

        with st.spinner("𝙻𝚘𝚊𝚍𝚒𝚗𝚐֎ Generating technical questions based on your tech stack..."):
            prompt = build_candidate_prompt(st.session_state.data)
            questions = get_technical_questions(prompt)
            st.session_state.all_questions = [q for q in questions.split("\n") if q.strip()]
            st.session_state.selected_questions = st.session_state.all_questions[:10]
        
        simulate_typing("assistant", "🔍😊 **Technical Interview Starting**\n\nI'll ask you questions one by one. Take your time!")
        st.session_state.step = 8
        st.session_state.current_question_num = 1
        st.session_state.actual_question_idx = 0
        show_next_question()

    elif st.session_state.step == 8 and not st.session_state.waiting_for_confirmation:
        chat_output("user", user_input)
        
        if is_unexpected_input(user_input):
            context = f"Technical interview for a {st.session_state.data.get('position', 'software')} role. Candidate tech stack: {st.session_state.data.get('tech_stack', '')}."
            fallback = get_fallback_response(user_input, context)
            
            if fallback:
                simulate_typing("assistant", f"↩️ {fallback}")
            else:
                simulate_typing("assistant", "Sorry, I didn't quite understand that. Could you try rephrasing?")
            
            current_q = st.session_state.selected_questions[st.session_state.actual_question_idx]
            simulate_typing("assistant", f"**Question {st.session_state.current_question_num}:**\n\n{current_q}")
            st.stop()
            
        st.session_state.current_question_num += 1
        st.session_state.actual_question_idx += 1

        if st.session_state.current_question_num <= 5:
            show_next_question()
        else:
            end_interview()
            
    elif st.session_state.step == 9:
        st.success("✰ ✰ ✰ Interview completed. Thank you!")  
    
        
  
