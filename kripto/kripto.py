import json
import os
import base64

REFERANS_DOSYA = "c:/Users/User/Documents/Soner/Yazılım Seviye 2 - 3/PythonProjeleri/Ders1/kripto/referans.json"
DUZ_DOSYA = "c:/Users/User/Documents/Soner/Yazılım Seviye 2 - 3/PythonProjeleri/Ders1/kripto/duz_metin.txt"
KRIPTOLU_DOSYA = "c:/Users/User/Documents/Soner/Yazılım Seviye 2 - 3/PythonProjeleri/Ders1/kripto/kriptolu.txt"
# ---------------- Yardımcılar ----------------

def referans_yukle():
    if not os.path.exists(REFERANS_DOSYA):
        raise FileNotFoundError(f"{REFERANS_DOSYA} bulunamadı!")
    with open(REFERANS_DOSYA, "r", encoding="utf-8") as f:
        return json.load(f)


def ters_harita(harfler):
    return {v: k for k, v in harfler.items()}


def dosyaya_yaz(yol, icerik):
    with open(yol, "w", encoding="utf-8") as f:
        f.write(icerik)


def dosyadan_oku(yol):
    if not os.path.exists(yol):
        return ""
    with open(yol, "r", encoding="utf-8") as f:
        return f.read()


# ---------------- Vigenère ----------------
# ÖNEMLİ: Vigenère artık SADECE alfabedeki harflere uygulanır.
# Rakam ve özel karakterler DOKUNULMADAN geçirilir (değiştirilmez).

def vigenere_sifrele(metin, anahtar):
    alfabe = "abcçdefgğhıijklmnoöprsştuüvyz"
    sonuc = []
    anahtar = anahtar.lower()
    k_idx = 0

    for ch in metin:
        alt = ch.lower()
        if alt in alfabe:
            kaydir_harf = anahtar[k_idx % len(anahtar)]
            kaydir = alfabe.index(kaydir_harf) if kaydir_harf in alfabe else 0
            yeni_idx = (alfabe.index(alt) + kaydir) % len(alfabe)
            yeni_harf = alfabe[yeni_idx]
            # Büyük/küçük harf koruması
            sonuc.append(yeni_harf.upper() if ch.isupper() else yeni_harf)
            k_idx += 1
        else:
            # Harf değilse (rakam, noktalama, boşluk) OLDUĞU GİBİ geçir
            sonuc.append(ch)
    return "".join(sonuc)


def vigenere_coz(metin, anahtar):
    alfabe = "abcçdefgğhıijklmnoöprsştuüvyz"
    sonuc = []
    anahtar = anahtar.lower()
    k_idx = 0

    for ch in metin:
        alt = ch.lower()
        if alt in alfabe:
            kaydir_harf = anahtar[k_idx % len(anahtar)]
            kaydir = alfabe.index(kaydir_harf) if kaydir_harf in alfabe else 0
            yeni_idx = (alfabe.index(alt) - kaydir) % len(alfabe)
            yeni_harf = alfabe[yeni_idx]
            sonuc.append(yeni_harf.upper() if ch.isupper() else yeni_harf)
            k_idx += 1
        else:
            sonuc.append(ch)
    return "".join(sonuc)


# ---------------- Sayısal Haritalama (GÜNCELLENDİ) ----------------

def sayilara_cevir(metin, harfler):
    """
    Her karakteri referans.json'daki sayı karşılığına çevirir.
    Bilinmeyen karakter varsa Unicode kod noktasını kullanır (kaybolmaz!).
    """
    kodlar = []
    for ch in metin:
        # Önce doğrudan eşleşme ara (küçük harfle)
        if ch in harfler:
            kodlar.append(str(harfler[ch]))
        elif ch.lower() in harfler:
            kodlar.append(str(harfler[ch.lower()]))
        else:
            # Bilinmeyen karakter → 900000 + Unicode kodu
            # Böylece hiçbir karakter kaybolmaz
            kodlar.append(str(900000 + ord(ch)))
    return "-".join(kodlar)


def sayilardan_geri(kodlu, ters):
    """
    Sayı kodlarını tekrar metne çevirir.
    900000+ aralığındaki kodlar Unicode karakterlerdir.
    """
    parcalar = kodlu.split("-")
    metin = []
    for p in parcalar:
        if p.strip() == "":
            continue
        try:
            sayi = int(p)
            if sayi >= 900000:
                # Unicode karakter geri kazan
                metin.append(chr(sayi - 900000))
            else:
                metin.append(ters.get(sayi, "?"))
        except ValueError:
            continue
    return "".join(metin)


