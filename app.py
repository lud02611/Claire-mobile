import streamlit as st
from supabase import create_client
from groq import Groq

# 1. Configuration des connexions
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_KEY"]
supabase = create_client(supabase_url, supabase_key)

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.title("Claire")

# 2. Fonction pour sauvegarder dans Supabase
def save_message(user_msg, ai_msg):
    data = {"user_message": user_msg, "ai_response": ai_msg}
    supabase.table("chat_history").insert(data).execute()

# 3. Initialisation de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Affichage des messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Gestion de la saisie utilisateur et réponse de Groq
if prompt := st.chat_input("Dis quelque chose à Claire..."):
    # Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Appeler l'API Groq
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    ai_response = chat_completion.choices[0].message.content

    # SAUVEGARDER DANS LA BASE DE DONNÉES
    save_message(prompt, ai_response)

    # Afficher la réponse de l'IA
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
