import tkinter as tk
from tkinter import messagebox

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def ekle(self, urun):
        yeni_node = Node(urun)
        if not self.head:
            self.head = yeni_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = yeni_node

    def __iter__(self):
        current = self.head
        while current:
            yield current
            current = current.next

class Urun:
    def __init__(self, ad, bedenler, max_adet, fiyat):
        self.ad = ad
        self.bedenler = bedenler
        self.max_adet = max_adet
        self.fiyat = fiyat

    def __str__(self):
        return self.ad

class Siparis:
    def __init__(self, urun, adet, toplam_tutar):
        self.urun = urun
        self.adet = adet
        self.toplam_tutar = toplam_tutar

class GirisEkrani:
    def __init__(self, root):
        self.root = root
        self.root.title("Giriş Ekranı")

        # Pencere boyutunu ayarla
        self.root.geometry("350x300+500+200")

        self.label_kullanici_adi = tk.Label(root, text="Kullanıcı Adı:")
        self.label_sifre = tk.Label(root, text="Şifre:")

        self.entry_kullanici_adi = tk.Entry(root)
        self.entry_sifre = tk.Entry(root, show="*")  # Şifre alanını gizlemek için

        self.button_giris = tk.Button(root, text="Giriş Yap", command=self.giris_kontrol)

        self.label_kullanici_adi.grid(row=0, column=0, padx=10, pady=10)
        self.label_sifre.grid(row=1, column=0, padx=10, pady=10)
        self.entry_kullanici_adi.grid(row=0, column=1, padx=10, pady=10)
        self.entry_sifre.grid(row=1, column=1, padx=10, pady=10)
        self.button_giris.grid(row=2, column=0, columnspan=2, pady=10)

        # Ürünleri linked list'e ekleyelim
        self.linked_list = LinkedList()
        self.linked_list.ekle(Urun("T-Shirt",      ["S", "M", "L", "XL"],          5, 1700.0))
        self.linked_list.ekle(Urun("Sweatshirt",   ["S", "M", "L", "XL"],          5, 4000.0))
        self.linked_list.ekle(Urun("Kazak",        ["S", "M", "L", "XL"],          5, 3500.0))
        self.linked_list.ekle(Urun("Gömlek",       ["S", "M", "L", "XL"],          5, 4000.0))
        self.linked_list.ekle(Urun("Hırka",        ["S", "M", "L", "XL"],          5, 3500.0))
        self.linked_list.ekle(Urun("Polar",        ["S", "M", "L", "XL"],          5, 3500.0))
        self.linked_list.ekle(Urun("Deri Ceket",   ["S", "M", "L", "XL"],          5, 10000.0))
        self.linked_list.ekle(Urun("Kot Ceket",    ["S", "M", "L", "XL"],          5, 8000.0))
        self.linked_list.ekle(Urun("Mont",         ["S", "M", "L", "XL"],          5, 12000.0))
        self.linked_list.ekle(Urun("Pantolon",     ["28", "30", "32", "34", "36"], 5, 7000.0))
        self.linked_list.ekle(Urun("Eşofman Altı", ["28", "30", "32", "34", "36"], 5, 5500.0))
        self.linked_list.ekle(Urun("Kot Şort",     ["28", "30", "32", "34", "36"], 5, 5000.0))


    def giris_kontrol(self):
        kullanici_adi = self.entry_kullanici_adi.get()
        sifre = self.entry_sifre.get()

        if kullanici_adi == "berkay" and sifre == "taha":
            self.root.withdraw()  # Giriş ekranını gizle
            self.acilis_ekrani()
        else:
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre.")

    def acilis_ekrani(self):
        acilis_penceresi = tk.Toplevel(self.root)
        uygulama = AcilisEkrani(acilis_penceresi, self.linked_list)
        acilis_penceresi.mainloop()

