#pythonda sözlük - dict ve obje veri tipleri ile ilgili örnekler
#keys ve values ve items kullanımı
ogrenciler = {
    "Ali": {"yas": 20, "bolum": "Bilgisayar Mühendisliği"},
    "Ayşe": {"yas": 22, "bolum": "Elektrik-Elektronik Mühendisliği"},
    "Mehmet": {"yas": 21, "bolum": "Makine Mühendisliği"}
}
#print(ogrenciler)  
#print(type(ogrenciler))  

#print(ogrenciler.keys())  
#print(ogrenciler.values())  # Sözlük'teki değerleri yazdırır
#print(ogrenciler.items())  # Sözlük'teki anahtar-değer çiftlerini yazdırır

#print(ogrenciler["Ali"])  # Ali'nin bilgilerini yazdırır    
#print(ogrenciler["Ali"]["yas"])  # Ali'nin yaşını yazdırır  
#print(ogrenciler["Ali"]["bolum"])  # Ali'nin bölümünü yazdırır

#ogrenciler["Ali"]["bolum"] = "Yazılım Mühendisliği"  # Ali'nin bölümünü günceller
#print(ogrenciler["Ali"]["bolum"])  # Ali'nin güncellenmiş bölümünü yazdırır
#print(ogrenciler)
#ogrenciler.update({"Ayşe": {"yas": 23, "bolum": "Bilgisayar Mühendisliği"}})  # Ayşe'nin bilgilerini günceller
#print(ogrenciler["Ayşe"])  # Ayşe'nin güncellenmiş bilgilerini yazdırır

#ogrenciler["Ali"]["hobi"] = ["yüzme", "kitap okuma"]  # Sözlük'e yeni bir anahtar-değer çifti ekler
#ogrenciler["Ayşe"]["hobi"] = ["yüzme", "kitap okuma"]  # Sözlük'e yeni bir anahtar-değer çifti ekler
#ogrenciler["Mehmet"]["hobi"] = ["yüzme", "kitap okuma"]  # Sözlük'e yeni bir anahtar-değer çifti ekler
#print(ogrenciler) # Sözlük'ü yazdırır   

#del ogrenciler["Mehmet"]["bolum"]  # Sözlük'ten bir anahtar-değer çiftini siler
#print(ogrenciler) # Sözlük'ü yazdırır

#for k in ogrenciler:
#    print(k)  # Sözlük'teki anahtarları yazdırır
    
#for k in ogrenciler.keys():
#    print(k)  # Sözlük'teki anahtarları yazdırır
    
#for v in ogrenciler.values():
#    print(v)  # Sözlük'teki değerleri yazdırır
    
#for k, v in ogrenciler.items():
#    print(k, ":", v)  # Sözlük'teki anahtar-değer çiftlerini yazdırır
    
ogrenciler = {
    "Ali": {"yas": 20, "bolum": "Bilgisayar Mühendisliği"},
    "Ayşe": {"yas": 22, "bolum": "Elektrik-Elektronik Mühendisliği"},
    "Mehmet": {"yas": 21, "bolum": "Makine Mühendisliği"}
}    
    
#print(ogrenciler["Veli"])  # Sözlük'teki bir anahtarın değerini yazdırır
print(ogrenciler.get("Veli"))
print(ogrenciler.get("Veli", "Veli Anahtar bulunamadı")) 
print(ogrenciler.get("Ali", "Anahtar bulunamadı"))  # Sözlük'teki bir anahtarın değerini yazdırır, anahtar yoksa varsayılan değeri döndürür    
    