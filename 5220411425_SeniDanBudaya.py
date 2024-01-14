import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import mysql.connector

# Koneksi ke MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="5220411425"
)

mycursor = mydb.cursor()

# Buat tabel jika belum ada
mycursor.execute("CREATE TABLE IF NOT EXISTS seni (id INT AUTO_INCREMENT PRIMARY KEY, nama VARCHAR(255), jenis VARCHAR(255), tahun_pembuatan INT)")
mycursor.execute("CREATE TABLE IF NOT EXISTS lukisan (id INT AUTO_INCREMENT PRIMARY KEY, teknik VARCHAR(255), gaya VARCHAR(255), seni_id INT, FOREIGN KEY (seni_id) REFERENCES seni(id))")
mycursor.execute("CREATE TABLE IF NOT EXISTS tarian (id INT AUTO_INCREMENT PRIMARY KEY, gerakan VARCHAR(255), asal VARCHAR(255), seni_id INT, FOREIGN KEY (seni_id) REFERENCES seni(id))")
mycursor.execute("CREATE TABLE IF NOT EXISTS lukisan_modern (id INT AUTO_INCREMENT PRIMARY KEY, media VARCHAR(255), tema VARCHAR(255), seni_id INT, FOREIGN KEY (seni_id) REFERENCES seni(id))")


class SeniDanBudaya:
    def __init__(self, nama, jenis, tahun_pembuatan):
        self._nama = nama
        self._jenis = jenis
        self._tahun_pembuatan = tahun_pembuatan  # Akses modifier protected

    def get_nama(self):
        return self._nama

    def get_jenis(self):
        return self._jenis

    def get_tahun_pembuatan(self):
        return self._tahun_pembuatan

    def hitung_umur(self):
        tahun_sekarang = datetime.now().year
        return tahun_sekarang - self._tahun_pembuatan

    def deskripsi(self):
        return (f"Sebuah karya seni dan budaya {self._jenis} dengan nama '{self._nama}'.\n"
                f"Tahun Pembuatan: {self._tahun_pembuatan}\n"
                f"Umur: {self.hitung_umur()} tahun\n")


class Lukisan(SeniDanBudaya):
    def __init__(self, nama, teknik, gaya, tahun_pembuatan):
        super().__init__(nama, "Lukisan", tahun_pembuatan)
        self.__teknik = teknik  # Akses modifier private
        self.gaya = gaya

    def get_teknik(self):
        return self.__teknik

    def deskripsi_lukisan(self):
        return (super().deskripsi() +
                f"Lukisan '{self._nama}' menggunakan teknik {self.__teknik} dengan gaya {self.gaya}.\n")


class Tarian(SeniDanBudaya):
    def __init__(self, nama, gerakan, asal, tahun_pembuatan):
        super().__init__(nama, "Tarian", tahun_pembuatan)
        self.gerakan = gerakan
        self.__asal = asal  # Akses modifier private

    def get_asal(self):
        return self.__asal

    def deskripsi_tarian(self):
        return (super().deskripsi() +
                f"Tarian '{self._nama}' berasal dari {self.__asal} dengan gerakan khas {self.gerakan}.\n")


class LukisanModern(Lukisan):
    def __init__(self, nama, teknik, gaya, tahun_pembuatan, media, tema):
        super().__init__(nama, teknik, gaya, tahun_pembuatan)
        self.media = media
        self.tema = tema

    def deskripsi_lukisan_modern(self):
        return (super().deskripsi_lukisan() +
                f"Medium Lukisan: {self.media}\n"
                f"Tema Lukisan Modern: {self.tema}\n")


# Contoh penggunaan program
def input_lukisan():
    nama = input("Masukkan nama lukisan: ")
    teknik = input("Masukkan teknik lukisan: ")
    gaya = input("Masukkan gaya lukisan: ")
    tahun_pembuatan = int(input("Masukkan tahun pembuatan lukisan: "))
    return Lukisan(nama, teknik, gaya, tahun_pembuatan)


