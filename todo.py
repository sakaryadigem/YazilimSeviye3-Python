"""JSON dosyası kullanan basit bir yapılacaklar listesi uygulaması."""

import json
from pathlib import Path


DOSYA = Path(__file__).with_name("gorevler.json")


def gorevleri_yukle():
    """Görevleri JSON dosyasından yükler."""
    try:
        with DOSYA.open("r", encoding="utf-8") as dosya:
            veri = json.load(dosya)
            if not isinstance(veri, dict) or not isinstance(veri.get("gorevler"), list):
                raise ValueError
            return veri
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return {"gorevler": []}


def gorevleri_kaydet(veri):
    """Görevleri JSON dosyasına kaydeder."""
    with DOSYA.open("w", encoding="utf-8") as dosya:
        json.dump(veri, dosya, ensure_ascii=False, indent=4)


def gorev_ekle():
    baslik = input("Görev başlığını giriniz: ").strip()
    if not baslik:
        print("Boş görev eklenemez.")
        return

    veri = gorevleri_yukle()
    veri["gorevler"].append({"baslik": baslik, "tamamlandi": False})
    gorevleri_kaydet(veri)
    print("Görev eklendi.")


def gorevleri_listele():
    gorevler = gorevleri_yukle()["gorevler"]
    if not gorevler:
        print("Henüz kayıtlı görev yok.")
        return

    for sira, gorev in enumerate(gorevler, start=1):
        durum = "Tamamlandı" if gorev.get("tamamlandi", False) else "Bekliyor"
        print(f"{sira}. [{durum}] {gorev.get('baslik', 'Başlıksız görev')}")


def gorev_numarasi_al(mesaj):
    try:
        return int(input(mesaj))
    except ValueError:
        print("Lütfen geçerli bir görev numarası giriniz.")
        return None


def gorev_tamamla():
    veri = gorevleri_yukle()
    numara = gorev_numarasi_al("Tamamlanacak görev numarası: ")
    if numara is None or not 1 <= numara <= len(veri["gorevler"]):
        print("Geçersiz görev numarası.")
        return

    veri["gorevler"][numara - 1]["tamamlandi"] = True
    gorevleri_kaydet(veri)
    print("Görev tamamlandı olarak işaretlendi.")


def gorev_sil():
    veri = gorevleri_yukle()
    numara = gorev_numarasi_al("Silinecek görev numarası: ")
    if numara is None or not 1 <= numara <= len(veri["gorevler"]):
        print("Geçersiz görev numarası.")
        return

    silinen = veri["gorevler"].pop(numara - 1)
    gorevleri_kaydet(veri)
    print(f"'{silinen['baslik']}' görevi silindi.")


def menu():
    while True:
        print("\n--- Yapılacaklar Listesi ---")
        print("1. Görev ekle")
        print("2. Görevleri listele")
        print("3. Görev tamamla")
        print("4. Görev sil")
        print("5. Çıkış")

        secim = input("Seçiminizi yapınız (1-5): ").strip()

        if secim == "1":
            gorev_ekle()
        elif secim == "2":
            gorevleri_listele()
        elif secim == "3":
            gorev_tamamla()
        elif secim == "4":
            gorev_sil()
        elif secim == "5":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim. Lütfen 1 ile 5 arasında seçim yapınız.")


if __name__ == "__main__":
    menu()
