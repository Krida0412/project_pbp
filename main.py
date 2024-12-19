import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class ContactApp(App):
    def build(self):
        # Layout utama untuk menampung semua elemen
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Bagian input (Form)
        input_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)
        
        # TextInput untuk nama
        self.name_input = TextInput(
            hint_text='Nama',git 
            background_color=(218/255, 247/255, 166/255, 1),
            font_size=20,
            height=65,
            size_hint_y=None
        )

        # TextInput untuk nomor telepon (hanya angka)
        self.phone_input = TextInput(
            hint_text='Nomor Telepon',git 
            background_color=(0.9, 0.9, 0.9, 1),
            font_size=20,
            height=65,
            size_hint_y=None,
            input_filter='int'
        )

        # Tombol Add Contact
        self.add_button = Button(
            text='Tambah Kontak',
            background_color=(0.1, 0.6, 0.1, 1),
            font_size=18,
            height=50,
            size_hint_y=None,
            on_press=self.add_contact
        )

        # Menambahkan elemen ke input_layout
        input_layout.add_widget(self.name_input)
        input_layout.add_widget(self.phone_input)
        input_layout.add_widget(self.add_button)

        # Menambahkan input_layout ke layout utama di bagian atas
        self.layout.add_widget(input_layout)

        # ScrollView untuk daftar kontak
        self.contacts_scroll = ScrollView(size_hint=(1, 1))
        self.contacts_grid = GridLayout(cols=1, size_hint_y=None)
        self.contacts_grid.bind(minimum_height=self.contacts_grid.setter('height'))
        self.contacts_scroll.add_widget(self.contacts_grid)

        # Menambahkan ScrollView ke layout utama
        self.layout.add_widget(self.contacts_scroll)

        # Memuat kontak dari database
        self.load_contacts()

        return self.layout

    def add_contact(self, instance):
        name = self.name_input.text
        phone = self.phone_input.text
        if name and phone:
            conn = sqlite3.connect('contacts.db')
            c = conn.cursor()
            c.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (name, phone))
            conn.commit()
            conn.close()
            self.name_input.text = ''
            self.phone_input.text = ''
            self.load_contacts()

    def load_contacts(self):
        self.contacts_grid.clear_widgets()
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute('SELECT * FROM contacts')
        contacts = c.fetchall()
        conn.close()

        for contact in contacts:
            contact_widget = BoxLayout(size_hint_y=None, height=50)
            contact_label = Label(text=f'{contact[1]} - {contact[2]}', size_hint_x=0.6, font_size=18)
            contact_widget.add_widget(contact_label)

            # Tombol Edit
            edit_button = Button(
                text='Edit',
                size_hint_x=0.2,
                font_size=14,
                background_color=(0.1, 0.5, 1, 1),
                on_press=lambda instance, c_id=contact[0], c_name=contact[1], c_phone=contact[2]: self.edit_contact(c_id, c_name, c_phone)
            )
            contact_widget.add_widget(edit_button)

            # Tombol Delete
            delete_button = Button(
                text='Hapus',
                size_hint_x=0.2,
                font_size=14,
                background_color=(1, 0, 0, 1),
                on_press=lambda instance, c_id=contact[0]: self.delete_contact(c_id)
            )
            contact_widget.add_widget(delete_button)

            self.contacts_grid.add_widget(contact_widget)

    def edit_contact(self, c_id, c_name, c_phone):
        self.name_input.text = c_name
        self.phone_input.text = c_phone
        self.add_button.text = 'Perbarui kontak'
        self.add_button.bind(on_press=lambda instance, c_id=c_id: self.update_contact(c_id))

    def update_contact(self, c_id):
        name = self.name_input.text
        phone = self.phone_input.text
        if name and phone:
            conn = sqlite3.connect('contacts.db')
            c = conn.cursor()
            c.execute('UPDATE contacts SET name = ?, phone = ? WHERE id = ?', (name, phone, c_id))
            conn.commit()
            conn.close()
            self.name_input.text = ''
            self.phone_input.text = ''
            self.add_button.text = 'Tambah Kontak'
            self.load_contacts()

    def delete_contact(self, c_id):
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute('DELETE FROM contacts WHERE id = ?', (c_id,))
        conn.commit()
        conn.close()
        self.load_contacts()

if __name__ == '__main__':
    ContactApp().run()
