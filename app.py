import streamlit as st
from supabase import create_client
from groq import Groq

# 1. Configuration des clients (via Streamlit Secrets)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 2. Fonctions Supabase pour la mémoire
def load_chat_history():
    # Charge les 20 derniers messages
    response = supabase.table("chat_history").select("*").order("id", desc=False).limit(20).execute()
    return response.data

def save_message(user_msg, ai_msg):
    data = {"user_message": user_msg, "ai_response": ai_msg}
    supabase.table("chat_history").insert(data).execute()

# 3. Initialisation de l'application
st.title("Claire")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Chargement unique de l'historique au démarrage
if "history_loaded" not in st.session_state:
    history = load_chat_history()
    for row in history:
        st.session_state.messages.append({"role": "user", "content": row["user_message"]})
        st.session_state.messages.append({"role": "assistant", "content": row["ai_response"]})
    st.session_state.history_loaded = True

# 5. Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Logique de chat et appel API
if prompt := st.chat_input("Dis quelque chose à Claire..."):
    # Afficher le message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Appel Groq (Llama 3.1)
    chat_completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-70b-versatile",
    )
    ai_response = chat_completion.choices[0].message.content
    
    # Afficher la réponse de Claire
    with st.chat_message("assistant"):
        st.markdown(ai_response)
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    
    # Sauvegarder dans Supabase
    save_message(prompt, ai_response)
