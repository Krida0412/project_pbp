import sqlite3
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class AplikasiKontak(App):
    def build(self):
        # Layout utama untuk menampung semua elemen
        self.layout_utama = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Bagian input (Form)
        layout_input = BoxLayout(orientation='vertical', size_hint_y=None, height=200, spacing=10)
        
        # TextInput untuk nama
        self.input_nama = TextInput(
            hint_text='Nama',
            background_color=(218/255, 247/255, 166/255, 1),
            font_size=20,
            height=65,
            size_hint_y=None
        )

        # TextInput untuk nomor telepon
        self.input_nomer = TextInput(
            hint_text='Nomor Telepon',
            background_color=(0.9, 0.9, 0.9, 1),
            font_size=20,
            height=65,
            size_hint_y=None,
            input_filter='int'
        )

        # Tombol Tambah Kontak
        self.tombol_tambah = Button(
            text='Tambah Kontak',
            background_color=(0.1, 0.6, 0.1, 1),
            font_size=18,
            height=50,
            size_hint_y=None,
            on_press=self.tambah_kontak
        )

        # Menambahkan elemen ke layout_input
        layout_input.add_widget(self.input_nama)
        layout_input.add_widget(self.input_nomer)
        layout_input.add_widget(self.tombol_tambah)

        # Menambahkan layout_input ke layout utama di bagian atas
        self.layout_utama.add_widget(layout_input)

        # ScrollView untuk daftar kontak
        self.scroll_kontak = ScrollView(size_hint=(1, 1))
        self.grid_kontak = GridLayout(cols=1, size_hint_y=None)
        self.grid_kontak.bind(minimum_height=self.grid_kontak.setter('height'))
        self.scroll_kontak.add_widget(self.grid_kontak)

        # Menambahkan ScrollView ke layout utama
        self.layout_utama.add_widget(self.scroll_kontak)

        # Memuat kontak dari database
        self.memuat_kontak()

        return self.layout_utama

    def tambah_kontak(self, instance):
        nama = self.input_nama.text
        nomer = self.input_nomer.text
        if nama and nomer:
            conn = sqlite3.connect('contacts.db')
            c = conn.cursor()
            c.execute('INSERT INTO contacts (name, phone) VALUES (?, ?)', (nama, nomer))
            conn.commit()
            conn.close()
            self.input_nama.text = ''
            self.input_nomer.text = ''
            self.memuat_kontak()

    def memuat_kontak(self):
        self.grid_kontak.clear_widgets()
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute('SELECT * FROM contacts')
        daftar_kontak = c.fetchall()
        conn.close()

        for kontak in daftar_kontak:
            widget_kontak = BoxLayout(size_hint_y=None, height=50)
            label_kontak = Label(text=f'{kontak[1]} - {kontak[2]}', size_hint_x=0.6, font_size=18)
            widget_kontak.add_widget(label_kontak)

            # Tombol Edit
            tombol_edit = Button(
                text='Edit',
                size_hint_x=0.2,
                font_size=14,
                background_color=(0.1, 0.5, 1, 1),
                on_press=lambda instance, c_id=kontak[0], c_nama=kontak[1], c_nomer=kontak[2]: self.edit_kontak(c_id, c_nama, c_nomer)
            )
            widget_kontak.add_widget(tombol_edit)

            # Tombol Hapus
            tombol_hapus = Button(
                text='Hapus',
                size_hint_x=0.2,
                font_size=14,
                background_color=(1, 0, 0, 1),
                on_press=lambda instance, c_id=kontak[0]: self.hapus_kontak(c_id)
            )
            widget_kontak.add_widget(tombol_hapus)

            self.grid_kontak.add_widget(widget_kontak)

    def edit_kontak(self, c_id, c_nama, c_nomer):
        self.input_nama.text = c_nama
        self.input_nomer.text = c_nomer
        self.tombol_tambah.text = 'Perbarui Kontak'
        self.tombol_tambah.bind(on_press=lambda instance, c_id=c_id: self.perbarui_kontak(c_id))

    def perbarui_kontak(self, c_id):
        nama = self.input_nama.text
        nomer = self.input_nomer.text
        if nama and nomer:
            conn = sqlite3.connect('contacts.db')
            c = conn.cursor()
            c.execute('UPDATE contacts SET name = ?, phone = ? WHERE id = ?', (nama, nomer, c_id))
            conn.commit()
            conn.close()
            self.input_nama.text = ''
            self.input_nomer.text = ''
            self.tombol_tambah.text = 'Tambah Kontak'
            self.memuat_kontak()

    def hapus_kontak(self, c_id):
        conn = sqlite3.connect('contacts.db')
        c = conn.cursor()
        c.execute('DELETE FROM contacts WHERE id = ?', (c_id,))
        conn.commit()
        conn.close()
        self.memuat_kontak()

if __name__ == '__main__':
    AplikasiKontak().run()
