import streamlit as st
from groq import Groq

# Configuration de l'app
st.set_page_config(page_title="Claire", page_icon="⚡")
st.title("Claire")

# Ton API Key ici
client = Groq(api_key="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")

# Initialisation du chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des anciens messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrée utilisateur
if prompt := st.chat_input("Que faire ?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Réponse de l'IA
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages
        ).choices[0].message.content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