def input_tarian():
    nama = input("Masukkan nama tarian: ")
    gerakan = input("Masukkan gerakan tarian: ")
    asal = input("Masukkan asal tarian: ")
    tahun_pembuatan = int(input("Masukkan tahun pembuatan tarian: "))
    return Tarian(nama, gerakan, asal, tahun_pembuatan)


def input_lukisan_modern():
    lukisan = input_lukisan()
    media = input("Masukkan media lukisan modern: ")
    tema = input("Masukkan tema lukisan modern: ")
    return LukisanModern(lukisan.get_nama(), lukisan.get_teknik(), lukisan.gaya, lukisan.get_tahun_pembuatan(), media, tema)


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("Aplikasi Seni dan Budaya")

        self.current_frame = None  # Frame yang sedang ditampilkan
        self.data_lukisan = []
        self.data_tarian = []
        self.data_lukisan_modern = []

        self.show_main_menu()

    def execute_query(self, query, values=None):
        try:
            mycursor.execute(query, values)
            mydb.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def show_main_menu(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Menu:").pack(pady=10)

        tk.Button(self.current_frame, text="Input Data Lukisan", command=self.show_input_lukisan).pack(pady=5)
        tk.Button(self.current_frame, text="Input Data Tarian", command=self.show_input_tarian).pack(pady=5)
        tk.Button(self.current_frame, text="Input Data Lukisan Modern", command=self.show_input_lukisan_modern).pack(pady=5)
        tk.Button(self.current_frame, text="Tampilkan Informasi Lukisan", command=self.tampilkan_lukisan).pack(pady=5)
        tk.Button(self.current_frame, text="Tampilkan Informasi Tarian", command=self.tampilkan_tarian).pack(pady=5)
        tk.Button(self.current_frame, text="Tampilkan Informasi Lukisan Modern", command=self.tampilkan_lukisan_modern).pack(pady=5)
        tk.Button(self.current_frame, text="Keluar", command=self.master.destroy).pack(pady=10)

    def show_input_lukisan(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Input Data Lukisan").pack(pady=10)

        tk.Label(self.current_frame, text="Nama:").pack()
        self.nama_entry = tk.Entry(self.current_frame)
        self.nama_entry.pack()

        tk.Label(self.current_frame, text="Teknik:").pack()
        self.teknik_entry = tk.Entry(self.current_frame)
        self.teknik_entry.pack()

        tk.Label(self.current_frame, text="Gaya:").pack()
        self.gaya_entry = tk.Entry(self.current_frame)
        self.gaya_entry.pack()

        tk.Label(self.current_frame, text="Tahun Pembuatan:").pack()
        self.tahun_pembuatan_entry = tk.Entry(self.current_frame)
        self.tahun_pembuatan_entry.pack()

        tk.Button(self.current_frame, text="Submit", command=self.submit_lukisan).pack(pady=10)
        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def submit_lukisan(self):
        nama = self.nama_entry.get()
        teknik = self.teknik_entry.get()
        gaya = self.gaya_entry.get()
        tahun_pembuatan = int(self.tahun_pembuatan_entry.get())

        # Simpan data ke dalam database
        query_seni = "INSERT INTO seni (nama, jenis, tahun_pembuatan) VALUES (%s, %s, %s)"
        values_seni = (nama, "Lukisan", tahun_pembuatan)
        self.execute_query(query_seni, values_seni)

        seni_id = mycursor.lastrowid  # Dapatkan ID dari data seni yang baru saja dimasukkan

        query_lukisan = "INSERT INTO lukisan (teknik, gaya, seni_id) VALUES (%s, %s, %s)"
        values_lukisan = (teknik, gaya, seni_id)
        self.execute_query(query_lukisan, values_lukisan)

        messagebox.showinfo("Info", "Data Lukisan berhasil diinput.")

        # Kembali ke menu utama setelah input data
        self.show_main_menu()

    def show_input_tarian(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Input Data Tarian").pack(pady=10)

        tk.Label(self.current_frame, text="Nama:").pack()
        self.nama_entry = tk.Entry(self.current_frame)
        self.nama_entry.pack()

        tk.Label(self.current_frame, text="Gerakan:").pack()
        self.gerakan_entry = tk.Entry(self.current_frame)
        self.gerakan_entry.pack()

        tk.Label(self.current_frame, text="Asal:").pack()
        self.asal_entry = tk.Entry(self.current_frame)
        self.asal_entry.pack()

        tk.Label(self.current_frame, text="Tahun Pembuatan:").pack()
        self.tahun_pembuatan_entry = tk.Entry(self.current_frame)
        self.tahun_pembuatan_entry.pack()

        tk.Button(self.current_frame, text="Submit", command=self.submit_tarian).pack(pady=10)
        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def submit_tarian(self):
        nama = self.nama_entry.get()
        gerakan = self.gerakan_entry.get()
        asal = self.asal_entry.get()
        tahun_pembuatan = int(self.tahun_pembuatan_entry.get())

        # Simpan data ke dalam database
        query_seni = "INSERT INTO seni (nama, jenis, tahun_pembuatan) VALUES (%s, %s, %s)"
        values_seni = (nama, "Tarian", tahun_pembuatan)
        self.execute_query(query_seni, values_seni)

        seni_id = mycursor.lastrowid  # Dapatkan ID dari data seni yang baru saja dimasukkan

        query_tarian = "INSERT INTO tarian (gerakan, asal, seni_id) VALUES (%s, %s, %s)"
        values_tarian = (gerakan, asal, seni_id)
        self.execute_query(query_tarian, values_tarian)

        messagebox.showinfo("Info", "Data Tarian berhasil diinput.")

        # Kembali ke menu utama setelah input data
        self.show_main_menu()

    def show_input_lukisan_modern(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Input Data Lukisan Modern").pack(pady=10)

        tk.Label(self.current_frame, text="Nama:").pack()
        self.nama_entry = tk.Entry(self.current_frame)
        self.nama_entry.pack()

        tk.Label(self.current_frame, text="Teknik:").pack()
        self.teknik_entry = tk.Entry(self.current_frame)
        self.teknik_entry.pack()

        tk.Label(self.current_frame, text="Gaya:").pack()
        self.gaya_entry = tk.Entry(self.current_frame)
        self.gaya_entry.pack()

        tk.Label(self.current_frame, text="Tahun Pembuatan:").pack()
        self.tahun_pembuatan_entry = tk.Entry(self.current_frame)
        self.tahun_pembuatan_entry.pack()

        tk.Label(self.current_frame, text="Media:").pack()
        self.media_entry = tk.Entry(self.current_frame)
        self.media_entry.pack()

        tk.Label(self.current_frame, text="Tema:").pack()
        self.tema_entry = tk.Entry(self.current_frame)
        self.tema_entry.pack()

        tk.Button(self.current_frame, text="Submit", command=self.submit_lukisan_modern).pack(pady=10)
        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def submit_lukisan_modern(self):
        nama = self.nama_entry.get()
        teknik = self.teknik_entry.get()
        gaya = self.gaya_entry.get()
        tahun_pembuatan = int(self.tahun_pembuatan_entry.get())
        media = self.media_entry.get()
        tema = self.tema_entry.get()

        # Simpan data ke dalam database
        query_seni = "INSERT INTO seni (nama, jenis, tahun_pembuatan) VALUES (%s, %s, %s)"
        values_seni = (nama, "Lukisan Modern", tahun_pembuatan)
        self.execute_query(query_seni, values_seni)

        seni_id = mycursor.lastrowid  # Dapatkan ID dari data seni yang baru saja dimasukkan

        query_lukisan_modern = "INSERT INTO lukisan_modern (media, tema, seni_id) VALUES (%s, %s, %s)"
        values_lukisan_modern = (media, tema, seni_id)
        self.execute_query(query_lukisan_modern, values_lukisan_modern)

        messagebox.showinfo("Info", "Data Lukisan Modern berhasil diinput.")

        # Kembali ke menu utama setelah input data
        self.show_main_menu()

    def tampilkan_lukisan(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Informasi Lukisan").pack(pady=10)

        # Tampilkan data lukisan dari database
        query = "SELECT seni.nama, seni.jenis, seni.tahun_pembuatan, lukisan.teknik, lukisan.gaya FROM seni JOIN lukisan ON seni.id = lukisan.seni_id"
        mycursor.execute(query)
        lukisan_data = mycursor.fetchall()

        for data in lukisan_data:
            lukisan_info = f"Nama: {data[0]}\nJenis: {data[1]}\nTahun Pembuatan: {data[2]}\nTeknik: {data[3]}\nGaya: {data[4]}\n"
            tk.Label(self.current_frame, text=lukisan_info).pack()

        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def tampilkan_tarian(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Informasi Tarian").pack(pady=10)

        # Tampilkan data tarian dari database
        query = "SELECT seni.nama, seni.jenis, seni.tahun_pembuatan, tarian.gerakan, tarian.asal FROM seni JOIN tarian ON seni.id = tarian.seni_id"
        mycursor.execute(query)
        tarian_data = mycursor.fetchall()

        for data in tarian_data:
            tarian_info = f"Nama: {data[0]}\nJenis: {data[1]}\nTahun Pembuatan: {data[2]}\nGerakan: {data[3]}\nAsal: {data[4]}\n"
            tk.Label(self.current_frame, text=tarian_info).pack()

        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def tampilkan_lukisan_modern(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Informasi Lukisan Modern").pack(pady=10)

        # Tampilkan data lukisan modern dari database
        query = "SELECT seni.nama, seni.jenis, seni.tahun_pembuatan, lukisan.teknik, lukisan.gaya, lukisan_modern.media, lukisan_modern.tema FROM seni JOIN lukisan ON seni.id = lukisan.seni_id JOIN lukisan_modern ON seni.id = lukisan_modern.seni_id"
        mycursor.execute(query)
        lukisan_modern_data = mycursor.fetchall()

        for data in lukisan_modern_data:
            lukisan_modern_info = f"Nama: {data[0]}\nJenis: {data[1]}\nTahun Pembuatan: {data[2]}\nTeknik: {data[3]}\nGaya: {data[4]}\nMedia: {data[5]}\nTema: {data[6]}\n"
            tk.Label(self.current_frame, text=lukisan_modern_info).pack()

        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()
    def update_data(self, table, data_id, field, new_value):
        query = f"UPDATE {table} SET {field} = %s WHERE id = %s"
        values = (new_value, data_id)
        self.execute_query(query, values)

    def delete_data(self, table, data_id):
        query = f"DELETE FROM {table} WHERE seni_id = %s"
        values = (data_id,)
        self.execute_query(query, values)

    def delete_data_seni(self, table, data_id):
        query = f"DELETE FROM seni WHERE id = %s"
        values = (data_id,)
        self.execute_query(query, values)

    def show_update_lukisan(self, data_type, data_id):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text=f"Update Data {data_type}").pack(pady=10)


        tk.Label(self.current_frame, text=f"teknik:").pack()
        teknik = tk.Entry(self.current_frame)
        teknik.pack()
        tk.Label(self.current_frame, text=f"gaya:").pack()
        gaya= tk.Entry(self.current_frame)
        gaya.pack()
        tk.Label(self.current_frame, text=f"nama:").pack()
        nama= tk.Entry(self.current_frame)
        nama.pack()
        tk.Label(self.current_frame, text=f"tahun pembuatan:").pack()
        tahun = tk.Entry(self.current_frame)
        tahun.pack()

        tk.Button(self.current_frame, text="Update", command=lambda: self.update_data_lukisan(data_type, data_id, teknik.get(), gaya.get(), nama.get(), tahun.get())).pack(pady=10)

        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def update_data_lukisan(self, data_type, id,teknik,gaya,nama,tahun):
        new ="seni" 
        field1 = "teknik"
        field2 = "gaya"
        field3 = "nama"
        field4 = "jenis"
        field5 = "tahun_pembuatan"

        # Update data in the database
        self.update_data(data_type.lower(), id, field1, teknik)
        self.update_data(data_type.lower(), id, field2, gaya)
        self.update_data(new.lower(), id, field3, nama)
        self.update_data(new.lower(), id, field4, data_type)
        self.update_data(new.lower(), id, field5, tahun)
        messagebox.showinfo("Info", f"Data {data_type} berhasil diupdate.")

        # Show the main menu after updating data
        self.show_main_menu()
    def show_update_tari(self, data_type, data_id):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text=f"Update Data {data_type}").pack(pady=10)

       
        tk.Label(self.current_frame, text=f"gerakan:").pack()
        teknik = tk.Entry(self.current_frame)
        teknik.pack()
        tk.Label(self.current_frame, text=f"asal:").pack()
        gaya= tk.Entry(self.current_frame)
        gaya.pack()
        tk.Label(self.current_frame, text=f"nama:").pack()
        nama= tk.Entry(self.current_frame)
        nama.pack()
        tk.Label(self.current_frame, text=f"tahun pembuatan:").pack()
        tahun = tk.Entry(self.current_frame)
        tahun.pack()

        tk.Button(self.current_frame, text="Update", command=lambda: self.update_data_tari(data_type, data_id, teknik.get(), gaya.get(), nama.get(), tahun.get())).pack(pady=10)

        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def update_data_tari(self, data_type, id,teknik,gaya,nama,tahun):
        new ="seni" 
        field1 = "gerakan"
        field2 = "asal"
        field3 = "nama"
        field4 = "jenis"
        field5 = "tahun_pembuatan"

        # Update data in the database
        self.update_data(data_type.lower(), id, field1, teknik)
        self.update_data(data_type.lower(), id, field2, gaya)
        self.update_data(new.lower(), id, field3, nama)
        self.update_data(new.lower(), id, field4, data_type)
        self.update_data(new.lower(), id, field5, tahun)
        messagebox.showinfo("Info", f"Data {data_type} berhasil diupdate.")

        # Show the main menu after updating data
        self.show_main_menu()
    def show_update_modern(self, data_type, data_id):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text=f"Update Data {data_type}").pack(pady=10)

       
        tk.Label(self.current_frame, text=f"media:").pack()
        teknik = tk.Entry(self.current_frame)
        teknik.pack()
        tk.Label(self.current_frame, text=f"tema:").pack()
        gaya= tk.Entry(self.current_frame)
        gaya.pack()
        tk.Label(self.current_frame, text=f"nama:").pack()
        nama= tk.Entry(self.current_frame)
        nama.pack()
        tk.Label(self.current_frame, text=f"tahun pembuatan:").pack()
        tahun = tk.Entry(self.current_frame)
        tahun.pack()

        tk.Button(self.current_frame, text="Update", command=lambda: self.update_data_modern(data_type, data_id, teknik.get(), gaya.get(), nama.get(), tahun.get())).pack(pady=10)

        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def update_data_modern(self, data_type, id,teknik,gaya,nama,tahun):
        new ="seni" 
        field1 = "media"
        field2 = "tema"
        field3 = "nama"
        field4 = "jenis"
        field5 = "tahun_pembuatan"

        # Update data in the database
        self.update_data(data_type.lower(), id, field1, teknik)
        self.update_data(data_type.lower(), id, field2, gaya)
        self.update_data(new.lower(), id, field3, nama)
        self.update_data(new.lower(), id, field4, data_type)
        self.update_data(new.lower(), id, field5, tahun)
        messagebox.showinfo("Info", f"Data {data_type} berhasil diupdate.")

        # Show the main menu after updating data
        self.show_main_menu()

    def show_delete_menu(self, data_type, data_id):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text=f"Delete Data {data_type}").pack(pady=10)

        tk.Button(self.current_frame, text="Delete", command=lambda: self.delete_data_menu(data_type, data_id)).pack(pady=10)
        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def delete_data_menu(self, data_type, data_id):
        # Delete data from the database
        self.delete_data(data_type.lower(), data_id)
        self.delete_data_seni(data_type.lower(), data_id)
        messagebox.showinfo("Info", f"Data {data_type} berhasil dihapus.")

        # Show the main menu after deleting data
        self.show_main_menu()

    def tampilkan_lukisan(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Informasi Lukisan").pack(pady=10)

        # Tampilkan data lukisan dari database
        query = "SELECT seni.id, seni.nama, seni.jenis, seni.tahun_pembuatan, lukisan.teknik, lukisan.gaya FROM seni JOIN lukisan ON seni.id = lukisan.seni_id"
        mycursor.execute(query)
        lukisan_data = mycursor.fetchall()

        for data in lukisan_data:
            lukisan_info = f"ID: {data[0]}\nNama: {data[1]}\nJenis: {data[2]}\nTahun Pembuatan: {data[3]}\nTeknik: {data[4]}\nGaya: {data[5]}\n"
            tk.Label(self.current_frame, text=lukisan_info).pack()
            
            # Add Update and Delete Buttons for each Lukisan
            update_button = tk.Button(self.current_frame, text="Update", command=lambda data_id=data[0]: self.show_update_lukisan("Lukisan", data_id))
            update_button.pack()
            
            delete_button = tk.Button(self.current_frame, text="Delete", command=lambda data_id=data[0]: self.show_delete_menu("Lukisan", data_id))
            delete_button.pack()

        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def tampilkan_tarian(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Informasi Tarian").pack(pady=10)

        # Tampilkan data tarian dari database
        query = "SELECT seni.id, seni.nama, seni.jenis, seni.tahun_pembuatan, tarian.gerakan, tarian.asal FROM seni JOIN tarian ON seni.id = tarian.seni_id"
        mycursor.execute(query)
        tarian_data = mycursor.fetchall()

        for data in tarian_data:
            tarian_info = f"ID: {data[0]}\nNama: {data[1]}\nJenis: {data[2]}\nTahun Pembuatan: {data[3]}\nGerakan: {data[4]}\nAsal: {data[5]}\n"
            tk.Label(self.current_frame, text=tarian_info).pack()
            
            # Add Update and Delete Buttons for each Tarian
            update_button = tk.Button(self.current_frame, text="Update", command=lambda data_id=data[0]: self.show_update_tari("Tarian", data_id))
            update_button.pack()
            
            delete_button = tk.Button(self.current_frame, text="Delete", command=lambda data_id=data[0]: self.show_delete_menu("Tarian", data_id))
            delete_button.pack()

        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()

    def tampilkan_lukisan_modern(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.master)
        self.current_frame.pack()

        tk.Label(self.current_frame, text="Informasi Lukisan Modern").pack(pady=10)

        # Tampilkan data lukisan modern dari database
        query = "SELECT seni.id, seni.nama, seni.jenis, seni.tahun_pembuatan, lukisan.teknik, lukisan.gaya, lukisan_modern.media, lukisan_modern.tema FROM seni JOIN lukisan ON seni.id = lukisan.seni_id JOIN lukisan_modern ON seni.id = lukisan_modern.seni_id"
        mycursor.execute(query)
        lukisan_modern_data = mycursor.fetchall()

        for data in lukisan_modern_data:
            lukisan_modern_info = f"ID: {data[0]}\nNama: {data[1]}\nJenis: {data[2]}\nTahun Pembuatan: {data[3]}\nTeknik: {data[4]}\nGaya: {data[5]}\nMedia: {data[6]}\nTema: {data[7]}\n"
            tk.Label(self.current_frame, text=lukisan_modern_info).pack()
            
            # Add Update and Delete Buttons for each Lukisan Modern
            update_button = tk.Button(self.current_frame, text="Update", command=lambda data_id=data[0]: self.show_update_modern("Lukisan Modern", data_id))
            update_button.pack()
            
            delete_button = tk.Button(self.current_frame, text="Delete", command=lambda data_id=data[0]: self.show_delete_menu("Lukisan Modern", data_id))
            delete_button.pack()

        tk.Button(self.current_frame, text="Kembali ke Menu Utama", command=self.show_main_menu).pack()




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


       
