import streamlit as st
from supabase import create_client

# Configuration Supabase (assure-toi que tes secrets sont dans Streamlit)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- NOUVEAU : Fonction pour charger l'historique ---
def load_chat_history():
    # On récupère les messages dans l'ordre chronologique
    response = supabase.table("chat_history").select("*").order("id", desc=False).execute()
    return response.data

# --- Fonction pour sauvegarder ---
def save_message(user_msg, ai_msg):
    data = {"user_message": user_msg, "ai_response": ai_msg}
    supabase.table("chat_history").insert(data).execute()

st.title("Claire")

# Initialisation de la session
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- NOUVEAU : Chargement de la mémoire au démarrage ---
if "history_loaded" not in st.session_state:
    history = load_chat_history()
    for row in history:
        st.session_state.messages.append({"role": "user", "content": row["user_message"]})
        st.session_state.messages.append({"role": "assistant", "content": row["ai_response"]})
    st.session_state.history_loaded = True

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de chat
if prompt := st.chat_input("Dis quelque chose à Claire..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Ici, tu mets ton appel à l'API Groq (Llama 3.1)
    # Exemple simplifié :
    ai_response = "Ceci est une réponse test de Claire." 
    
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Sauvegarde dans Supabase
    save_message(prompt, ai_response)