class AcilisEkrani:
    def __init__(self, root, linked_list):
        self.root = root
        self.root.title("Sipariş Ekranı")
        self.linked_list = linked_list  # linked_list parametresini al ve sınıf içinde sakla

        # Pencere boyutunu ayarla
        self.root.geometry("500x400+500+200")

        self.label_acilis = tk.Label(root, text="Hoş Geldiniz!")
        self.label_acilis.pack(padx=10, pady=10)

        # Ürünleri linked list'ten alarak yazdır
        self.listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, height=10, width=40)
        self.listbox.pack(pady=10)

        for node in linked_list:
            self.listbox.insert(tk.END, str(node.data))

        self.button_devam_et = tk.Button(root, text="Devam Et", command=self.devam_et)
        self.button_devam_et.pack(pady=10)
        self.sepet = []
        self.toplam_tutar = 0

    def devam_et(self):
        selected_items = [self.listbox.get(idx) for idx in self.listbox.curselection()]
        if not selected_items:
            messagebox.showerror("Hata", "Lütfen en az bir ürün seçiniz.")
        else:
            self.secenekleri_sor(selected_items)

    def secenekleri_sor(self, selected_items):
        secilen_urunler = []
        for item in selected_items:
            urun = next(node.data for node in self.linked_list if str(node.data) == item)
            beden_secimi, adet_secimi = self.beden_ve_adet_secimi(urun)
            secilen_urunler.append((urun, beden_secimi, adet_secimi))

        self.sepete_ekle(secilen_urunler)

    def beden_ve_adet_secimi(self, urun):
        beden_sor = tk.Toplevel(self.root)
        beden_sor.title(f"{urun.ad} Beden ve Adet Seçimi")

        # Pencere boyutunu ve konumunu ayarla
        beden_sor.geometry("400x300+500+200")

        label_beden = tk.Label(beden_sor, text=f"{urun.ad} için beden seçiniz:")
        label_beden.pack(pady=5)

        var_beden = tk.StringVar(beden_sor)
        var_beden.set(urun.bedenler[0])  # Varsayılan olarak ilk bedeni seç

        dropdown_beden = tk.OptionMenu(beden_sor, var_beden, *urun.bedenler)
        dropdown_beden.pack(pady=5)

        label_adet = tk.Label(beden_sor, text="Adet seçiniz:")
        label_adet.pack(pady=5)

        var_adet = tk.IntVar(beden_sor)
        var_adet.set(1)  # Varsayılan olarak 1 adet seç

        spinbox_adet = tk.Spinbox(beden_sor, from_=1, to=urun.max_adet, textvariable=var_adet)
        spinbox_adet.pack(pady=5)

        button_devam_et = tk.Button(beden_sor, text="Sepete Ekle", command=lambda: self.devam_et_beden_adet(var_adet, urun, beden_sor))
        button_devam_et.pack(pady=10)

        beden_sor.wait_window()

        return var_beden.get(), var_adet.get()

    def devam_et_beden_adet(self, var_adet, urun, beden_sor):
        girilen_adet = var_adet.get()
        if girilen_adet < 1 or girilen_adet > urun.max_adet:
            messagebox.showerror("Hata", f"Lütfen geçerli bir adet giriniz (1 ile {urun.max_adet} arasında).")
        else:
            beden_sor.destroy()
            self.sepete_ekle([(urun, girilen_adet)])

    def sepete_ekle(self, secilen_urunler):
        for secilen_urun in secilen_urunler:
            urun, beden_secimi, adet_secimi = secilen_urun
            self.sepet.append((urun, adet_secimi))
            self.toplam_tutar += urun.fiyat * adet_secimi

        self.sepet_penceresini_goster()

    def sepet_penceresini_goster(self):
        sepet_penceresi = tk.Toplevel(self.root)
        sepet_penceresi.title("Sepetim")

        # Pencere boyutunu ve konumunu ayarla
        sepet_penceresi.geometry("500x400+500+200")

        label_sepet = tk.Label(sepet_penceresi, text="Sepetiniz:")
        label_sepet.pack(pady=10)

        listbox_sepet = tk.Listbox(sepet_penceresi, selectmode=tk.MULTIPLE, height=10, width=40)
        listbox_sepet.pack(pady=10)

        for urun, adet in self.sepet:
            listbox_sepet.insert(tk.END, f"{urun.ad} - Beden: {urun.bedenler[0]} - Adet: {adet}")

        label_toplam_tutar = tk.Label(sepet_penceresi, text=f"Toplam Tutar: {self.toplam_tutar} TL")
        label_toplam_tutar.pack(pady=10)

        button_cikar = tk.Button(sepet_penceresi, text="Ürünü Çıkar", command=lambda: self.urun_cikar(listbox_sepet, label_toplam_tutar))
        button_cikar.pack(pady=10)

        button_onayla = tk.Button(sepet_penceresi, text="Sepeti Onayla", command=lambda: self.sepeti_onayla(sepet_penceresi))
        button_onayla.pack(pady=10)

    def urun_cikar(self, listbox_sepet, label_toplam_tutar):
        selected_items = listbox_sepet.curselection()
        if not selected_items:
            messagebox.showerror("Hata", "Lütfen en az bir ürün seçiniz.")
        else:
            for index in reversed(selected_items):
                urun, adet = self.sepet.pop(index)
                self.toplam_tutar -= urun.fiyat * adet

            listbox_sepet.delete(0, tk.END)
            for urun, adet in self.sepet:
                listbox_sepet.insert(tk.END, f"{urun.ad} - Beden: {urun.bedenler[0]} - Adet: {adet}")

            label_toplam_tutar.config(text=f"Toplam Tutar: {self.toplam_tutar} TL")

    def sepeti_onayla(self, sepet_penceresi):
        if not self.sepet:
            messagebox.showinfo("Uyarı", "Sepetiniz boş. "
                                         "Sepeti onaylamanız için sepette ürün olmalıdır ")
        else:
            # Siparişi onayladıktan sonra sepeti sıfırla
            siparisler = [Siparis(urun, adet, urun.fiyat * adet) for urun, adet in self.sepet]
            self.sepet = []
            self.toplam_tutar = 0

            # Siparişleri gösteren pencereyi aç
            siparislerim_penceresi = tk.Toplevel(self.root)
            uygulama = SiparislerimEkrani(siparislerim_penceresi, siparisler)
            siparislerim_penceresi.protocol("WM_DELETE_WINDOW",
                                            lambda: self.siparislerim_penceresi_kapat(siparislerim_penceresi))
            sepet_penceresi.destroy()

            # Sipariş alındı mesajını göster
            messagebox.showinfo("Sipariş Alındı", "Siparişiniz alınmıştır. Teşekkür ederiz!")

    def siparislerim_penceresi_kapat(self, siparislerim_penceresi):
        siparislerim_penceresi.destroy()
        self.sepet_penceresini_goster()

