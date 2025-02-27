import streamlit as st
from openai import OpenAI
from os import environ

st.title("RAG Chatbot")
st.caption("Powered by INFO-5940")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you today?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # use gpt-mini to parse if the prompt is about a question about cornell, harvard or duke. 
    response = client.chat.completions.create(model="openai.gpt-4o-mini", 
                                              messages=[
            {
                "role": "system",
                "content": """Your job is to guess which knowledge base I need to load based on the user 
                prompt. The available knowledge bases are:
                harvard.txt, cornell.txt, duke.txt if these are not related to the prompt please 
                output none.txt.
                I want you output to only be the name of the file. and nothing else.""",
            },
            {
                "role": "user",
                "content": prompt
            }
        ])
    print(response.choices[0].message.content)
    # load the file based on the response
    if response.choices[0].message.content in ["harvard.txt", "cornell.txt", "duke.txt"]:
        knowledge_base_file_path = "/workspace/data/knowledge_base"
        with open(f"{knowledge_base_file_path}/{response.choices[0].message.content}", "r") as file:
            content = file.read()

        print(content)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model="openai.gpt-4o",  # Change this to a valid model name
                messages=[
                    {"role": "system", "content": f"Here's the content of the file:\n\n{content}"},
                    *st.session_state.messages
                ],
                stream=True
            )
            response = st.write_stream(stream)
    
    else:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(model="openai.gpt-4o", 
                                                    messages=st.session_state.messages,
                                                    stream=True)
            response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

