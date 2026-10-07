import json
import os
from collections import defaultdict
from datetime import datetime

# JSON dosyasının yolu
JSON_DOSYA = "c:/Users/User/Documents/Soner/Yazılım Seviye 2 - 3/PythonProjeleri/Ders1/fatura/fatura.json"


def veri_yukle():
    """fatura.json dosyasını okur ve liste olarak döndürür."""
    if not os.path.exists(JSON_DOSYA):
        print(f"HATA: '{JSON_DOSYA}' dosyası bulunamadı!")
        return []
    with open(JSON_DOSYA, "r", encoding="utf-8") as f:
        return json.load(f)


def para_formatla(deger):
    """Sayıyı Türk Lirası formatında gösterir."""
    return f"{deger:,.2f} TL".replace(",", "X").replace(".", ",").replace("X", ".")


def baslik_yazdir(baslik):
    """Başlık yazdırır."""
    print("\n" + "=" * 70)
    print(f" {baslik}")
    print("=" * 70)


# ----------------------------------------------------------------------
# 1- GENEL ÖZET
# ----------------------------------------------------------------------
def genel_ozet(faturalar):
    baslik_yazdir("GENEL ÖZET (İl - Fatura Tipi - Toplam Tutar)")

    if not faturalar:
        print("Kayıt bulunamadı.")
        return

    # İl + Fatura Tipi bazında gruplama
    gruplar = defaultdict(lambda: {"adet": 0, "toplam": 0.0, "tuketim": 0.0})

    for f in faturalar:
        anahtar = (f["İl"], f["Fatura Tipi"])
        gruplar[anahtar]["adet"] += 1
        gruplar[anahtar]["toplam"] += f["Toplam Fatura"]
        gruplar[anahtar]["tuketim"] += f["Tüketim Miktarı"]

    print(f"{'İl':<15} {'Fatura Tipi':<12} {'Adet':>6} {'Tüketim':>12} {'Toplam Tutar':>18}")
    print("-" * 70)

    genel_toplam = 0.0
    genel_adet = 0
    for (il, tip), deger in sorted(gruplar.items()):
        print(f"{il:<15} {tip:<12} {deger['adet']:>6} "
              f"{deger['tuketim']:>12,.0f} {para_formatla(deger['toplam']):>18}")
        genel_toplam += deger["toplam"]
        genel_adet += deger["adet"]

    print("-" * 70)
    print(f"{'TOPLAM':<15} {'':<12} {genel_adet:>6} {'':>12} {para_formatla(genel_toplam):>18}")

    # Fatura tipi bazında da özet
    baslik_yazdir("FATURA TİPİ BAZINDA ÖZET")
    tip_gruplari = defaultdict(lambda: {"adet": 0, "toplam": 0.0})
    for f in faturalar:
        tip_gruplari[f["Fatura Tipi"]]["adet"] += 1
        tip_gruplari[f["Fatura Tipi"]]["toplam"] += f["Toplam Fatura"]

    print(f"{'Fatura Tipi':<15} {'Adet':>6} {'Toplam Tutar':>18}")
    print("-" * 45)
    for tip, deger in sorted(tip_gruplari.items()):
        print(f"{tip:<15} {deger['adet']:>6} {para_formatla(deger['toplam']):>18}")


# ----------------------------------------------------------------------
# 2- FATURA NOYA GÖRE DETAY
# ----------------------------------------------------------------------
def fatura_detay(faturalar):
    baslik_yazdir("FATURA NOYA GÖRE DETAY")

    if not faturalar:
        print("Kayıt bulunamadı.")
        return
    #strip kullanıcının başında ve sonunda boşluk bırakmasını engeller
    fatura_no = input("Fatura No giriniz (örn: FTR20241001): ").strip()

    bulunan = None
    for f in faturalar:
        if f["Fatura No"].lower() == fatura_no.lower():
            bulunan = f
            break

    if not bulunan:
        print(f"'{fatura_no}' numaralı fatura bulunamadı!")
        return

    print("\n" + "-" * 50)
    for anahtar, deger in bulunan.items():
        if isinstance(deger, float):
            print(f"{anahtar:<20}: {para_formatla(deger)}")
        elif isinstance(deger, int):
            print(f"{anahtar:<20}: {deger:,}".replace(",", "."))
        else:
            print(f"{anahtar:<20}: {deger}")
    print("-" * 50)


