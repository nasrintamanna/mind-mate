import streamlit as st
import uuid
import backend

USER_ICON = "./user.jpg"
BOT_ICON = "./ai.jpg"

# Streamlit interface setup
st.set_page_config(page_title="MindMate")

if "user_id" in st.session_state:
    user_id = st.session_state["user_id"]
else:
    user_id = str(uuid.uuid4())

if "llm_chain" not in st.session_state:
    st.session_state["llm_app"] = backend
    st.session_state["llm_chain"] = backend.openai_chain()

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "input" not in st.session_state:
    st.session_state.input = ""

def top_bar():
    col1, col2 = st.columns([10, 3])
    with col1:
        header = "Open AI powered mental healthcare chatbot"
        st.write(f"<h3 class='main-header'>{header}</h3>", unsafe_allow_html=True)
    with col2:
        clear = st.button("clear chat")

    return clear

clear = top_bar()

if clear:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.input = ""
    backend.clear_memory(st.session_state["llm_chain"])

def handle_input():
    input = st.session_state.input

    llm_chain = st.session_state["llm_chain"]
    chain = st.session_state["llm_app"]
    result, no_of_token = chain.run_chain(llm_chain, input)
    question_with_id = {
        "question": input,
        "id": len(st.session_state.questions),
        "tokens": no_of_token
    }

    st.session_state.questions.append(question_with_id)

    st.session_state.answers.append(
        {"answer": result, "id": len(st.session_state.questions)}
    )
    st.session_state.input = ""

def user_message(md):
    col1, col2 = st.columns([1, 12])
    with col1:
        st.image(USER_ICON, use_column_width="always")
    with col2:
        st.warning(md["question"])
        st.write(f"Number of Tokens used: {md['tokens']}")

def render_answer(answer):
    col1, col2 = st.columns([1, 12])
    with col1:
        st.image(BOT_ICON, use_column_width="always")
    with col2:
        st.info(answer["response"])

def write_chat_message(md):
    chat = st.container()
    with chat:
        render_answer(md["answer"])

with st.container():
    for q, a in zip(st.session_state.questions, st.session_state.answers):
        user_message(q)
        write_chat_message(a)

st.markdown("---")
imput = st.text_input(
    "How are you today?", key="input", on_change=handle_input
)