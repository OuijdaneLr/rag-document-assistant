import os
import glob
import chromadb
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF


# Charger le modèle multilingue
modele = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


# Définir la fonction d'embeddings pour ChromaDB
class FonctionEmbeddings:
    def __init__(self, modele):
        self.modele = modele

    def __call__(self, input):
        vecteurs = self.modele.encode(input)
        return vecteurs.tolist()

    def embed_query(self, input):
        vecteurs = self.modele.encode(input)
        return vecteurs.tolist()

    @staticmethod
    def name():
        return "modele-multilingue"


embedding_function = FonctionEmbeddings(modele)


# Ouvrir la base de données ChromaDB
client = chromadb.PersistentClient(path="chroma_db")


# Recréer la collection pour éviter de conserver d'anciennes données
collections_existantes = [
    collection.name for collection in client.list_collections()
]

if "documents" in collections_existantes:
    client.delete_collection(name="documents")
    print("Ancienne collection supprimée.")

collection = client.create_collection(
    name="documents",
    embedding_function=embedding_function
)


# Trouver tous les PDF du dossier data
fichiers_pdf = glob.glob(os.path.join("data", "*.pdf"))

if not fichiers_pdf:
    print("Aucun fichier PDF trouvé dans le dossier data.")

# Importer chaque PDF
for chemin_pdf in fichiers_pdf:
    nom_pdf = os.path.basename(chemin_pdf)
    print(f"\nImportation de : {nom_pdf}")

    document = fitz.open(chemin_pdf)

    textes = []
    identifiants = []
    metadonnees = []

    # Lire chaque page du PDF
    for numero_page, page in enumerate(document):
        texte = page.get_text()

        # Ignorer les pages sans texte
        if not texte.strip():
            continue

        # Découper le texte en morceaux de 500 caractères
        taille_morceau = 500

        for debut in range(0, len(texte), taille_morceau):
            morceau = texte[debut:debut + taille_morceau]

            identifiants.append(
                f"{nom_pdf}_page{numero_page + 1}_morceau{len(identifiants) + 1}"
            )
            textes.append(morceau)
            metadonnees.append({
                "source": nom_pdf,
                "page": numero_page + 1
            })

    document.close()

    # Ajouter les morceaux du PDF à ChromaDB
    if textes:
        collection.add(
            ids=identifiants,
            documents=textes,
            metadatas=metadonnees
        )
        print(f"{len(textes)} morceaux importés depuis {nom_pdf}.")
    else:
        print(f"Aucun texte exploitable trouvé dans {nom_pdf}.")


print("\nImportation terminée !")
print("Nombre total de morceaux :", collection.count())