# ----------------------------------------------------------------------
# 3- İL BAZLI DETAYLI ÖZET
# ----------------------------------------------------------------------
def il_bazli_ozet(faturalar):
    baslik_yazdir("İL BAZLI DETAYLI ÖZET")

    if not faturalar:
        print("Kayıt bulunamadı.")
        return

    # Benzersiz illeri topla
    iller = sorted(set(f["İl"] for f in faturalar))

    # İl -> ID eşleşmesi
    il_id = {il: idx + 1 for idx, il in enumerate(iller)}

    print("Mevcut İller:")
    print(f"{'ID':<5} {'İl':<15}")
    print("-" * 25)
    for il, idx in il_id.items():
        print(f"{idx:<5} {il:<15}")

    try:
        secim = int(input("\nİl ID giriniz: ").strip())
    except ValueError:
        print("Geçersiz ID!")
        return

    secilen_il = None
    for il, idx in il_id.items():
        if idx == secim:
            secilen_il = il
            break

    if not secilen_il:
        print(f"'{secim}' ID'li il bulunamadı!")
        return

    # Seçilen ilin faturaları
    il_faturalari = [f for f in faturalar if f["İl"] == secilen_il]

    baslik_yazdir(f"{secilen_il} İLİ DETAYLI ÖZETİ")

    # Fatura tipi bazında gruplama
    tip_gruplari = defaultdict(lambda: {"adet": 0, "toplam": 0.0,
                                         "tuketim": 0.0, "musteriler": set()})
    for f in il_faturalari:
        tip = f["Fatura Tipi"]
        tip_gruplari[tip]["adet"] += 1
        tip_gruplari[tip]["toplam"] += f["Toplam Fatura"]
        tip_gruplari[tip]["tuketim"] += f["Tüketim Miktarı"]
        tip_gruplari[tip]["musteriler"].add(f["Müşteri Adı"])

    print(f"{'Fatura Tipi':<12} {'Adet':>6} {'Müşteri':>8} {'Tüketim':>12} {'Toplam Tutar':>18}")
    print("-" * 60)

    il_toplam = 0.0
    il_adet = 0
    for tip, deger in sorted(tip_gruplari.items()):
        print(f"{tip:<12} {deger['adet']:>6} {len(deger['musteriler']):>8} "
              f"{deger['tuketim']:>12,.0f} {para_formatla(deger['toplam']):>18}")
        il_toplam += deger["toplam"]
        il_adet += deger["adet"]

    print("-" * 60)
    print(f"{'TOPLAM':<12} {il_adet:>6} {'':>8} {'':>12} {para_formatla(il_toplam):>18}")

    # İlçe bazında da özet
    baslik_yazdir(f"{secilen_il} İLİ İLÇE BAZINDA ÖZET")
    ilce_gruplari = defaultdict(lambda: {"adet": 0, "toplam": 0.0})
    for f in il_faturalari:
        ilce_gruplari[f["İlçe"]]["adet"] += 1
        ilce_gruplari[f["İlçe"]]["toplam"] += f["Toplam Fatura"]

    print(f"{'İlçe':<15} {'Adet':>6} {'Toplam Tutar':>18}")
    print("-" * 42)
    for ilce, deger in sorted(ilce_gruplari.items()):
        print(f"{ilce:<15} {deger['adet']:>6} {para_formatla(deger['toplam']):>18}")


