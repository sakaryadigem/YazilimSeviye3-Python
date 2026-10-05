#fonksiyon kullanım örneği içeren python kodu
import random
import string

print("="*32)
print("Fonksiyon Kullanım Örneği")  
print("="*32)

print("Birinci sayıyı giriniz: ")
sayi1 = float(input())
print("İkinci sayıyı giriniz: ")
sayi2 = float(input())

def topla(a, b):
    return a + b
def carp(a, b):
    return a * b
def cikar(a, b):
    return a - b

print(f"Toplam: {topla(sayi1, sayi2)}")
print(f"Çarpım: {carp(sayi1, sayi2)}")
print(f"Fark: {cikar(sayi1, sayi2)}")


def email_kontrol(email):
    if "@" in email and "." in email and email.index("@") < email.rindex(".") and email.index("@") > 0 and email.rindex(".") < len(email) - 1:
        return True
    else:
        return False

email = input("Email adresinizi giriniz: ")
if email_kontrol(email):
    print("Geçerli bir email adresi girdiniz.")
else:
    print("Geçersiz bir email adresi girdiniz.")


    
# Şifre Güç Testi Oyunu
def sifre_guclu_mu(sifre):
    uzunluk = 8 <= len(sifre) <= 10
    buyuk_harf = any(c.isupper() for c in sifre)
    kucuk_harf = any(c.islower() for c in sifre)
    rakam = any(c.isdigit() for c in sifre)
    ozel_karakter = any(not c.isalnum() for c in sifre)
    
    return uzunluk and buyuk_harf and kucuk_harf and rakam and ozel_karakter

def guclu_sifre_oner(uzunluk=10):
    """
    Tüm kurallara uyan rastgele güçlü bir şifre üretir.
    - En az 1 büyük harf
    - En az 1 küçük harf
    - En az 1 rakam
    - En az 1 özel karakter
    """
    if uzunluk < 8:
        uzunluk = 8  # Minimum 8 karakter zorunlu
    elif uzunluk > 10:
        uzunluk = 10  # Maximum 10 karakter zorunlu

    # Karakter havuzları
    buyukler = string.ascii_uppercase
    kucukler = string.ascii_lowercase
    rakamlar = string.digits
    ozeller = "!@#$%^&*()-_=+[]{};:,.<>?/"

    # Her kategoriden en az 1 karakter ekle
    sifre = [
        random.choice(buyukler),
        random.choice(kucukler),
        random.choice(rakamlar),
        random.choice(ozeller)
    ]

    # Kalan karakterleri tüm havuzdan rastgele doldur
    tum_havuz = buyukler + kucukler + rakamlar + ozeller
    for _ in range(uzunluk - 4):
        sifre.append(random.choice(tum_havuz))

    # Karakterlerin sırasını karıştır (yoksa hep aynı sırada olur)
    random.shuffle(sifre)

    return "".join(sifre)

sifre = input("Şifrenizi giriniz: ")
if sifre_guclu_mu(sifre):
    print("Şifreniz güçlü.")
else:
    print("Şifreniz zayıf. Lütfen daha güçlü bir şifre seçin.")
    print(f"Önerilen güçlü şifre: {guclu_sifre_oner(10)}")