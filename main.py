# This is a simple Python program that prints "Hello World!" in Turkish.
# İlk ders

mesaj = "Merhaba Dünya!" #string variable
ders_notu = 85 #integer variable
kilom = 75.5 #float variable
ilk_ders_mi = True #boolean variable

#print(ilk_ders_mi)
#print(mesaj)
#print(ders_notu)
#print(kilom)

ilk_ders_mi = False #boolean variable
#print(ilk_ders_mi)


urun_adi = "Laptop" #string variable
urun_fiyati = 45000 #integer variable
urun_agirligi = 2.5 #float variable
urun_yeni_mi = 0 #boolean variable

if urun_yeni_mi:
    urun_durumu = "Ürün Yeni"
else:
    urun_durumu = "Ürün İkinci El"

print("Ürün Adı: " + urun_adi 
      + "\nÜrün Fiyatı: " + str(urun_fiyati) + " TL" 
      + "\nÜrün Ağırlığı: " + str(urun_agirligi) + " kg" 
      + "\nÜrün Durumu: " + urun_durumu)


#Ali Veli kişisinin yaşı ve kg ve cinsiyet (erkek_mi) değişkenlerini tanımlayalım ve ekrana yazdıralım.


kisi_adi = "Ali Veli" #string variable
kisi_yasi = 30 #integer variable
kisi_kilosu = 75.5 #float variable
kisi_erkek_mi = True #boolean variable

print(type(kisi_erkek_mi)) #boolean variable type

if kisi_erkek_mi:
    kisi_cinsiyeti = "Erkek"    
else:
    kisi_cinsiyeti = "Kadın"
    
    
print("Kişi Adı: " + kisi_adi
      + "\nKişi Yaşı: " + str(kisi_yasi)         
      + "\nKişi Kilosu: " + str(kisi_kilosu) + " kg"
      + "\nKişi Cinsiyeti: " + kisi_cinsiyeti)