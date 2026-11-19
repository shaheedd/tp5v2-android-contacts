# TP5 Android — Liste de contacts V2

Application Android Kotlin (Interfaces XML) avec deux activités, une `ListView`
personnalisée, la gestion des photos et des intents explicites/implicites.

## Fonctionnalités

- `MainActivity` : liste personnalisée (`ContactAdapter`) affichant photo, nom,
  prénom et téléphone de 5 contacts.
- `DetailActivity` : ouverte par un **Intent explicite**, affiche et permet de
  modifier nom, prénom, téléphone et e-mail.
- **Appeler** : Intent implicite `ACTION_DIAL` (`tel:`).
- **Envoyer un e-mail** : Intent implicite `ACTION_SEND` avec type `message/rfc822`
  et `EXTRA_EMAIL` ; affiche le sélecteur d'applications.
- **Choisir une photo** : `ActivityResultContracts.GetContent()` ; l'image est
  copiée dans le stockage interne puis exposée via `FileProvider`.
- **Prendre une photo** : `ActivityResultContracts.TakePicture()` avec Uri
  `FileProvider` ; absence de caméra ou annulation gérée.
- **Enregistrer** : `setResult(RESULT_OK, ...)` + `notifyDataSetChanged()` dans
  `MainActivity` ; **Annuler** : `RESULT_CANCELED` sans modification.
- Validations : champs vides, e-mail invalide, annulation photo, absence
  d'application compatible.

## Structure

| Fichier | Rôle |
| --- | --- |
| `MainActivity.kt` | Liste + lancement de `DetailActivity` + retour de résultat |
| `DetailActivity.kt` | Édition, photos, intents, enregistrement |
| `Contact.kt` | Modèle `Serializable` |
| `ContactAdapter.kt` | `BaseAdapter` personnalisé avec `ViewHolder` |
| `PhotoLoader.kt` | Décodage des Uri photo |
| `res/xml/file_paths.xml` | Chemins autorisés du `FileProvider` |
| `captures/` | Captures d'écran réelles |
| `compte-rendu/` | Compte rendu PDF |

## Livrables

- [Compte rendu PDF](compte-rendu/compte-rendu-tp5v2.pdf) — démarche, tests, difficultés.
- [Captures d'écran réelles](captures/) — MainActivity, DetailActivity, modification,
  galerie, caméra, appel et e-mail.

## Dépôt

https://github.com/shaheedd/tp5v2-android-contacts

## Compilation

```powershell
.\gradlew assembleDebug
```

`compileSdk` est fixé à 37 (seule plateforme installée localement), `minSdk` à 24
et `targetSdk` à 35.
