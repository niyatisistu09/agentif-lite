
import streamlit as st

st.set_page_config(
    page_title="AgentIF-Lite",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AgentIF-Lite")
st.subheader("AI Instruction Compliance Evaluator")

st.write(
    "Enter a task and an AI response to check "
    "whether the response follows the instructions."
)

instructions = st.text_area(
    "Task instructions",
    placeholder="Example: Write exactly 3 bullet points."
)

response = st.text_area(
    "AI response",
    placeholder="Paste the response you want to evaluate."
)

if st.button("Evaluate Response"):
    if not instructions.strip() or not response.strip():
        st.warning("Please enter both instructions and a response.")
    else:
        st.info("Your evaluator is ready for the next implementation step!")
        st.write("**Instructions:**", instructions)
        st.write("**Response:**", response)
