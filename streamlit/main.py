import streamlit as st
import requests


st.title("💬 Fencing Assistant")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    fencingpt_url = "http://127.0.0.1:8000/ask"
    payload = {
        "question": prompt
    }

    # api will return:
    # return {
    #     "question": user_question,
    #     "context": context,
    #     "answer": answer
    # }
    try:
        response = requests.post(fencingpt_url, json=payload)
        response.raise_for_status()
        msg = response.json()["answer"]
    except Exception as e:
        msg = "Sorry, something went wrong."

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)