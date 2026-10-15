
import chromadb
import ollama

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
#question = input("Pose ta question sur le document : ")

# Poser plusieurs questions
while True:
    question = input("\nPose ta question (ou tape 'quitter') : ")

    if question.lower().strip() == "quitter":
        print("Au revoir !")
        break

    resultats = rechercher_texte(question)

    if resultats["documents"] and resultats["documents"][0]:
        contexte = "\n\n".join(resultats["documents"][0])

        print("\nPassages trouvés :")
        for numero in range(len(resultats["documents"][0])):
            texte = resultats["documents"][0][numero]
            metadonnees = resultats["metadatas"][0][numero]

            print("\nPassage :", texte)
            print("Page :", metadonnees.get("page", "Inconnue"))

        reponse = ollama.chat(
            model="llama3.2",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es un assistant qui analyse des lettres de motivation. "
                        "Réponds en français uniquement à partir du contexte fourni. "
                        "Si l'information n'est pas présente, dis-le clairement."
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
    else:
        print("Aucun passage pertinent trouvé.")

        

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


# Générer une réponse avec Llama 3.2
if resultats["documents"] and resultats["documents"][0]:
    contexte = "\n\n".join(resultats["documents"][0])

    reponse = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un assistant qui analyse des lettres de motivation. "
                    "Réponds en français uniquement à partir du contexte fourni. "
                    "Si l'information n'est pas présente, dis-le clairement."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Contexte de la lettre de motivation :\n{contexte}\n\n"
                    f"Question : {question}"
                )
            }
        ]
    )

    print("\nRéponse de Llama 3.2 :")
    print(reponse["message"]["content"])
