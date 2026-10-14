import pymupdf
import chromadb


import pymupdf
import chromadb

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

# Afficher le résultat
print("Nombre de pages extraites :", len(pages))


# Découper un texte en petits morceaux
def decouper_texte(texte, taille=500):
    morceaux = []

    debut = 0

    while debut < len(texte):
        morceau = texte[debut:debut + taille]
        morceaux.append(morceau)
        debut = debut + taille

    return morceaux


print("Fonction de découpage prête !")

# Découper le texte de la première page
if pages:
    morceaux = decouper_texte(pages[0]["text"])

    print("Nombre de morceaux de la première page :", len(morceaux))

    
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

# Afficher le nombre total de morceaux
print("Nombre total de morceaux :", len(tous_les_morceaux))


# Ouvrir la base de données ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

# Créer la collection des documents
collection = client.get_or_create_collection(
    name="documents"
)

print("Connexion à ChromaDB réussie !")


# Créer une liste pour les identifiants
identifiants = []

# Donner un identifiant à chaque morceau
for numero in range(len(tous_les_morceaux)):
    identifiant = "pdf_morceau_" + str(numero)
    identifiants.append(identifiant)

# Afficher quelques identifiants
print("Nombre d'identifiants :", len(identifiants))
print("Premier identifiant :", identifiants[0])



# Créer une liste pour les textes
textes = []

# Récupérer le texte de chaque morceau
for morceau in tous_les_morceaux:
    textes.append(morceau["text"])

# Afficher le nombre de textes
print("Nombre de textes préparés :", len(textes))


# Créer une liste pour les numéros de page
numeros_pages = []

# Récupérer la page de chaque morceau
for morceau in tous_les_morceaux:
    numeros_pages.append(morceau["page"])

# Afficher le nombre de numéros de page
print("Nombre de numéros de page :", len(numeros_pages))



# Créer les informations de source pour chaque morceau
metadonnees = []

for numero_page in numeros_pages:
    metadonnees.append({
        "page": numero_page,
        "source": "document.pdf"
    })

# Enregistrer les morceaux dans ChromaDB
collection.add(
    ids=identifiants,
    documents=textes,
    metadatas=metadonnees
)

print("Le PDF a été enregistré dans ChromaDB !")

print("Nombre de morceaux dans ChromaDB :", collection.count())