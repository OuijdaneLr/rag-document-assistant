
import pymupdf
"""
# Ouvrir le document PDF
document = pymupdf.open("data/document.pdf")

pages = []

for numero, page in enumerate(document, start=1):
    texte = page.get_text()

    pages.append({
        "page": numero,
        "text": texte
    })

document.close()

print("Nombre de pages extraites :", len(pages))

# Afficher un aperçu de la première page
if pages:
    print("\nNuméro de page :", pages[0]["page"])
    print("Aperçu du texte :")
    print(pages[0]["text"][:500])
"""

import pymupdf


def extraire_texte_pdf(chemin_pdf):
    document = pymupdf.open(chemin_pdf)

    pages = []

    for numero, page in enumerate(document, start=1):
        texte = page.get_text()

        pages.append({
            "page": numero,
            "text": texte
        })

    document.close()

    return pages


# Tester la fonction
pages = extraire_texte_pdf("data/document.pdf")

print("Nombre de pages extraites :", len(pages))

if pages:
    print("\nNuméro de page :", pages[0]["page"])
    print("Aperçu du texte :")
    print(pages[0]["text"][:500])

print("\nExtraction terminée avec succès !")


def decouper_texte(texte, taille=500):
    morceaux = []

    for debut in range(0, len(texte), taille):
        morceau = texte[debut:debut + taille]
        morceaux.append(morceau)

    return morceaux


# Tester le découpage de la première page
if pages:
    morceaux = decouper_texte(pages[0]["text"])

    print("\nNombre de morceaux :", len(morceaux))
    print("Taille du premier morceau :", len(morceaux[0]))

print("\nContenu du premier morceau :")
print(morceaux[0])



# Associer chaque morceau à son numéro de page
morceaux_avec_sources = []

for page in pages:
    morceaux_page = decouper_texte(page["text"])

    for morceau in morceaux_page:
        morceaux_avec_sources.append({
            "page": page["page"],
            "text": morceau
        })

print("\nNombre total de morceaux :", len(morceaux_avec_sources))

if morceaux_avec_sources:
    print("Page du premier morceau :", morceaux_avec_sources[0]["page"])
