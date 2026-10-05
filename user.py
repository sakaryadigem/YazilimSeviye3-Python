#kullanici ve sifre kontrolunu bir json dosyası 
# üzerinden yapan örnek bir pyhon kodu
import json


kullanici_adi     = input("Kullanıcı: ")
sifre             = input("Şifre: ")

# Kullanıcı listesini bir json dosyasının içinden okuyabiliriz. Örnek olarak, kullanıcı_listesi.json dosyası:
# {
#     "kullanicilar": ["aliveli", "mehmet1453"]
# }
kullanici_listesi = []

try:
    with open("users.json", "r") as file:
        data = json.load(file)
        # "users" anahtarı var mı kontrol et
        if ("users" in data) and ("username" in data["users"][0]) and ("password" in data["users"][0]):
            kullanici_listesi = [user["username"] for user in data["users"]]
        else:
            print("'users' anahtarı bulunamadı. Boş liste oluşturuluyor.")
            kullanici_listesi = []

except (FileNotFoundError, json.JSONDecodeError):
    print("Kullanıcı listesi bulunamadı veya bozuk. Yeni bir liste oluşturulacak.")
    kullanici_listesi = []


# Hataları biriktirmek için liste
hatalar = []

# 1) Kullanıcı adı uzunluk kontrolü: 8'den fazla, 11'den az olmalı
if not (len(kullanici_adi) > 7 and len(kullanici_adi) < 11):
    hatalar.append("Kullanıcı adı en az 8 karakter ve en fazla 10 karakter olmalı.")

# 2) Kullanıcı adı zaten kayıtlı mı?
if kullanici_adi in kullanici_listesi:
    hatalar.append("Bu kullanıcı adı zaten kayıtlı.")

# 3) Şifre en az 8 karakter olmalı
if len(sifre) < 8:
    hatalar.append("Şifre en az 8 karakter uzunluğunda olmalı.")

# 4) Şifre '1234' veya 'password' içermemeli
if ("1234" in sifre) or ("password" in sifre):
    hatalar.append("Şifre '1234' veya 'password' içermemeli.")

# 5) Şifre 'a' harfi içermemeli
if "a" in sifre:
    hatalar.append("Şifre 'a' harfi içermemeli.")

# 6) Kullanıcı adı ile şifre aynı olmamalı
if kullanici_adi == sifre:
    hatalar.append("Kullanıcı adı ile şifre aynı olmamalı.")

# Sonuç kontrolü
if not hatalar:
    #kullanıcı listesine ekleme yap
    data["users"].append({"username": kullanici_adi, "password": sifre})
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4, sort_keys=False)
    print("Kullanıcı adı ve Şifre kabul edildi")
else:
    print("Kullanıcı adı veya Şifre reddedildi. İhlal edilen kurallar:")
    for hata in hatalar:
        print("-", hata)    