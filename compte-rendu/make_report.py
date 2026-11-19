# -*- coding: utf-8 -*-
"""Génère le compte rendu PDF final du TP5 V2 (propre, accentué, avec captures)."""
import os
import pymupdf

ROOT = r"C:\Users\ASUS\Documents\Projet par défaut\tp5v2-android-contacts"
CAP = os.path.join(ROOT, "captures")
OUT = os.path.join(ROOT, "compte-rendu", "compte-rendu-tp5v2.pdf")

W, H = 595, 842
M = 52
BLUE = (0.08, 0.22, 0.38)
GREY = (0.15, 0.15, 0.15)

doc = pymupdf.open()


def base_page():
    return doc.new_page(width=W, height=H)


def section_page(title, parts):
    """Une page de contenu : titre + paires (sous-titre, paragraphe)."""
    p = base_page()
    y = M + 6
    p.insert_text((M, y), title, fontname="hebo", fontsize=16, color=BLUE)
    y += 14
    p.draw_line((M, y + 6), (W - M, y + 6), color=(0.65, 0.74, 0.82), width=1)
    y += 28
    for heading, body in parts:
        p.insert_text((M, y), heading, fontname="hebo", fontsize=11.5, color=(0.10, 0.34, 0.55))
        y += 17
        rect = pymupdf.Rect(M + 4, y, W - M, min(y + 300, H - M - 20))
        used = p.insert_textbox(rect, body, fontname="helv", fontsize=10.3,
                                lineheight=1.45, color=GREY)
        if used < 0:
            raise RuntimeError(f"Débordement de texte pour « {heading} »")
        y = rect.y0 + used + 20
    return p


# ---------------------------------------------------------------- page de garde
p = base_page()
p.draw_rect(pymupdf.Rect(0, 0, W, 190), color=(0.08, 0.22, 0.38), fill=(0.08, 0.22, 0.38))
p.insert_text((M, 78), "COMPTE RENDU DE TRAVAUX PRATIQUES",
              fontname="hebo", fontsize=12, color=(0.75, 0.86, 0.95))
p.insert_text((M, 118), "Android · Liste de contacts (Version 2)",
              fontname="hebo", fontsize=20, color=(1, 1, 1))
p.insert_text((M, 150), "Kotlin · Android Studio · Interfaces XML",
              fontname="helv", fontsize=11, color=(0.82, 0.90, 0.97))

y = 240
for label, value in [
    ("Étudiant", "shahed attari"),
    ("Matière", "Développement Android"),
    ("TP", "TP5 · Liste de contacts V2"),
    ("Date", "19 novembre 2026"),
    ("Environnement", "Émulateur Small_Phone · API 35 · 720 × 1280 px"),
    ("Dépôt GitHub", "github.com/shaheedd/tp5v2-android-contacts"),
]:
    p.insert_text((M, y), label, fontname="hebo", fontsize=10.5, color=(0.10, 0.34, 0.55))
    p.insert_text((M + 110, y), value, fontname="helv", fontsize=10.5, color=GREY)
    y += 26

p.draw_line((M, y + 8), (W - M, y + 8), color=(0.65, 0.74, 0.82), width=1)
p.insert_text((M, y + 36), "Résumé", fontname="hebo", fontsize=12, color=BLUE)
resume = (
    "Ce compte rendu présente la réalisation d'une application Android en Kotlin comportant "
    "deux activités : une liste personnalisée de contacts et un écran de détail modifiable. "
    "L'application permet d'appeler un contact, de lui envoyer un e-mail, de choisir sa photo "
    "dans la galerie ou de la prendre avec l'appareil photo, puis de renvoyer les données "
    "modifiées à la liste. Les tests effectués sur émulateur et les difficultés rencontrées "
    "sont détaillés dans les pages suivantes, accompagnés de captures d'écran réelles."
)
p.insert_textbox(pymupdf.Rect(M, y + 56, W - M, H - M - 20), resume,
                 fontname="helv", fontsize=10.3, lineheight=1.45, color=GREY)

# --------------------------------------------------------------------- sommaire
p = base_page()
p.insert_text((M, M + 6), "Sommaire", fontname="hebo", fontsize=16, color=BLUE)
p.draw_line((M, M + 32), (W - M, M + 32), color=(0.65, 0.74, 0.82), width=1)
y = M + 66
toc = [
    ("1. Objectif du TP", "3"),
    ("2. Environnement de développement", "3"),
    ("3. Architecture du projet", "4"),
    ("4. Réalisation détaillée", "5"),
    ("5. Tests effectués et résultats", "7"),
    ("6. Difficultés rencontrées", "8"),
    ("7. Conclusion", "8"),
    ("Captures d'écran réelles (1 à 8)", "9 à 16"),
]
for label, page_no in toc:
    p.insert_text((M, y), label, fontname="helv", fontsize=11.5, color=GREY)
    p.insert_text((W - M - 60, y), page_no, fontname="helv", fontsize=11.5, color=GREY)
    p.draw_line((M, y + 10), (W - M, y + 10), color=(0.88, 0.90, 0.93), width=0.6)
    y += 32

