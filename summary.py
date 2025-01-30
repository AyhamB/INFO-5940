import streamlit as st
from openai import OpenAI
from os import environ
import tiktoken

# Set the title and caption of the Streamlit app
st.title("Chatbot with Conversation Summary")
st.caption("Powered by INFO-5940")

# Function to count the number of tokens in a list of messages
def count_tokens(messages):
    encoding = tiktoken.encoding_for_model("gpt-4")
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # Base tokens for each message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))  # Tokens for the content
            if key == "name":
                num_tokens += -1  # Adjust for the 'name' key
    num_tokens += 2  # Additional tokens
    return num_tokens

# Function to summarize a conversation using OpenAI's API
def summarize_conversation(messages):
    client = OpenAI(api_key=environ['OPENAI_API_KEY'])
    summary_prompt = "Summarize the following conversation concisely:"
    for msg in messages:
        summary_prompt += f"\n{msg['role']}: {msg['content']}"
    summary_prompt += "\nSummary:"

    response = client.chat.completions.create(
        model="openai.gpt-4o-mini",
        messages=[{"role": "user", "content": summary_prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! How can I help you today?"}]
if "total_tokens" not in st.session_state:
    st.session_state["total_tokens"] = 0
if "summary" not in st.session_state:
    st.session_state["summary"] = ""

# Display the chat messages
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Handle user input
if prompt := st.chat_input():
    client = OpenAI(api_key=environ['OPENAI_API_KEY'])

    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Summarize conversation every 3 messages
    if len(st.session_state.messages) % 3 == 0:
        st.session_state["summary"] = summarize_conversation(st.session_state.messages)
        st.session_state.messages = [
            {"role": "system", "content": f"Previous conversation summary: {st.session_state['summary']}"},
            {"role": "user", "content": prompt}
        ]

    # Display the current summary in the sidebar
    if st.session_state["summary"]:
        st.sidebar.write("Current Conversation Summary:")
        st.sidebar.write(st.session_state["summary"])

    # Count input tokens
    input_tokens = count_tokens(st.session_state.messages)

    # Generate assistant response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="openai.gpt-4o",
            messages=st.session_state.messages,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Count output tokens
    output_tokens = count_tokens([{"role": "assistant", "content": response}])

    # Update total tokens used
    st.session_state.total_tokens += input_tokens + output_tokens

    # Display token usage in the sidebar
    st.sidebar.write(f"Tokens used in this interaction:")
    st.sidebar.write(f"Input: {input_tokens}")
    st.sidebar.write(f"Output: {output_tokens}")
    st.sidebar.write(f"Total: {input_tokens + output_tokens}")
    st.sidebar.write(f"Total tokens used: {st.session_state.total_tokens}")