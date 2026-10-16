
import streamlit as st
import chromadb
import ollama
from sentence_transformers import SentenceTransformer

# Configuration de la page
st.set_page_config(
    page_title="Mon assistant RAG",
    page_icon="📚"
)

st.title("📚 Mon assistant RAG")
st.write("Pose une question sur tes documents PDF.")

# Charger le modèle multilingue pour les recherches
@st.cache_resource
def charger_modele():
    return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

modele = charger_modele()

# Fonction pour créer les embeddings
class EmbeddingFunction:
    def __call__(self, input):
        return modele.encode(input).tolist()

    def embed_query(self, input):
        return modele.encode(input).tolist()

    def name(self):
        return "modele-multilingue"

# Connexion à la base de données ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="documents",
    embedding_function=EmbeddingFunction()
)

# Zone de saisie de la question
question = st.text_input("💬 Ta question :")

if st.button("Rechercher"):
    if question.strip():
        # Rechercher les passages les plus pertinents
        resultats = collection.query(
            query_texts=[question],
            n_results=2
        )

        passages = resultats["documents"][0]
        metadonnees = resultats["metadatas"][0]

        contexte = ""
        for passage, metadata in zip(passages, metadonnees):
            contexte += (
                f"\nSource : {metadata.get('source', 'Inconnue')}\n"
                f"Page : {metadata.get('page', '?')}\n"
                f"Passage : {passage}\n"
            )

        # Préparer les instructions pour le modèle IA
        prompt = f"""
        Tu es un assistant qui répond en français.
        Réponds uniquement à partir du contexte fourni.
        Si la réponse n'est pas dans les documents, dis-le clairement.

        Contexte :
        {contexte}

        Question : {question}

        Réponse :
        """

        with st.spinner("Je recherche la réponse..."):
            reponse = ollama.chat(
                model="llama3.2",
                messages=[{"role": "user", "content": prompt}]
            )

        st.subheader("💡 Réponse")
        st.write(reponse["message"]["content"])

        # Afficher les sources utilisées
        with st.expander("📄 Voir les passages et les sources"):
            st.text(contexte)
    else:
        st.warning("Écris une question avant de lancer la recherche.")
