package com.example.contacts

import java.io.Serializable

/**
 * Un contact complet, transmissible entre activités via un Intent.
 * Le chemin de la photo est une chaîne (Uri) pour rester sérialisable.
 */
data class Contact(
    val nom: String,
    val prenom: String,
    val telephone: String,
    val email: String,
    val photoPath: String? = null
) : Serializable {

    companion object {
        private const val serialVersionUID = 1L
    }
}
