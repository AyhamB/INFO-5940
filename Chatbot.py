import streamlit as st
from openai import OpenAI

st.title("Chatbot")
st.caption("Powered by INFO-5940")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])


if prompt := st.chat_input():

    client = OpenAI()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.chat.completions.create(model="openai.gpt-4o", messages=st.session_state.messages)

    msg = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": msg})

    st.chat_message("assistant").write(msg)

