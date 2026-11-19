package com.example.contacts

import android.content.Intent
import android.os.Bundle
import android.widget.ListView
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private val contacts = mutableListOf(
        Contact("Dupont", "Claire", "06 12 34 56 78", "claire.dupont@example.com"),
        Contact("Martin", "Thomas", "07 23 45 67 89", "thomas.martin@example.com"),
        Contact("Bernard", "Sophie", "06 98 76 54 32", "sophie.bernard@example.com"),
        Contact("Petit", "Lucas", "07 11 22 33 44", "lucas.petit@example.com"),
        Contact("Moreau", "Julien", "06 55 44 33 22", "julien.moreau@example.com")
    )

    private lateinit var adapter: ContactAdapter

    /** Retour de DetailActivity : on remplace le contact modifié puis on rafraîchit la liste. */
    private val detailLauncher =
        registerForActivityResult(ActivityResultContracts.StartActivityForResult()) { result ->
            if (result.resultCode == RESULT_OK) {
                val contact = result.data?.getSerializableExtra(EXTRA_CONTACT) as? Contact
                val position = result.data?.getIntExtra(EXTRA_POSITION, -1) ?: -1
                if (contact != null && position in contacts.indices) {
                    contacts[position] = contact
                    adapter.notifyDataSetChanged()
                    Toast.makeText(this, R.string.msg_enregistre, Toast.LENGTH_SHORT).show()
                }
            }
        }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        adapter = ContactAdapter(this, contacts)
        val lvContacts = findViewById<ListView>(R.id.lvContacts)
        lvContacts.adapter = adapter

        lvContacts.setOnItemClickListener { _, _, position, _ ->
            val intent = Intent(this, DetailActivity::class.java).apply {
                putExtra(EXTRA_CONTACT, contacts[position])
                putExtra(EXTRA_POSITION, position)
            }
            // Intent explicite : on cible précisément DetailActivity.
            detailLauncher.launch(intent)
        }
    }
}
