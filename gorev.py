#to do list mantığında json dosyasındaki görevlerin takibini yapacak bir 
# program yazalım. Kullanıcılar görev ekleyebilecek, tamamlanan görevleri 
# işaretleyebilecek ve görevleri silebilecekler. 
# Görevler bir json dosyasında saklanacak.
import json

def yukle():
    try:
        with open("gorevler.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"gorevler": []}

def kaydet(data):
    with open("gorevler.json", "w") as file:
        json.dump(data, file, indent=4, sort_keys=False)

def gorev_ekle(gorev):
    data = yukle()
    data["gorevler"].append({"baslik": gorev, "tamamlandi": False})
    kaydet(data)

def gorevleri_listele():
    data = yukle()
    for i, g in enumerate(data["gorevler"], 1):
        durum = "✔" if g["tamamlandi"] else "✘"
        print(f"{i}. [{durum}] {g['baslik']}")

def gorev_tamamla(index):
    data = yukle()
    if 0 < index <= len(data["gorevler"]):
        data["gorevler"][index - 1]["tamamlandi"] = True
        kaydet(data)
    else:
        print("Geçersiz görev numarası.")

def gorev_sil(index):
    data = yukle()
    if 0 < index <= len(data["gorevler"]):
        data["gorevler"].pop(index - 1)
        kaydet(data)
    else:
        print("Geçersiz görev numarası.")


def main():
    print("**"*32)
    print("***        Görev Listesi Uygulaması     ***")
    print("**"*32)
    print("1. Görev Ekle")
    print("2. Görevleri Listele")   
    print("3. Görev Tamamla")
    print("4. Görev Sil")
    print("5. Çıkış")

    while True:
        secim = input("Seçiminizi yapınız (1-5): ")

        if secim == "1":
            gorev = input("Görev başlığını giriniz: ")
            gorev_ekle(gorev)
            print("Görev eklendi.")
        elif secim == "2":
            print("Görevler:")
            gorevleri_listele()
        elif secim == "3":
            index = int(input("Tamamlanacak görev numarasını giriniz: "))
            gorev_tamamla(index)
            print("Görev tamamlandı.")
        elif secim == "4":
            index = int(input("Silinecek görev numarasını giriniz: "))
            gorev_sil(index)
            print("Görev silindi.")
        elif secim == "5":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen tekrar deneyin.")
            
if __name__ == "__main__":            
    main()

