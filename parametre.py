#parametre almak için örnek güzel görünümlü python kodu yazma

print("="*32)
print("="*32)
print("Parametreli Python Kodu Örneği")
print("="*32)
print("="*32)

print("1. Selamla")
print("2. Toplama Yap")   
print("3. Çarpma Yap")
print("4. Çıkarma Yap")
print("5. Çıkış")

while True:
    secim = input("Seçiminizi yapınız (1-5): ")
    if secim == "1":
        isim = input("İsminizi giriniz: ")
        print(f"Merhaba, {isim}!")
    elif secim == "2":
        sayi1 = float(input("Birinci sayıyı giriniz: "))
        sayi2 = float(input("İkinci sayıyı giriniz: "))
        print(f"Toplam: {sayi1 + sayi2}")
    elif secim == "3":
        sayi1 = float(input("Birinci sayıyı giriniz: "))
        sayi2 = float(input("İkinci sayıyı giriniz: "))
        print(f"Çarpım: {sayi1 * sayi2}")
    elif secim == "4":
        sayi1 = float(input("Birinci sayıyı giriniz: "))
        sayi2 = float(input("İkinci sayıyı giriniz: "))
        print(f"Fark: {sayi1 - sayi2}")
    elif secim == "5":
        print("Çıkış yapılıyor...")
        break
    else:
        print("Geçersiz seçim. Lütfen tekrar deneyin.")
