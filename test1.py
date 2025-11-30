# ===================================
# CHATBOT GEMINI AVEC STREAMLIT
# Version simple et complète
# ===================================

"""
Installation :
    pip install streamlit google-generativeai python-dotenv

Lancer :
    streamlit run app.py

Créer un fichier .env :
    GEMINI_API_KEY=votre_clé_ici
"""

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Configuration de la page
st.set_page_config(
    page_title="Recommendation Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Charger la clé API
load_dotenv("test.env")
api_key = os.getenv('GEMINI_API_KEY')

# Vérifier la clé API
if not api_key:
    st.error("❌ Clé API non trouvée ! Ajoutez GEMINI_API_KEY dans votre fichier .env")
    st.stop()

# Configurer Gemini
genai.configure(api_key=api_key)

# ===================================
# INTERFACE UTILISATEUR
# ===================================

# Titre
st.title("🤖 Recommendation Chatbot")
st.markdown("Cherchez votre MEILLEUR artisan !")
st.markdown("*Donnez des questions, le chatbot est ici pour te repondre.*")

# ===================================
# SIDEBAR (Barre latérale)
# ===================================

with st.sidebar:
    st.header("⚙️ Paramètres")
    
    # Température
    temperature = st.slider(
        "Créativité",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="0.0 = Précis | 1.0 = Créatif"
    )
    
    # Max tokens
    max_tokens = st.number_input(
        "Longueur max",
        min_value=100,
        max_value=2000,
        value=1000,
        step=100,
        help="Nombre maximum de mots dans la réponse"
    )
    
    
    st.divider()
    
    # Statistiques
    st.markdown("### 📊 Statistiques")
    if 'messages' in st.session_state:
        nb_messages = len(st.session_state.messages) // 2
        st.metric("Messages envoyés", nb_messages)
    
    st.divider()
    
    # Bouton pour effacer
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        if 'chat' in st.session_state:
            del st.session_state.chat
        st.rerun()

# ===================================
# INITIALISATION
# ===================================

# Initialiser le modèle
if 'model' not in st.session_state:
    st.session_state.model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config={
            'temperature': temperature,
            'max_output_tokens': max_tokens
        }
    )
    st.session_state.chat = st.session_state.model.start_chat(history=[])

# Initialiser l'historique des messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ===================================
# AFFICHAGE DE L'HISTORIQUE
# ===================================

# Afficher tous les messages précédents
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ===================================
# INPUT UTILISATEUR ET RÉPONSE
# ===================================

# Zone de saisie du chat
if prompt := st.chat_input("Posez votre question..."):
    
    # Ajouter et afficher le message utilisateur
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Générer et afficher la réponse
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # Envoyer le message à Gemini
            response = st.session_state.chat.send_message(prompt)
            full_response = response.text
            
            # Afficher la réponse
            message_placeholder.markdown(full_response)
            
            # Ajouter la réponse à l'historique
            st.session_state.messages.append({
                "role": "assistant",
                "content": full_response
            })
        
        except Exception as e:
            error_message = f"❌ Erreur : {str(e)}"
            message_placeholder.error(error_message)
            
            # Messages d'erreur spécifiques
            if "quota" in str(e).lower():
                st.warning("⚠️ Limite d'API atteinte. Attendez un peu.")
            elif "invalid" in str(e).lower():
                st.error("🔑 Clé API invalide. Vérifiez votre .env")

# ===================================
# FOOTER
# ===================================

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
        Créé avec ❤️ | Propulsé par Gemini API
    </div>
    """,
    unsafe_allow_html=True
)


