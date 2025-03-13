import streamlit as st
from openai import AzureOpenAI
from openai import OpenAI
from os import environ
import tiktoken

st.title("Chatbot")
st.caption("Powered by INFO-5940")

def count_tokens(messages):
    encoding = tiktoken.encoding_for_model("gpt-4")
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you today?"}]
if "total_tokens" not in st.session_state:
    st.session_state["total_tokens"] = 0

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    input_tokens = count_tokens(st.session_state.messages)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

    output_tokens = count_tokens([{"role": "assistant", "content": response}])

    # Update total tokens
    st.session_state.total_tokens += input_tokens + output_tokens

    # Display token count for this interaction
    st.sidebar.write(f"Tokens used in this interaction:")
    st.sidebar.write(f"Input: {input_tokens}")
    st.sidebar.write(f"Output: {output_tokens}")
    st.sidebar.write(f"Total: {input_tokens + output_tokens}")

    # Display total tokens used in all interactions
    st.sidebar.write(f"Total tokens used: {st.session_state.total_tokens}")

