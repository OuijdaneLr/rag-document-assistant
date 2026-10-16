import chromadb
import ollama
from sentence_transformers import SentenceTransformer


# Charger le modèle multilingue utilisé lors de l'importation
modele = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")



class FonctionEmbeddings:
    def __init__(self, modele):
        self.modele = modele

    # Transformer les textes en vecteurs lors de l'importation
    def __call__(self, input):
        vecteurs = self.modele.encode(input)
        return vecteurs.tolist()

    # Transformer une question en vecteur lors de la recherche
    def embed_query(self, input):
        vecteurs = self.modele.encode(input)
        return vecteurs.tolist()

    @staticmethod
    def name():
        return "modele-multilingue"



embedding_function = FonctionEmbeddings(modele)


# Ouvrir la base de données ChromaDB
client = chromadb.PersistentClient(path="chroma_db")


# Ouvrir la collection existante avec le même modèle
collection = client.get_collection(
    name="documents",
    embedding_function=embedding_function
)


# Afficher le nombre de morceaux
print("Nombre de morceaux :", collection.count())

resultat = collection.get(
    where={"source": "document.pdf"}
)

print("Morceaux provenant du PDF :", len(resultat["ids"]))

# Rechercher les passages pertinents
def rechercher_texte(question):
    resultats = collection.query(
        query_texts=[question],
        n_results=2,
        where={"source": "document.pdf"}
    )
    return resultats

# Poser plusieurs questions
while True:
    question = input(
        "\nPose ta question sur la lettre (ou tape 'quitter') : "
    ).strip()

    if question.lower() == "quitter":
        print("Au revoir !")
        break

    if not question:
        print("Écris une question avant d'appuyer sur Entrée.")
        continue

    resultats = rechercher_texte(question)

    if not resultats["documents"] or not resultats["documents"][0]:
        print("Aucun passage pertinent trouvé.")
        continue

    # Préparer le contexte à partir des passages retrouvés
    contexte = "\n\n".join(resultats["documents"][0])

    print("\nPassages trouvés :")

    for numero, texte in enumerate(resultats["documents"][0]):
        metadonnees = resultats["metadatas"][0][numero]
        print("\nPassage :", texte)
        print("Page :", metadonnees.get("page", "Inconnue"))

    # Générer une réponse à partir du contexte
    reponse = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un assistant qui analyse des lettres de motivation. "
                    "Réponds en français uniquement à partir du contexte fourni. "
                    "N'invente aucune information. "
                    "Si l'information est absente du contexte, dis-le clairement."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Contexte de la lettre :\n{contexte}\n\n"
                    f"Question : {question}"
                )
            }
        ]
    )

    print("\nRéponse de Llama 3.2 :")
    print(reponse["message"]["content"])