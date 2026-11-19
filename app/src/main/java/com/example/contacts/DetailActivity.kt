package com.example.contacts

import android.content.Intent
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Bundle
import android.util.Patterns
import android.widget.Button
import android.widget.EditText
import android.widget.ImageView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.FileProvider
import java.io.File
import java.io.FileOutputStream

const val EXTRA_CONTACT = "com.example.contacts.EXTRA_CONTACT"
const val EXTRA_POSITION = "com.example.contacts.EXTRA_POSITION"

class DetailActivity : AppCompatActivity() {

    private lateinit var contact: Contact
    private var position = -1
    private var currentPhotoPath: String? = null
    private var cameraPhotoUri: Uri? = null

    private lateinit var imgPhotoDetail: ImageView
    private lateinit var etNom: EditText
    private lateinit var etPrenom: EditText
    private lateinit var etTel: EditText
    private lateinit var etEmail: EditText

    /** Galerie : sélection d'une image existante. */
    private val pickImageLauncher =
        registerForActivityResult(ActivityResultContracts.GetContent()) { uri ->
            if (uri == null) {
                toast(R.string.msg_photo_galerie_annulee)
            } else {
                val savedPath = copyToInternalStorage(uri)
                if (savedPath == null) {
                    toast(R.string.msg_erreur_photo)
                } else {
                    currentPhotoPath = savedPath
                    displayPhoto()
                }
            }
        }

    /** Appareil photo : TakePicture dépose la photo directement dans l'Uri fourni. */
    private val takePictureLauncher =
        registerForActivityResult(ActivityResultContracts.TakePicture()) { success ->
            if (success && cameraPhotoUri != null) {
                currentPhotoPath = cameraPhotoUri.toString()
                displayPhoto()
            } else {
                toast(R.string.msg_photo_camera_annulee)
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_detail)

        contact = intent.getSerializableExtra(EXTRA_CONTACT) as? Contact ?: run {
            finish()
            return
        }
        position = intent.getIntExtra(EXTRA_POSITION, -1)
        currentPhotoPath = contact.photoPath

        imgPhotoDetail = findViewById(R.id.imgPhotoDetail)
        etNom = findViewById(R.id.etNom)
        etPrenom = findViewById(R.id.etPrenom)
        etTel = findViewById(R.id.etTel)
        etEmail = findViewById(R.id.etEmail)

        etNom.setText(contact.nom)
        etPrenom.setText(contact.prenom)
        etTel.setText(contact.telephone)
        etEmail.setText(contact.email)
        displayPhoto()

        findViewById<Button>(R.id.btnChoisirPhoto).setOnClickListener {
            pickImageLauncher.launch("image/*")
        }
        findViewById<Button>(R.id.btnPrendrePhoto).setOnClickListener { takePhoto() }
        findViewById<Button>(R.id.btnAppeler).setOnClickListener { callContact() }
        findViewById<Button>(R.id.btnEmail).setOnClickListener { emailContact() }
        findViewById<Button>(R.id.btnEnregistrer).setOnClickListener { saveContact() }
        findViewById<Button>(R.id.btnAnnuler).setOnClickListener {
            setResult(RESULT_CANCELED)
            finish()
        }
    }

    private fun displayPhoto() {
        val bitmap = PhotoLoader.load(contentResolver, currentPhotoPath)
        if (bitmap != null) {
            imgPhotoDetail.setImageBitmap(bitmap)
        } else {
            imgPhotoDetail.setImageResource(R.drawable.ic_person)
        }
    }

    /** Copie l'image de la galerie dans les fichiers de l'application pour qu'elle reste lisible. */
    private fun copyToInternalStorage(source: Uri): String? {
        return try {
            val dir = File(filesDir, "photos").apply { mkdirs() }
            val file = File(dir, "photo_${System.currentTimeMillis()}.jpg")
            val input = contentResolver.openInputStream(source) ?: return null
            input.use { stream ->
                FileOutputStream(file).use { output -> stream.copyTo(output) }
            }
            FileProvider.getUriForFile(this, "$packageName.fileprovider", file).toString()
        } catch (e: Exception) {
            null
        }
    }

    private fun takePhoto() {
        if (!packageManager.hasSystemFeature(PackageManager.FEATURE_CAMERA_ANY)) {
            toast(R.string.msg_pas_camera)
            return
        }
        val dir = File(cacheDir, "camera").apply { mkdirs() }
        val file = File(dir, "photo_${System.currentTimeMillis()}.jpg")
        cameraPhotoUri = FileProvider.getUriForFile(this, "$packageName.fileprovider", file)
        try {
            takePictureLauncher.launch(cameraPhotoUri!!)
        } catch (e: Exception) {
            toast(R.string.msg_pas_camera)
        }
    }

    /** Intent implicite : ouvre le composeur téléphonique. */
    private fun callContact() {
        val number = etTel.text.toString().replace(" ", "")
        if (number.isBlank()) {
            etTel.error = getString(R.string.msg_champs_vides)
            return
        }
        val intent = Intent(Intent.ACTION_DIAL, Uri.parse("tel:$number"))
        if (intent.resolveActivity(packageManager) != null) {
            startActivity(intent)
        } else {
            toast(R.string.msg_pas_app_tel)
        }
    }

    /** Intent implicite : ouvre une application de messagerie avec le destinataire prérempli. */
    private fun emailContact() {
        val address = etEmail.text.toString().trim()
        if (address.isBlank()) {
            etEmail.error = getString(R.string.msg_champs_vides)
            return
        }
        val intent = Intent(Intent.ACTION_SENDTO).apply {
            data = Uri.parse("mailto:$address")
            putExtra(Intent.EXTRA_EMAIL, arrayOf(address))
            putExtra(Intent.EXTRA_SUBJECT, "Contact")
        }
        if (intent.resolveActivity(packageManager) != null) {
            startActivity(Intent.createChooser(intent, getString(R.string.envoyer_email)))
        } else {
            toast(R.string.msg_pas_app_mail)
        }
    }

    private fun validateFields(): Boolean {
        val fields = listOf(etNom, etPrenom, etTel, etEmail)
        val empty = fields.filter { it.text.isBlank() }
        if (empty.isNotEmpty()) {
            empty.forEach { it.error = getString(R.string.msg_champs_vides) }
            toast(R.string.msg_champs_vides)
            return false
        }
        if (!Patterns.EMAIL_ADDRESS.matcher(etEmail.text.toString()).matches()) {
            etEmail.error = getString(R.string.msg_email_invalide)
            return false
        }
        return true
    }

    /** Renvoie les données modifiées à MainActivity grâce au mécanisme de résultat d'activité. */
    private fun saveContact() {
        if (!validateFields()) return
        val updated = Contact(
            nom = etNom.text.toString().trim(),
            prenom = etPrenom.text.toString().trim(),
            telephone = etTel.text.toString().trim(),
            email = etEmail.text.toString().trim(),
            photoPath = currentPhotoPath
        )
        val data = Intent().apply {
            putExtra(EXTRA_CONTACT, updated)
            putExtra(EXTRA_POSITION, position)
        }
        setResult(RESULT_OK, data)
        finish()
    }

    private fun toast(messageRes: Int) {
        Toast.makeText(this, messageRes, Toast.LENGTH_SHORT).show()
    }
}
