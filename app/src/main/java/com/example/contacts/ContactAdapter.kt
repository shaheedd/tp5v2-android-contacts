package com.example.contacts

import android.content.Context
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.BaseAdapter
import android.widget.ImageView
import android.widget.TextView

/** ListView personnalisée : photo, nom, prénom et téléphone sur chaque ligne. */
class ContactAdapter(
    private val context: Context,
    private val contacts: List<Contact>
) : BaseAdapter() {

    override fun getCount(): Int = contacts.size

    override fun getItem(position: Int): Contact = contacts[position]

    override fun getItemId(position: Int): Long = position.toLong()

    override fun getView(position: Int, convertView: View?, parent: ViewGroup): View {
        val view: View
        val holder: ViewHolder
        if (convertView == null) {
            view = LayoutInflater.from(context).inflate(R.layout.item_contact, parent, false)
            holder = ViewHolder(view)
            view.tag = holder
        } else {
            view = convertView
            holder = view.tag as ViewHolder
        }

        val contact = contacts[position]
        holder.tvNom.text = contact.nom
        holder.tvPrenom.text = contact.prenom
        holder.tvTel.text = contact.telephone

        val bitmap = PhotoLoader.load(context.contentResolver, contact.photoPath)
        if (bitmap != null) {
            holder.imgPhoto.setImageBitmap(bitmap)
        } else {
            holder.imgPhoto.setImageResource(R.drawable.ic_person)
        }
        return view
    }

    private class ViewHolder(view: View) {
        val imgPhoto: ImageView = view.findViewById(R.id.imgPhoto)
        val tvNom: TextView = view.findViewById(R.id.tvNom)
        val tvPrenom: TextView = view.findViewById(R.id.tvPrenom)
        val tvTel: TextView = view.findViewById(R.id.tvTel)
    }
}
