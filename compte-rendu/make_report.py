# -*- coding: utf-8 -*-
"""Génère le compte rendu PDF du TP5 V2 avec les captures réelles."""
import os
import pymupdf

ROOT = r"C:\Users\ASUS\Documents\Projet par défaut\tp5v2-android-contacts"
CAP = os.path.join(ROOT, "captures")
OUT = os.path.join(ROOT, "compte-rendu", "compte-rendu-tp5v2.pdf")

doc = pymupdf.open()
A4 = (595, 842)
MARGIN = 50


def new_text_page(title=None):
    p = doc.new_page(width=A4[0], height=A4[1])
    if title:
        p.insert_text((MARGIN, MARGIN), title, fontname="hebo", fontsize=17,
                      color=(0.08, 0.20, 0.35))
        p.draw_line((MARGIN, MARGIN + 20), (A4[0] - MARGIN, MARGIN + 20),
                    color=(0.6, 0.7, 0.8), width=1)
        return p, MARGIN + 38
    p.insert_text((MARGIN, MARGIN), "(suite)", fontname="hebo", fontsize=12,
                  color=(0.10, 0.30, 0.50))
    return p, MARGIN + 22


def text_page(title, blocks):
    page, y = new_text_page(title)
    for heading, body in blocks:
        if y > A4[1] - MARGIN - 110:
            page, y = new_text_page()
        page.insert_text((MARGIN, y), heading, fontname="hebo", fontsize=12,
                         color=(0.10, 0.30, 0.50))
        y += 18
        bottom = min(y + 460, A4[1] - MARGIN)
        rect = pymupdf.Rect(MARGIN + 6, y, A4[0] - MARGIN, bottom)
        used = page.insert_textbox(rect, body, fontname="helv", fontsize=10.2,
                                   lineheight=1.42, color=(0.12, 0.12, 0.12))
        if used < 0:
            page, y = new_text_page()
            rect = pymupdf.Rect(MARGIN + 6, y, A4[0] - MARGIN, A4[1] - MARGIN)
            used = page.insert_textbox(rect, body, fontname="helv", fontsize=10.2,
                                       lineheight=1.42, color=(0.12, 0.12, 0.12))
        y = rect.y0 + used + 20
    return page


text_page("Compte rendu - TP5 Android : Liste de contacts (Version 2)", [
    ("1. Objectif",
     "Réaliser une application Android en Kotlin avec deux activités : MainActivity (liste "
     "personnalisée de contacts) et DetailActivity (consultation et modification d'un contact). "
     "L'application doit permettre d'appeler, d'envoyer un e-mail, de choisir une photo dans la "
     "galerie ou d'en prendre une avec l'appareil photo, puis de renvoyer les données modifiées "
     "à la liste grâce au mécanisme de résultat d'activité."),
    ("2. Environnement",
     "Android Studio / Kotlin, Android Gradle Plugin 9.4.1, Gradle 9.6.0. compileSdk 37 (seule "
     "plateforme installée localement), minSdk 24, targetSdk 35, Java 17. Dépendances : "
     "androidx.core:core-ktx 1.13.1, androidx.appcompat:appcompat 1.7.0, "
     "androidx.activity:activity-ktx 1.8.0. Tests sur l'émulateur Small_Phone (API 35, "
     "720 x 1280 px, 320 dpi). Dépôt GitHub : github.com/shaheedd/tp5v2-android-contacts."),
    ("3. Architecture du projet",
     "MainActivity.kt : liste de 5 contacts, ContactAdapter, Intent explicite vers DetailActivity "
     "et ActivityResultLauncher pour recevoir le contact modifié.\n"
     "DetailActivity.kt : formulaires, validations, intents implicites, galerie/caméra via "
     "Activity Result API, setResult(RESULT_OK) ou RESULT_CANCELED.\n"
     "Contact.kt : modèle Serializable (nom, prénom, téléphone, email, chemin de photo).\n"
     "ContactAdapter.kt : BaseAdapter avec ViewHolder affichant photo, nom, prénom et téléphone.\n"
     "PhotoLoader.kt : décodage des Uri avec réduction d'échantillonnage.\n"
     "res/xml/file_paths.xml : chemins exposes par le FileProvider."),
])

