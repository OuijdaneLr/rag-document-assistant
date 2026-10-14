
import chromadb

# Ouvrir la base de données
client = chromadb.PersistentClient(path="chroma_db")

# Ouvrir la collection des documents
collection = client.get_or_create_collection(
    name="documents"
)

# Afficher le nombre de morceaux
print("Nombre de morceaux :", collection.count())
resultat = collection.get(
    where={"source": "document.pdf"}
)

print("Morceaux provenant du PDF :", len(resultat["ids"]))

# Rechercher des passages dans les documents

def rechercher_texte(question):
    resultats = collection.query(
        query_texts=[question],
        n_results=2,
        where={"source": "document.pdf"}
    )

    return resultats


# Poser une question
question = "Quelles sont les informations principales du document ?"

# Effectuer la recherche
resultats = rechercher_texte(question)

# Afficher les résultats
print("\nRésultats de la recherche :")

if resultats["documents"] and resultats["documents"][0]:
    for numero in range(len(resultats["documents"][0])):
        texte = resultats["documents"][0][numero]
        metadonnees = resultats["metadatas"][0][numero]

        print("\nPassage trouvé :")
        print(texte)

        print("Page :", metadonnees.get("page", "Inconnue"))
        print("Source :", metadonnees.get("source", "Inconnue"))
else:
    print("Aucun passage trouvé.")
