import streamlit as st
import phoenix as px
import logging
from llama_index.core import PromptTemplate, set_global_handler

from query_pipeline import pipeline
from prompts import summary_tmpl_with_mem_str

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

px.launch_app()
set_global_handler('arize_phoenix')

def response_generator(prompt: str, update_tmpl: PromptTemplate=None) -> str:
    if update_tmpl:
        pipeline.dict()['module_dict']['synthesizer']['synthesizer'].update_prompts(
            {'summary_template': update_tmpl}
        )
    response = pipeline.run(topic=prompt)
    return response

def add_to_message_history(role: str, content: str) -> None:
    message = {"role": role, "content": str(content)}
    st.session_state.messages.append(message)  # Add response to message history

def generate_memory_str_from_messages(session_state: st.session_state) -> str:
    question = session_state.messages[-1]['content']
    answer = session_state.messages[-2]['content']
    return f'User\'s previous question: {question}\nYour previous answer: {answer}'


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
                    # update prompt with the last assistant message for context
                    if len(st.session_state.messages) >= 3: # can only update with context if there is atleast 1 Q and 1 A in the message history
                        prompt_with_mem_tmpl = PromptTemplate(summary_tmpl_with_mem_str.format(
                            memory_str=generate_memory_str_from_messages(st.session_state),
                            )
                        )
                        response = (str(response_generator(prompt, update_tmpl=prompt_with_mem_tmpl)))
                    else:
                        response = (str(response_generator(prompt)))
                    st.write(response)
                    add_to_message_history("assistant", (response))