# ---------------- Katmanlı Şifreleme ----------------

def sifrele(duz_metin, referans):
    harfler = referans["harfler"]
    anahtar = referans["anahtar"]

    v = vigenere_sifrele(duz_metin, anahtar)
    print(f"   [1] Vigenère sonrası : {v}")

    s = sayilara_cevir(v, harfler)
    print(f"   [2] Sayısal harita  : {s[:80]}{'...' if len(s) > 80 else ''}")

    b = base64.b64encode(s.encode("utf-8")).decode("utf-8")
    print(f"   [3] Base64 sonrası  : {b[:80]}{'...' if len(b) > 80 else ''}")

    kriptolu = b[::-1]
    print(f"   [4] Ters çevrilmiş  : {kriptolu[:80]}{'...' if len(kriptolu) > 80 else ''}")

    return kriptolu


def geri_dondur(kriptolu, referans):
    harfler = referans["harfler"]
    anahtar = referans["anahtar"]
    ters = ters_harita(harfler)

    b = kriptolu[::-1]
    print(f"   [1] Ters geri       : {b[:80]}{'...' if len(b) > 80 else ''}")

    s = base64.b64decode(b.encode("utf-8")).decode("utf-8")
    print(f"   [2] Base64 geri     : {s[:80]}{'...' if len(s) > 80 else ''}")

    v = sayilardan_geri(s, ters)
    print(f"   [3] Sayı geri       : {v}")

    duz = vigenere_coz(v, anahtar)
    print(f"   [4] Vigenère geri   : {duz}")

    return duz


# ---------------- Menü İşlemleri ----------------

def menu_sifrele(referans):
    print("\n" + "-" * 55)
    print("🔒 METNİ ŞİFRELE")
    print("-" * 55)

    metin = input("📝 Şifrelenecek metin: ")
    if not metin.strip():
        print("⚠️  Boş metin giremezsiniz.")
        return

    print("\n--- ŞİFRELEME ADIMLARI ---")
    kriptolu = sifrele(metin, referans)

    dosyaya_yaz(KRIPTOLU_DOSYA, kriptolu)
    dosyaya_yaz(DUZ_DOSYA, metin)

    print(f"\n✅ kriptolu.txt dosyasına yazıldı.")
    print(f"✅ duz_metin.txt dosyasına yazıldı.")
    print("-" * 55)


def menu_geri_dondur(referans):
    print("\n" + "-" * 55)
    print("🔓 ŞİFRELİ METNİ ÇEVİR")
    print("-" * 55)

    kriptolu = dosyadan_oku(KRIPTOLU_DOSYA).strip()
    if not kriptolu:
        print("⚠️  kriptolu.txt boş! Önce bir metin şifreleyin.")
        return

    print(f"📄 Okunan şifreli metin: {kriptolu[:80]}{'...' if len(kriptolu) > 80 else ''}\n")
    print("--- ÇÖZME ADIMLARI ---")

    try:
        duz = geri_dondur(kriptolu, referans)
    except Exception as e:
        print(f"❌ Çözme hatası: {e}")
        return

    dosyaya_yaz(DUZ_DOSYA, duz)

    print("\n" + "=" * 55)
    print(f"📢 ÇÖZÜLEN METİN : {duz}")
    print("=" * 55)
    print(f"✅ duz_metin.txt dosyasına yazıldı.")
    print("-" * 55)


def main():
    try:
        referans = referans_yukle()
    except FileNotFoundError as e:
        print(f"❌ {e}")
        return

    while True:
        print("\n" + "=" * 55)
        print("🔐 KRİPTOLOJİ MENÜSÜ")
        print("=" * 55)
        print("  1. Metni Şifrele")
        print("  2. Şifreli Metni Çevir")
        print("  3. Çıkış")
        print("=" * 55)

        secim = input("👉 Seçiminiz (1/2/3): ").strip()

        if secim == "1":
            menu_sifrele(referans)
        elif secim == "2":
            menu_geri_dondur(referans)
        elif secim == "3":
            print("\n👋 Çıkılıyor... Görüşürüz!")
            break
        else:
            print("⚠️  Geçersiz seçim! Lütfen 1, 2 veya 3 girin.")


if __name__ == "__main__":
    main()