text_page("4. Réalisation détaillée", [
    ("4.1 Liste personnalisée",
     "Chaque ligne (item_contact.xml) contient une ImageView et trois TextView. L'adapter "
     "recycle les vues avec le motif ViewHolder et remplace l'image par un avatar par défaut "
     "lorsqu'aucune photo n'est renseignée."),
    ("4.2 Intent explicite et retour de résultat",
     "Au clic sur une ligne, MainActivity lance DetailActivity avec le contact et sa position "
     "en extras. Le bouton Enregistrer construit un Contact mis a jour et appelle "
     "setResult(RESULT_OK, data) ; MainActivity remplace alors l'élément et appelle "
     "adapter.notifyDataSetChanged(). Le bouton Annuler renvoie RESULT_CANCELED : aucune "
     "modification n'est appliquée."),
    ("4.3 Photos",
     "La galerie utilise ActivityResultContracts.GetContent(). L'image sélectionnée est copiée "
     "dans filesDir/photos puis exposee via FileProvider afin que l'Uri reste lisible après "
     "le retour de l'application. La caméra utilise ActivityResultContracts.TakePicture() avec "
     "une Uri FileProvider dans cacheDir/caméra. Les annulations et échecs affichent un Toast."),
    ("4.4 Intents implicites",
     "Appeler : ACTION_DIAL avec Uri tel:. Envoyer un e-mail : ACTION_SENDTO avec Uri mailto: "
     "et extra EXTRA_EMAIL. La présence d'une application compatible est vérifiée avec "
     "resolveActivity(). Le manifeste declare des éléments <queries> pour la visibilité des "
     "applications tierces a partir d'Android 11."),
    ("4.5 Validations",
     "Champs obligatoires (nom, prénom, téléphone, e-mail) : messages d'erreur sur les EditText "
     "et Toast. Format de l'e-mail verifie avec Patterns.EMAIL_ADDRESS. Numeros nettoyes des "
     "espaces avant l'appel. Absence de caméra, refus ou annulation pris en charge."),
])

text_page("5. Tests effectués et résultats", [
    ("Tests fonctionnels",
     "[OK] Ouverture d'un contact : DetailActivity affiche les données (Dupont Claire, "
     "06 12 34 56 78, claire.dupont@example.com).\n"
     "[OK] Modification du nom en 'Dupont-Modifie' puis Enregistrer : la liste est "
     "actualisée immediatement (capture 04).\n"
     "[OK] Annuler : les anciennes valeurs restent inchangées.\n"
     "[OK] Champs vides : messages d'erreur affiches, aucun enregistrement.\n"
     "[OK] Adresse e-mail invalide : error sur le champ.\n"
     "[OK] Bouton Choisir une photo : le sélecteur système s'ouvre (capture 05) ; "
     "une annulation ne modifié pas la photo.\n"
     "[OK] Bouton Prendre une photo : l'application caméra s'ouvre (capture 06) ; "
     "une annulation est correctement détectée.\n"
     "[OK] Bouton Appeler : le composeur telephonique s'ouvre avec le numero (capture 07).\n"
     "[OK] Bouton Envoyer un e-mail : une application de messagerie s'ouvre avec "
     "le destinataire (capture 08)."),
    ("6. Difficultés rencontrees",
     "1) Sous Android 11+, resolveActivity() renvoyait null pour ACTION_DIAL et ACTION_SENDTO : "
     "il a fallu ajouter les declarations <queries> dans le manifeste.\n"
     "2) Une Uri de galerie n'est pas durable : l'image est donc copiée dans le stockage interne "
     "avant d'etre réexposée par le FileProvider.\n"
     "3) La caméra n'ecrit que dans une Uri content fournie par l'application, d'ou la mise en "
     "place de file_paths.xml et de deux repertoires de stockage.\n"
     "4) Le SDK local ne contenant que la plateforme 37, compileSdk a ete aligne sur 37 tout en "
     "conservant minSdk 24 et targetSdk 35."),
    ("7. Conclusion",
     "Toutes les fonctionnalites demandees sont implémentées et vérifiées sur l'émulateur. "
     "Le projet compile sans erreur (BUILD SUCCESSFUL), est publié sur GitHub et accompagne "
     "de ce compte rendu ainsi que de captures d'écran réelles dans le dossier captures/."),
])

captions = [
    ("01-mainactivity.png", "Capture 1 - MainActivity : liste personnalisée des contacts."),
    ("02-detailactivity.png", "Capture 2 - DetailActivity : données du contact et boutons d'action."),
    ("03-modification.png", "Capture 3 - Modification du nom dans DetailActivity."),
    ("04-liste-modifiee.png", "Capture 4 - Liste actualisée après Enregistrer."),
    ("05-galerie.png", "Capture 5 - Selecteur système de photo (galerie)."),
    ("06-camera.png", "Capture 6 - Application appareil photo."),
    ("07-appel.png", "Capture 7 - Composeur telephonique ouvert par l'intent implicite."),
    ("08-email.png", "Capture 8 - Application de messagerie ouverte par l'intent implicite."),
]

for filename, caption in captions:
    path = os.path.join(CAP, filename)
    if not os.path.exists(path):
        continue
    page = doc.new_page(width=A4[0], height=A4[1])
    page.insert_text((MARGIN, 42), "Captures d'écran réelles", fontname="hebo", fontsize=15,
                     color=(0.08, 0.20, 0.35))
    img = pymupdf.Pixmap(path)
    max_w, max_h = 380, 690
    scale = min(max_w / img.width, max_h / img.height)
    w, h = img.width * scale, img.height * scale
    rect = pymupdf.Rect((A4[0] - w) / 2, 66, (A4[0] + w) / 2, 66 + h)
    page.insert_image(rect, filename=path)
    page.insert_text((MARGIN, 770), caption, fontname="helv", fontsize=10.5,
                     color=(0.15, 0.15, 0.15))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT, garbage=4, deflate=True)
print("PDF:", OUT, "pages:", doc.page_count, "size:", os.path.getsize(OUT))