# ------------------------------------------------------------------------ pages
section_page("1. Objectif du TP · 2. Environnement", [
    ("1. Objectif du TP",
     "Réaliser une application Android en Kotlin avec deux activités : MainActivity, qui affiche "
     "plusieurs contacts dans une ListView personnalisée, et DetailActivity, qui affiche et permet "
     "de modifier le nom, le prénom, le téléphone et l'e-mail du contact sélectionné. L'application "
     "doit également ouvrir le composeur téléphonique et une application de messagerie par des intents "
     "implicites, choisir une photo dans la galerie ou en prendre avec l'appareil photo, puis "
     "renvoyer les données modifiées à la liste grâce au mécanisme de résultat d'activité. Enfin, "
     "les cas courants (champs vides, annulation d'une photo, absence d'application compatible, "
     "caméra indisponible) doivent être gérés."),
    ("2. Environnement de développement",
     "Android Studio, Kotlin, Android Gradle Plugin 9.4.1 et Gradle 9.6.0. compileSdk 37 (seule "
     "plateforme installée localement), minSdk 24, targetSdk 35, JDK 17. Dépendances : "
     "androidx.core:core-ktx 1.13.1, androidx.appcompat:appcompat 1.7.0 et "
     "androidx.activity:activity-ktx 1.8.0. Les essais ont été réalisés sur l'émulateur "
     "Small_Phone (API 35, 720 × 1280 px, 320 dpi), ainsi que sur le dépôt public GitHub "
     "shaheedd/tp5v2-android-contacts."),
])

section_page("3. Architecture du projet", [
    ("Fichiers Kotlin",
     "MainActivity.kt · liste de cinq contacts, ContactAdapter, Intent explicite vers "
     "DetailActivity et ActivityResultLauncher qui reçoit le contact modifié.\n"
     "DetailActivity.kt · formulaire, validations, intents implicites, galerie et caméra via "
     "l'Activity Result API, setResult(RESULT_OK) ou RESULT_CANCELED.\n"
     "Contact.kt · modèle Serializable (nom, prénom, téléphone, e-mail, chemin de la photo).\n"
     "ContactAdapter.kt · BaseAdapter avec ViewHolder affichant photo, nom, prénom et téléphone.\n"
     "PhotoLoader.kt · décodage des Uri photo avec réduction d'échantillonnage."),
    ("Ressources et configuration",
     "activity_main.xml · ListView plein écran.\n"
     "item_contact.xml · ligne personnalisée (ImageView + trois TextView).\n"
     "activity_detail.xml · photo, deux boutons photo, quatre champs de saisie et quatre "
     "boutons d'action, dans un ScrollView.\n"
     "res/xml/file_paths.xml · chemins exposés par le FileProvider (photos internes et cache "
     "de la caméra).\n"
     "AndroidManifest.xml · activités, FileProvider, et déclarations <queries> nécessaires à "
     "la résolution des intents implicites depuis Android 11."),
])

section_page("4. Réalisation détaillée", [
    ("4.1 Liste personnalisée",
     "L'adapter ContactAdapter étend BaseAdapter et applique le motif ViewHolder pour recycler "
     "les lignes. Chaque ligne affiche la photo du contact, son nom en gras, son prénom et son "
     "numéro de téléphone. Lorsqu'aucune photo n'est renseignée, un avatar par défaut est affiché."),
    ("4.2 Intent explicite et retour de résultat",
     "Au clic sur une ligne, MainActivity lance DetailActivity avec le contact et sa position "
     "en extras. Le bouton Enregistrer construit un Contact mis à jour puis appelle "
     "setResult(RESULT_OK, data) ; MainActivity remplace alors l'élément à la bonne position et "
     "appelle adapter.notifyDataSetChanged() pour redessiner immédiatement la liste. Le bouton "
     "Annuler renvoie simplement RESULT_CANCELED : aucune donnée n'est modifiée."),
])

section_page("4. Réalisation détaillée (suite)", [
    ("4.3 Gestion des photos",
     "Le bouton « Choisir une photo » utilise ActivityResultContracts.GetContent(). L'image "
     "sélectionnée est copiée dans filesDir/photos puis réexposée via le FileProvider afin que "
     "son Uri reste lisible après le retour de l'activité. Le bouton « Prendre une photo » "
     "utilise ActivityResultContracts.TakePicture() avec une Uri FileProvider située dans "
     "cacheDir/camera. Une annulation ou un échec est détecté et signalé par un Toast."),
    ("4.4 Intents implicites",
     "« Appeler » lance ACTION_DIAL avec une Uri tel: construite à partir du numéro nettoyé de "
     "ses espaces. « Envoyer un e-mail » lance ACTION_SENDTO avec une Uri mailto: et l'extra "
     "EXTRA_EMAIL. La présence d'une application compatible est vérifiée avec resolveActivity(), "
     "et un Toast indique l'absence d'application le cas échéant."),
    ("4.5 Validations",
     "Les quatre champs sont obligatoires : une erreur est affichée sur chaque champ vide avec "
     "un Toast récapitulatif. Le format de l'adresse e-mail est contrôlé avec "
     "Patterns.EMAIL_ADDRESS. L'absence de caméra, le refus ou l'annulation d'une opération photo "
     "sont pris en charge."),
])

