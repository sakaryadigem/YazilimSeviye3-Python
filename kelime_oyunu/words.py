import json
import os
import random
from pathlib import Path

DATA_FILE = Path(__file__).with_name("words.json")


# ---------------------------
# Veri İşlemleri
# ---------------------------
def load_words():
    """JSON dosyasından kelimeleri yükler."""
    if not os.path.exists(DATA_FILE):
        # Örnek verilerle başlat. json dosyası yoksa, varsayılan kelimelerle başlatılır.
        default_data = [
            {"id": 1, "en": "Achieve", "tr": "Başarmak", "level": 3,
             "correct_count": 2, "wrong_count": 1},
            {"id": 2, "en": "Curious", "tr": "Meraklı", "level": 1,
             "correct_count": 5, "wrong_count": 0},
        ]
        save_words(default_data)
        return default_data

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_words(words):
    """Kelimeleri JSON dosyasına kaydeder."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)


def get_next_id(words):
    """Yeni kelime için benzersiz ID üretir."""
    return max((w["id"] for w in words), default=0) + 1


# ---------------------------
# Yardımcılar
# ---------------------------
def clear():
    os.system("cls" if os.name == "nt" else "clear")


def input_int(prompt, min_val=None, max_val=None):
    """Geçerli bir tamsayı alana kadar sorar."""
    while True:
        try:
            val = int(input(prompt).strip())
            if (min_val is not None and val < min_val) or \
               (max_val is not None and val > max_val):
                print(f"⚠️  Lütfen {min_val} ile {max_val} arasında bir değer girin.")
                continue
            return val
        except ValueError:
            print("⚠️  Geçersiz giriş. Tamsayı giriniz.")


def pause():
    input("\n⏎ Devam etmek için Enter'a basın...")


# ---------------------------
# Flashcard Modu
# ---------------------------
def flashcard_mode(words):
    if not words:
        print("📭 Henüz kelime yok. Önce kelime ekleyin.")
        pause()
        return

    print("\n🎯 Flashcard Modu")
    print("Yön seçin:")
    print("  1) İngilizce → Türkçe")
    print("  2) Türkçe → İngilizce")
    direction = input_int("Seçim: ", 1, 2)

    # Zorluk filtresi
    print("\nZorluk filtresi (1-5). Hepsini çalışmak için 0 girin.")
    level_filter = input_int("Seviye: ", 0, 5)
    pool = [w for w in words if level_filter == 0 or w["level"] == level_filter]

    if not pool:
        print("📭 Bu seviyede kelime bulunamadı.")
        pause()
        return

    random.shuffle(pool)
    correct = 0
    wrong = 0

    for idx, word in enumerate(pool, 1):
        clear()
        print(f"📇 Soru {idx}/{len(pool)}  |  Seviye: {word['level']}")
        print("-" * 40)

        if direction == 1:
            question, answer = word["en"], word["tr"]
        else:
            question, answer = word["tr"], word["en"]

        print(f"❓ {question}")
        user_ans = input("👉 Cevabınız: ").strip()

        if user_ans.lower() == answer.lower():
            print("✅ Doğru!")
            word["correct_count"] += 1
            correct += 1
        else:
            print(f"❌ Yanlış. Doğru cevap: {answer}")
            word["wrong_count"] += 1
            wrong += 1

        pause()

    save_words(words)
    print(f"\n🏁 Bitti!  Doğru: {correct}  |  Yanlış: {wrong}")


# ---------------------------
# Yeni Kelime Ekle
# ---------------------------
def add_word(words):
    print("\n➕ Yeni Kelime Ekle")
    en = input("İngilizce: ").strip()
    tr = input("Türkçe: ").strip()

    if not en or not tr:
        print("⚠️  Boş bırakılamaz.")
        pause()
        return

    level = input_int("Zorluk (1-5): ", 1, 5)

    new_word = {
        "id": get_next_id(words),
        "en": en,
        "tr": tr,
        "level": level,
        "correct_count": 0,
        "wrong_count": 0,
    }
    words.append(new_word)
    save_words(words)
    print(f"✅ '{en}' eklendi.")
    pause()


# ---------------------------
# Listele / Düzenle
# ---------------------------
def list_words(words):
    if not words:
        print("📭 Kayıtlı kelime yok.")
        pause()
        return

    print("\n📋 Kelime Listesi")
    print(f"{'ID':<5}{'İngilizce':<20}{'Türkçe':<20}{'Sv':<4}{'D':<4}{'Y':<4}")
    print("-" * 57)
    for w in words:
        print(f"{w['id']:<5}{w['en']:<20}{w['tr']:<20}"
              f"{w['level']:<4}{w['correct_count']:<4}{w['wrong_count']:<4}")

    print("\nİşlem seçin:")
    print("  1) Kelime Düzenle")
    print("  2) Kelime Sil")
    print("  0) Geri")
    choice = input_int("Seçim: ", 0, 2)

    if choice == 0:
        return

    target_id = input_int("Kelime ID: ")
    target = next((w for w in words if w["id"] == target_id), None)
    if not target:
        print("⚠️  ID bulunamadı.")
        pause()
        return

    if choice == 1:
        print(f"\nMevcut: EN={target['en']} | TR={target['tr']} | Seviye={target['level']}")
        en = input("Yeni İngilizce (boş = değiştirme): ").strip()
        tr = input("Yeni Türkçe (boş = değiştirme): ").strip()
        lvl = input("Yeni Seviye 1-5 (boş = değiştirme): ").strip()

        if en:
            target["en"] = en
        if tr:
            target["tr"] = tr
        if lvl:
            try:
                l = int(lvl)
                if 1 <= l <= 5:
                    target["level"] = l
                else:
                    print("⚠️  Seviye 1-5 olmalı, değiştirilmedi.")
            except ValueError:
                print("⚠️  Geçersiz seviye, değiştirilmedi.")
        print("✅ Güncellendi.")
    else:
        words.remove(target)
        print("🗑️  Silindi.")

    save_words(words)
    pause()


# ---------------------------
# İstatistikler
# ---------------------------
def show_stats(words):
    clear()
    print("📊 İstatistikler")
    print("=" * 40)
    if not words:
        print("📭 Veri yok.")
        pause()
        return

    total = len(words)
    total_correct = sum(w["correct_count"] for w in words)
    total_wrong = sum(w["wrong_count"] for w in words)
    total_attempts = total_correct + total_wrong
    accuracy = (total_correct / total_attempts * 100) if total_attempts else 0

    print(f"Toplam Kelime      : {total}")
    print(f"Doğru Cevap        : {total_correct}")
    print(f"Yanlış Cevap       : {total_wrong}")
    print(f"Başarı Oranı       : {accuracy:.1f}%")

    # Seviyeye göre dağılım
    print("\nSeviye Dağılımı:")
    for lvl in range(1, 6):
        count = sum(1 for w in words if w["level"] == lvl)
        bar = "█" * count
        print(f"  Seviye {lvl}: {bar} ({count})")

    # En çok yanlış yapılanlar
    hardest = sorted(words, key=lambda w: w["wrong_count"], reverse=True)[:5]
    print("\n🔻 En Çok Yanlış Yapılanlar:")
    for w in hardest:
        if w["wrong_count"] > 0:
            print(f"  • {w['en']} → {w['tr']}  (Y:{w['wrong_count']} D:{w['correct_count']})")

    # En iyi bilinenler
    easiest = sorted(words,
                     key=lambda w: w["correct_count"] - w["wrong_count"],
                     reverse=True)[:5]
    print("\n🏆 En İyi Bilinenler:")
    for w in easiest:
        print(f"  • {w['en']} → {w['tr']}  (D:{w['correct_count']} Y:{w['wrong_count']})")

    pause()


# ---------------------------
# Ana Menü
# ---------------------------
def main():
    words = load_words()

    while True:
        clear()
        print("╔══════════════════════════════════════╗")
        print("║   📚 KELİME KARTI UYGULAMASI 📚      ║")
        print("╠══════════════════════════════════════╣")
        print("║  1) Kelime Çalışması (Flashcard)     ║")
        print("║  2) Yeni Kelime Ekle                 ║")
        print("║  3) Kelimeleri Listele / Düzenle     ║")
        print("║  4) İstatistikleri Gör               ║")
        print("║  0) Çıkış                            ║")
        print("╚══════════════════════════════════════╝")

        choice = input_int("Seçiminiz: ", 0, 4)

        if choice == 1:
            flashcard_mode(words)
        elif choice == 2:
            add_word(words)
        elif choice == 3:
            list_words(words)
        elif choice == 4:
            show_stats(words)
        elif choice == 0:
            save_words(words)
            print("\n👋 Görüşmek üzere!")
            break


if __name__ == "__main__":
    main()