class SiparislerimEkrani:
    def __init__(self, root, siparisler):
        self.root = root
        self.root.title("Siparişim")

        # Pencere boyutunu ayarla
        self.root.geometry("500x400+500+200")

        self.siparisler = siparisler

        # Ürünleri linked list'ten alarak yazdır
        self.listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=10, width=40)
        self.listbox.pack(pady=10)

        for siparis in siparisler:
            self.listbox.insert(tk.END, f"{siparis.urun.ad} - Adet: {siparis.adet} - Tutar: {siparis.toplam_tutar} TL")

        self.button_iptal_et = tk.Button(root, text="İptal Et", command=self.siparisi_iptal_et)
        self.button_iptal_et.pack(pady=10)
        self.button_devam = tk.Button(root, text="Tamam", command=self.devam_et)
        self.button_devam.pack(pady=10)

    def siparisi_iptal_et(self):
        selected_index = self.listbox.curselection()
        if not selected_index:
            messagebox.showerror("Hata", "Lütfen iptal etmek istediğiniz siparişi seçiniz.")
        else:
            selected_siparis = self.siparisler.pop(selected_index[0])
            messagebox.showinfo("Onay", f"{selected_siparis.urun.ad} siparişiniz iptal edilmiştir.")
            # Listbox'ı güncelle
            self.listbox.delete(0, tk.END)
            for siparis in self.siparisler:
                self.listbox.insert(tk.END, f"{siparis.urun.ad} - Adet: {siparis.adet} - Tutar: {siparis.toplam_tutar} TL")

    def devam_et(self):
        self.root.destroy()
        # pencereyi kapatmak için

if __name__ == "__main__":
    root = tk.Tk()
    giris_ekrani = GirisEkrani(root)
    root.mainloop()
