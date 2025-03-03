import streamlit as st
from openai import OpenAI

st.title("Awesome Chatbot")
st.caption("Powered by INFO-5940")
print("Hello World")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])


if prompt := st.chat_input():
    client = OpenAI()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(model="openai.gpt-4o", 
                                                messages=st.session_state.messages,
                                                stream=True)
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

