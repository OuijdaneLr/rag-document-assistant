import pymupdf
import chromadb
from sentence_transformers import SentenceTransformer


# Charger le modèle multilingue pour transformer les textes en vecteurs numériques
modele = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")


# Définir la fonction qui transforme les textes en vecteurs
class FonctionEmbeddings:
    def __init__(self, modele):
        self.modele = modele

    def __call__(self, input):
        vecteurs = self.modele.encode(input)
        return vecteurs.tolist()

    @staticmethod
    def name():
        return "modele-multilingue"


embedding_function = FonctionEmbeddings(modele)


# Ouvrir le fichier PDF
document = pymupdf.open("data/document.pdf")

# Créer une liste pour stocker les pages
pages = []

# Lire chaque page du PDF
for numero, page in enumerate(document, start=1):
    texte = page.get_text()

    # Garder le numéro de page et le texte
    pages.append({
        "page": numero,
        "text": texte
    })

# Fermer le PDF
document.close()

print("Nombre de pages extraites :", len(pages))


# Découper un texte en petits morceaux
def decouper_texte(texte, taille=500):
    morceaux = []

    debut = 0

    while debut < len(texte):
        morceau = texte[debut:debut + taille]
        morceaux.append(morceau)
        debut += taille

    return morceaux


print("Fonction de découpage prête !")


# Créer une liste pour tous les morceaux
tous_les_morceaux = []

# Parcourir toutes les pages
for page in pages:
    morceaux_page = decouper_texte(page["text"])

    # Garder chaque morceau avec son numéro de page
    for morceau in morceaux_page:
        tous_les_morceaux.append({
            "page": page["page"],
            "text": morceau
        })

print("Nombre total de morceaux :", len(tous_les_morceaux))


# Préparer les textes et leurs métadonnées
textes = []
metadonnees = []
identifiants = []

for numero, morceau in enumerate(tous_les_morceaux):
    textes.append(morceau["text"])

    metadonnees.append({
        "page": morceau["page"],
        "source": "document.pdf"
    })

    identifiants.append("pdf_morceau_" + str(numero))


# Ouvrir la base de données ChromaDB
client = chromadb.PersistentClient(path="chroma_db")


# Supprimer l'ancienne collection si elle existe
collections_existantes = [
    collection.name for collection in client.list_collections()
]

if "documents" in collections_existantes:
    client.delete_collection(name="documents")
    print("Ancienne collection supprimée.")


# Créer la collection avec le modèle d'embeddings multilingue
collection = client.create_collection(
    name="documents",
    embedding_function=embedding_function
)

print("Collection créée avec le modèle multilingue !")


# Enregistrer les morceaux dans ChromaDB
if textes:
    collection.add(
        ids=identifiants,
        documents=textes,
        metadatas=metadonnees
    )

    print("Le PDF a été enregistré dans ChromaDB !")
    print("Nombre de morceaux dans ChromaDB :", collection.count())
else:
    print("Aucun texte trouvé dans le PDF.")