section_page("5. Tests effectués et résultats", [
    ("Tests fonctionnels sur émulateur",
     "[OK] Ouverture d'un contact : DetailActivity affiche les données (Dupont Claire, "
     "06 12 34 56 78, claire.dupont@example.com).\n"
     "[OK] Modification du nom en « Dupont-Modifie » puis Enregistrer : la liste est actualisée "
     "immédiatement (capture 4).\n"
     "[OK] Annuler : les anciennes valeurs restent inchangées.\n"
     "[OK] Champs vides : messages d'erreur affichés, aucun enregistrement.\n"
     "[OK] Adresse e-mail invalide : erreur affichée sur le champ.\n"
     "[OK] Choisir une photo : le sélecteur système s'ouvre (capture 5) ; une annulation ne "
     "modifie pas la photo.\n"
     "[OK] Prendre une photo : l'application caméra s'ouvre (capture 6) ; l'annulation est "
     "correctement détectée.\n"
     "[OK] Appeler : le composeur téléphonique s'ouvre avec le numéro (capture 7).\n"
     "[OK] Envoyer un e-mail : une application de messagerie s'ouvre avec le destinataire "
     "(capture 8).\n"
     "Compilation vérifiée : ./gradlew assembleDebug -> BUILD SUCCESSFUL."),
])

section_page("6. Difficultés rencontrées · 7. Conclusion", [
    ("6. Difficultés rencontrées",
     "1) Sous Android 11+, resolveActivity() renvoyait null pour ACTION_DIAL et ACTION_SENDTO : "
     "il a fallu ajouter les éléments <queries> dans le manifeste pour rendre les applications "
     "tierces visibles.\n"
     "2) Une Uri issue de la galerie n'est pas durable : l'image est donc copiée dans le stockage "
     "interne avant d'être réexposée par le FileProvider.\n"
     "3) La caméra n'écrit que dans une Uri content fournie par l'application, d'où la mise en "
     "place de file_paths.xml et de deux répertoires dédiés.\n"
     "4) Le SDK local ne contenant que la plateforme 37, compileSdk a été aligné sur 37 tout en "
     "conservant minSdk 24 et targetSdk 35."),
    ("7. Conclusion",
     "Toutes les fonctionnalités demandées sont implémentées et vérifiées sur l'émulateur. Le "
     "projet compile sans erreur, est publié sur GitHub et est accompagné de ce compte rendu "
     "et de huit captures d'écran réelles dans le dossier captures/."),
])

# ------------------------------------------------------------------- captures
shots = [
    ("01-mainactivity.png", "Capture 1 · MainActivity",
     "La ListView personnalisée affiche les cinq contacts avec photo, nom, prénom et téléphone."),
    ("02-detailactivity.png", "Capture 2 · DetailActivity",
     "Les informations du contact et les boutons d'action sont affichés après un Intent explicite."),
    ("03-modification.png", "Capture 3 · Modification",
     "Le nom est remplacé par « Dupont-Modifie » dans le champ Nom."),
    ("04-liste-modifiee.png", "Capture 4 · Liste actualisée",
     "Après Enregistrer, le retour de résultat met immédiatement la liste à jour."),
    ("05-galerie.png", "Capture 5 · Galerie",
     "Le sélecteur de photos système s'ouvre via ActivityResultContracts.GetContent()."),
    ("06-camera.png", "Capture 6 · Appareil photo",
     "L'application caméra s'ouvre via ActivityResultContracts.TakePicture()."),
    ("07-appel.png", "Capture 7 · Appel",
     "L'Intent implicite ACTION_DIAL ouvre le composeur avec le numéro du contact."),
    ("08-email.png", "Capture 8 · E-mail",
     "L'Intent implicite ACTION_SENDTO ouvre une application de messagerie."),
]

for filename, title, note in shots:
    path = os.path.join(CAP, filename)
    if not os.path.exists(path):
        continue
    p = base_page()
    p.insert_text((M, 44), title, fontname="hebo", fontsize=15, color=BLUE)
    p.draw_line((M, 62), (W - M, 62), color=(0.65, 0.74, 0.82), width=1)
    img = pymupdf.Pixmap(path)
    scale = min(360 / img.width, 640 / img.height)
    w, h = img.width * scale, img.height * scale
    p.insert_image(pymupdf.Rect((W - w) / 2, 76, (W + w) / 2, 76 + h), filename=path)
    p.insert_textbox(pymupdf.Rect(M, 730, W - M, 798), note,
                     fontname="helv", fontsize=10.2, lineheight=1.4, color=GREY)

# --------------------------------------------------------------- numérotation
for i, page in enumerate(doc, start=1):
    page.insert_text((W - M - 40, H - 24), str(i), fontname="helv", fontsize=9,
                     color=(0.45, 0.45, 0.45))

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT, garbage=4, deflate=True)
print("PDF:", OUT, "| pages:", doc.page_count, "| images:",
      sum(len(pg.get_images()) for pg in doc))