# ----------------------------------------------------------------------
# 4- DÖNEM LİSTESİ VE ÖZETİ
# ----------------------------------------------------------------------
def donem_ozeti(faturalar):
    baslik_yazdir("DÖNEM LİSTESİ VE ÖZETİ")

    if not faturalar:
        print("Kayıt bulunamadı.")
        return

    # Tarihleri ay-yıl olarak grupla
    donemler = defaultdict(lambda: {"adet": 0, "toplam": 0.0,
                                     "tuketim": 0.0, "faturalar": []})

    for f in faturalar:
        # Tarih formatı: GG.AA.YYYY
        try:
            tarih = datetime.strptime(f["Tarih"], "%d.%m.%Y")
            donem = tarih.strftime("%m.%Y")  # AA.YYYY
        except ValueError:
            donem = "Bilinmeyen"

        donemler[donem]["adet"] += 1
        donemler[donem]["toplam"] += f["Toplam Fatura"]
        donemler[donem]["tuketim"] += f["Tüketim Miktarı"]
        donemler[donem]["faturalar"].append(f)

    # Dönemleri sırala
    sirali_donemler = sorted(donemler.keys(),
                             key=lambda x: datetime.strptime(x, "%m.%Y") if x != "Bilinmeyen" else datetime.min)

    # ID ata
    donem_id = {donem: idx + 1 for idx, donem in enumerate(sirali_donemler)}

    print("Mevcut Dönemler:")
    print(f"{'ID':<5} {'Dönem':<10} {'Fatura Adedi':>12}")
    print("-" * 30)
    for donem, idx in donem_id.items():
        print(f"{idx:<5} {donem:<10} {donemler[donem]['adet']:>12}")

    try:
        secim = int(input("\nDönem ID giriniz: ").strip())
    except ValueError:
        print("Geçersiz ID!")
        return

    secilen_donem = None
    for donem, idx in donem_id.items():
        if idx == secim:
            secilen_donem = donem
            break

    if not secilen_donem:
        print(f"'{secim}' ID'li dönem bulunamadı!")
        return

    baslik_yazdir(f"{secilen_donem} DÖNEMİ ÖZETİ")

    donem_faturalari = donemler[secilen_donem]["faturalar"]

    # Fatura tipi bazında gruplama
    tip_gruplari = defaultdict(lambda: {"adet": 0, "toplam": 0.0, "tuketim": 0.0})
    for f in donem_faturalari:
        tip = f["Fatura Tipi"]
        tip_gruplari[tip]["adet"] += 1
        tip_gruplari[tip]["toplam"] += f["Toplam Fatura"]
        tip_gruplari[tip]["tuketim"] += f["Tüketim Miktarı"]

    print(f"{'Fatura Tipi':<12} {'Adet':>6} {'Tüketim':>12} {'Toplam Tutar':>18}")
    print("-" * 52)

    donem_toplam = 0.0
    donem_adet = 0
    for tip, deger in sorted(tip_gruplari.items()):
        print(f"{tip:<12} {deger['adet']:>6} {deger['tuketim']:>12,.0f} "
              f"{para_formatla(deger['toplam']):>18}")
        donem_toplam += deger["toplam"]
        donem_adet += deger["adet"]

    print("-" * 52)
    print(f"{'TOPLAM':<12} {donem_adet:>6} {'':>12} {para_formatla(donem_toplam):>18}")

    # İl bazında özet
    print("\nİl Bazında Dağılım:")
    il_gruplari = defaultdict(lambda: {"adet": 0, "toplam": 0.0})
    for f in donem_faturalari:
        il_gruplari[f["İl"]]["adet"] += 1
        il_gruplari[f["İl"]]["toplam"] += f["Toplam Fatura"]

    print(f"{'İl':<15} {'Adet':>6} {'Toplam Tutar':>18}")
    print("-" * 42)
    for il, deger in sorted(il_gruplari.items()):
        print(f"{il:<15} {deger['adet']:>6} {para_formatla(deger['toplam']):>18}")


# ----------------------------------------------------------------------
# ANA MENÜ
# ----------------------------------------------------------------------
def ana_menu():
    faturalar = veri_yukle()
    if not faturalar:
        return

    while True:
        baslik_yazdir("FATURA KONSOL UYGULAMASI")
        print("1- Genel Özet Ver (İl - Fatura Tipi - Toplam Tutar)")
        print("2- Fatura Noya Göre Detay Ver")
        print("3- İl Bazlı Detaylı Özet")
        print("4- Dönemleri Listele ve Özet Ver")
        print("5- Çıkış")
        print("-" * 70)

        secim = input("Seçiminiz (1-5): ").strip()

        if secim == "1":
            genel_ozet(faturalar)
        elif secim == "2":
            fatura_detay(faturalar)
        elif secim == "3":
            il_bazli_ozet(faturalar)
        elif secim == "4":
            donem_ozeti(faturalar)
        elif secim == "5":
            print("\nProgramdan çıkılıyor. İyi günler!")
            break
        else:
            print("\nGeçersiz seçim! Lütfen 1-5 arasında bir değer giriniz.")

        input("\nDevam etmek için Enter'a basın...")


if __name__ == "__main__":
    ana_menu()