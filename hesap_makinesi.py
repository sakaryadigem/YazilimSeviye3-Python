#basit bir hesap makinesi için arayüze sahip örnek bir python kodu
import tkinter as tk

def hesap_makinesi():
    pencere = tk.Tk()
    pencere.title("Hesap Makinesi")
    pencere.geometry("480x350")
    pencere.configure(bg="#1e1e2e")
    pencere.resizable(False, False)

    giris = tk.Entry(pencere, width=30, borderwidth=10, font=("Tahoma", 20)) # giriş alanı oluşturuluyor
    giris.grid(row=0, column=0, columnspan=4) # giriş alanı pencereye yerleştiriliyor

    # butonların işlevlerini tanımlayan fonksiyonlar
    def buton_tikla(deger):
        mevcut = giris.get()
        giris.delete(0, tk.END)
        giris.insert(0, mevcut + str(deger))

    def esit_tikla():
        try:
            islem = giris.get()
            # Sadece izin verilen karakterler
            izinli = set("0123456789+-*/.()% ")
            if not set(islem).issubset(izinli):
                hata = "Geçersiz karakterler içeriyor"
                raise ValueError("Geçersiz karakter")
            # Girdi uzunluğunu sınırla
            if len(islem) > 20:
                hata = "İfade çok uzun"
                raise ValueError("İfade çok uzun")

            # Üs operatörünü tamamen yasakla (opsiyonel)
            if "**" in islem:
                hata = "Üs operatörü desteklenmiyor"
                raise ValueError("Üs operatörü desteklenmiyor")
            
            sonuc = eval(islem, {"__builtins__": {}}, {})
            giris.delete(0, tk.END)
            giris.insert(0, str(sonuc))
        except:
            giris.delete(0, tk.END)
            giris.insert(0, "Hata" + " - " + hata)
            pencere.after(3000, temizle)

    def temizle():
        giris.delete(0, tk.END)

    butonlar = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('C', 4, 2), ('+', 4, 3)
    ]

    # butonları pencereye yerleştir
    for (text, row, col) in butonlar:
        if text == 'C':
            tk.Button(pencere, text=text, 
            font=("Tahoma", 12, "bold"),
            activebackground="#89b4fa",
            activeforeground="#1e1e2e",
            width=6, height=2,
            relief="flat", bd=0, bg="lightcoral", command=temizle).grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
        else:
            tk.Button(pencere, text=text, 
            font=("Tahoma", 12, "bold"),
            activebackground="#89b4fa",
            activeforeground="#1e1e2e",
            width=6, height=2,
            relief="flat", bd=0, bg="lightgray", command=lambda t=text: buton_tikla(t)).grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    # eşittir butonu ekle
    tk.Button(pencere, text="=",     
            font=("Tahoma", 12, "bold"),
            activebackground="#89b4fa",
            activeforeground="#1e1e2e",
            width=6, height=2,
            relief="flat", bd=0, bg="lightgreen", 
            command=esit_tikla).grid(row=5, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
    # pencereyi çalıştır
    pencere.mainloop()
    
    
# hesap makinesi fonksiyonunu çağır
hesap_makinesi()