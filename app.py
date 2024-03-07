import streamlit as st
import random
import time

from query_pipeline import pipeline

def response_generator(prompt: str) -> str:
    response = pipeline.run(topic=prompt)
    return response

def add_to_message_history(role: str, content: str) -> None:
    message = {"role": role, "content": str(content)}
    st.session_state.messages.append(message)  # Add response to message history


st.set_page_config(
    page_title="CoinChat: Your DeFi Smart Assistant",
    page_icon="👾",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
st.title("CoinChat: Your DeFi Smart Assistant 👾💬")

# initialise chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# print out chat history everytime app is updated
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])


# TODO: this is really hacky, only because st.rerun is jank
if prompt := st.chat_input(
    "Give me a topic",
):  # Prompt for user input and save to chat history
    # TODO: hacky
    if "has_rerun" in st.session_state.keys() and st.session_state.has_rerun:
        # if this is true, skip the user input
        st.session_state.has_rerun = False
    else:
        add_to_message_history("user", prompt)
        with st.chat_message("user"):
            st.write(prompt)

        # If last message is not from assistant, generate a new response
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = (str(response_generator(prompt)))
                    st.write(response)
                    add_to_message_history("assistant", (response))