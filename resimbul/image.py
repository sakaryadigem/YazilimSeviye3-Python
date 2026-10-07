"""
Görsel Sınıflandırma ve Otomatik Taşıma Uygulaması
--------------------------------------------------
Kaynak klasördeki görselleri analiz eder, kriterlere göre
sınıflandırır ve hedef alt klasörlere taşır.

Gereksinimler:
    pip install Pillow
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from collections import defaultdict

try:
    from PIL import Image, UnidentifiedImageError
except ImportError:
    print("[HATA] 'Pillow' kütüphanesi bulunamadı.")
    print("Kurulum için: pip install Pillow")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Ayarlar
# ---------------------------------------------------------------------------
DESTEKLI_UZANTILAR = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp"}

# Kategori isimleri (klasör adı olarak kullanılacak)
KATEGORI_DIKEY   = "Dikey"
KATEGORI_YATAY   = "Yatay"
KATEGORI_KARE    = "Kare"
KATEGORI_GRI     = "Gri_Ton"
KATEGORI_RENKLI  = "Renkli"

# En-boy oranı toleransı (kare kabul edilme sınırı)
KARE_TOLERANS = 0.05  # ±%5


# ---------------------------------------------------------------------------
# Loglama Yapılandırması
# ---------------------------------------------------------------------------
def loglama_kur(log_dosyasi: Path) -> logging.Logger:
    """Hem konsola hem de dosyaya yazan bir logger oluşturur."""
    logger = logging.getLogger("GorselSiniflandirici")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Konsol handler
    konsol = logging.StreamHandler(sys.stdout)
    konsol.setFormatter(formatter)
    logger.addHandler(konsol)

    # Dosya handler
    try:
        dosya = logging.FileHandler(log_dosyasi, encoding="utf-8")
        dosya.setFormatter(formatter)
        logger.addHandler(dosya)
    except OSError as e:
        logger.warning(f"Log dosyası oluşturulamadı: {e}")

    return logger


# ---------------------------------------------------------------------------
# Kullanıcı Girdileri
# ---------------------------------------------------------------------------
def kaynak_klasor_al() -> Path:
    """Kullanıcıdan geçerli bir kaynak klasör yolu alır."""
    while True:
        yol = input("Taranacak kaynak klasörün yolunu girin: ").strip().strip('"')
        if not yol:
            print("[!] Yol boş olamaz. Tekrar deneyin.")
            continue

        klasor = Path(yol).expanduser().resolve()
        if not klasor.exists():
            print(f"[!] Klasör bulunamadı: {klasor}")
        elif not klasor.is_dir():
            print(f"[!] Bu bir klasör değil: {klasor}")
        else:
            return klasor


def hedef_klasor_al(varsayilan: Path) -> Path:
    """Hedef klasör yolunu alır; boş bırakılırsa varsayılan kullanılır."""
    yol = input(
        f"Hedef klasör (Enter = '{varsayilan}'): "
    ).strip().strip('"')

    if not yol:
        hedef = varsayilan
    else:
        hedef = Path(yol).expanduser().resolve()

    hedef.mkdir(parents=True, exist_ok=True)
    return hedef


# ---------------------------------------------------------------------------
# Kategori Klasörlerini Oluşturma
# ---------------------------------------------------------------------------
def kategori_klasorlerini_olustur(hedef: Path) -> dict:
    """Hedef dizin altında tüm kategori klasörlerini oluşturur."""
    kategoriler = [
        KATEGORI_YATAY, KATEGORI_DIKEY, KATEGORI_KARE,
        KATEGORI_GRI, KATEGORI_RENKLI,
    ]
    yollar = {}
    for k in kategoriler:
        p = hedef / k
        p.mkdir(parents=True, exist_ok=True)
        yollar[k] = p
    return yollar


# ---------------------------------------------------------------------------
# Görsel Analiz Motoru
# ---------------------------------------------------------------------------
def yon_belirle(width: int, height: int) -> str:
    """En-boy oranına göre yön kategorisini döndürür."""
    if height == 0 or width == 0:
        return KATEGORI_KARE  # bozuk durum, varsayılan

    oran = width / height

    if abs(oran - 1.0) <= KARE_TOLERANS:
        return KATEGORI_KARE
    elif oran > 1.0:
        return KATEGORI_YATAY
    else:
        return KATEGORI_DIKEY


def renk_modu_belirle(mode: str) -> str:
    """Pillow renk moduna göre gri/renkli sınıflandırması yapar."""
    # 'L'  -> Gri tonlamalı (8-bit)
    # '1'  -> 1-bit siyah/beyaz
    # 'LA' -> Gri + alfa
    # 'I;16', 'F' -> tek kanal yoğunluk
    gri_modlar = {"L", "1", "LA", "I", "I;16", "F"}
    if mode in gri_modlar:
        return KATEGORI_GRI
    return KATEGORI_RENKLI


def gorsel_analiz_et(dosya: Path, logger: logging.Logger) -> dict | None:
    """
    Bir görseli analiz eder ve sonuçları sözlük olarak döner.
    Başarısız olursa None döner.
    """
    try:
        with Image.open(dosya) as img:
            width, height = img.size
            mode = img.mode

        yon = yon_belirle(width, height)
        renk = renk_modu_belirle(mode)

        return {
            "dosya": dosya,
            "genislik": width,
            "yukseklik": height,
            "mod": mode,
            "yon": yon,
            "renk": renk,
        }
    except UnidentifiedImageError:
        logger.warning(f"Görsel değil / bozuk: {dosya.name}")
    except (OSError, IOError) as e:
        logger.error(f"Dosya okunamadı ({dosya.name}): {e}")
    except Exception as e:
        logger.error(f"Beklenmeyen hata ({dosya.name}): {e}")
    return None


# ---------------------------------------------------------------------------
# Akıllı Taşıma
# ---------------------------------------------------------------------------
def benzersiz_yol(hedef_dosya: Path) -> Path:
    """Aynı isim varsa dosya_adı_1.jpg, _2.jpg ... şeklinde yeni ad üretir."""
    if not hedef_dosya.exists():
        return hedef_dosya

    kok = hedef_dosya.stem
    uzanti = hedef_dosya.suffix
    klasor = hedef_dosya.parent
    sayac = 1
    while True:
        yeni = klasor / f"{kok}_{sayac}{uzanti}"
        if not yeni.exists():
            return yeni
        sayac += 1


def guvenli_tasi(kaynak: Path, hedef_klasor: Path, logger: logging.Logger) -> bool:
    """Dosyayı güvenli şekilde hedef klasöre taşır."""
    try:
        hedef = benzersiz_yol(hedef_klasor / kaynak.name)
        shutil.move(str(kaynak), str(hedef))
        return True
    except (shutil.Error, OSError, PermissionError) as e:
        logger.error(f"Taşıma hatası ({kaynak.name}): {e}")
        return False


# ---------------------------------------------------------------------------
# Ana İş Akışı
# ---------------------------------------------------------------------------
def dosyalari_topla(kaynak: Path) -> list[Path]:
    """Kaynak klasördeki desteklenen görsel dosyalarını listeler (alt klasörler hariç)."""
    gorseller = []
    for dosya in kaynak.iterdir():
        if dosya.is_file() and dosya.suffix.lower() in DESTEKLI_UZANTILAR:
            gorseller.append(dosya)
    return gorseller


def rapor_yazdir(sayaclar: dict, toplam: int, hatali: int, logger: logging.Logger) -> None:
    """Konsola özet raporu yazdırır."""
    print("\n" + "=" * 55)
    print("             SINIFLANDIRMA ÖZET RAPORU")
    print("=" * 55)

    if toplam == 0:
        print("Hiç görsel bulunamadı veya işlenemedi.")
    else:
        print(f"Toplam taranan görsel : {toplam}")
        print(f"Başarılı taşınan      : {toplam - hatali}")
        print(f"Hatalı / atlanan      : {hatali}")
        print("-" * 55)
        print(f"{'Kategori':<20}{'Adet':>10}")
        print("-" * 55)

        for kategori in [
            KATEGORI_YATAY, KATEGORI_DIKEY, KATEGORI_KARE,
            KATEGORI_GRI, KATEGORI_RENKLI,
        ]:
            adet = sayaclar.get(kategori, 0)
            print(f"{kategori:<20}{adet:>10}")

    print("=" * 55)

    # Log dosyasına da özet yaz
    logger.info("---- ÖZET RAPOR ----")
    logger.info(f"Toplam: {toplam} | Başarılı: {toplam - hatali} | Hatalı: {hatali}")
    for k, v in sayaclar.items():
        logger.info(f"  {k}: {v}")


def main() -> None:
    print("=" * 55)
    print("   GÖRSEL SINIFLANDIRICI VE OTOMATİK TAŞIYICI")
    print("=" * 55)

    # 1) Kaynak klasör
    kaynak = kaynak_klasor_al()

    # 2) Hedef klasör
    varsayilan_hedef = kaynak / "Siniflandirilmis"
    hedef = hedef_klasor_al(varsayilan_hedef)

    # 3) Loglama
    logger = loglama_kur(hedef / "islem_logu.log")
    logger.info(f"Kaynak klasör : {kaynak}")
    logger.info(f"Hedef klasör  : {hedef}")

    # 4) Kategori klasörlerini oluştur
    kategori_yollari = kategori_klasorlerini_olustur(hedef)
    logger.info(f"{len(kategori_yollari)} kategori klasörü hazır.")

    # 5) Kaynak klasördeki görselleri topla
    gorseller = dosyalari_topla(kaynak)
    logger.info(f"{len(gorseller)} görsel dosyası bulundu.")

    if not gorseller:
        print("[!] Kaynak klasörde desteklenen görsel bulunamadı.")
        return

    # 6) Analiz + Taşıma
    sayaclar = defaultdict(int)
    hatali = 0
    toplam = 0

    print("\nİşlem başlatılıyor...\n")

    for gorsel in gorseller:
        toplam += 1
        sonuc = gorsel_analiz_et(gorsel, logger)
        if sonuc is None:
            hatali += 1
            continue

        # Bir görsel iki kategoriye ait olabilir: yön + renk
        # Bu yüzden her iki kategoriye de taşımak yerine, daha anlamlı olan
        # TEK bir kategori seçiyoruz. Burada öncelik sırası:
        #   Gri tonlamalı  -> Gri_Ton
        #   Aksi halde     -> Dikey / Yatay / Kare
        if sonuc["renk"] == KATEGORI_GRI:
            kategori = KATEGORI_GRI
        else:
            kategori = sonuc["yon"]

        basarili = guvenli_tasi(gorsel, kategori_yollari[kategori], logger)

        if basarili:
            sayaclar[kategori] += 1
            logger.info(
                f"TAŞINDI | {gorsel.name} -> {kategori} "
                f"({sonuc['genislik']}x{sonuc['yukseklik']}, mod={sonuc['mod']})"
            )
        else:
            hatali += 1

    # 7) Rapor
    rapor_yazdir(sayaclar, toplam, hatali, logger)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Kullanıcı tarafından iptal edildi.")
    except Exception as e:
        print(f"\n[HATA] Beklenmeyen bir sorun oluştu: {e}")