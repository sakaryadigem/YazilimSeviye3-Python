"""Renkli Kart Hafızası - İlkokul öğrencileri için Tkinter oyunu.

Not: İstenen HTML/CSS/JS görünümü Tkinter'ın Python arayüzüyle hazırlanmıştır:
renkler ve stiller CSS değişkenleri gibi, oyun akışı da JavaScript'teki olay
yöneticileri gibi ayrı fonksiyonlarda tutulur.
"""

import random
import tkinter as tk
from tkinter import messagebox

try:
    import winsound
except ImportError:  # Windows dışı bilgisayarlarda sessizce çalışır.
    winsound = None


# CSS benzeri renk paleti
COLORS = {
    "background": "#FFF4D6",
    "panel": "#FFFFFF",
    "purple": "#7C4DFF",
    "pink": "#FF5C8A",
    "yellow": "#FFD54F",
    "green": "#21C982",
    "blue": "#36A9E1",
    "card_back": "#6C63FF",
    "card_open": "#FFFFFF",
    "text": "#34265E",
}

EMOJIS = [
    "🐶", "🐱", "🦊", "🐸", "🐼", "🦁", "🐯", "🐨",
    "🍎", "🍉", "🍓", "🍕", "🍩", "🌈", "⭐", "🚀",
    "⚽", "🎸", "🎨", "🎁", "🦄", "🌻", "🐳", "🦋",
    "🍦", "🎈", "🏀", "🌙", "☀️", "🍀", "💎", "🤖",
]


class HafizaOyunu:
    """Kart eşleştirme oyununun arayüzü ve oyun kuralları."""

    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("🌈 Renkli Kart Hafızası")
        self.pencere.configure(bg=COLORS["background"])
        self.pencere.minsize(650, 650)

        self.boyut = 4
        self.kartlar = []
        self.butons = []
        self.acik_kartlar = []
        self.eslesenler = set()
        self.hamle = 0
        self.kilitli = False
        self.zaman_id = None

        self._arayuzu_olustur()
        self.yeni_oyun()

    def _arayuzu_olustur(self):
        # HTML'deki başlık bölümü gibi üst bilgi paneli
        ust = tk.Frame(self.pencere, bg=COLORS["purple"], padx=18, pady=12)
        ust.pack(fill="x")

        baslik = tk.Label(
            ust, text="🌈  RENKLİ KART HAFIZASI  🧠",
            font=("Segoe UI Emoji", 22, "bold"),
            fg="white", bg=COLORS["purple"],
        )
        baslik.pack(side="left")

        tk.Button(
            ust, text="?", command=self.yardim_penceresi,
            font=("Arial", 18, "bold"), fg="white", bg=COLORS["pink"],
            activebackground="#E84B77", relief="flat", width=3, cursor="hand2",
        ).pack(side="right")

        bilgi = tk.Frame(self.pencere, bg=COLORS["background"], pady=10)
        bilgi.pack(fill="x")

        tk.Label(
            bilgi, text="Kaçlık oyun oynayalım?",
            font=("Arial", 13, "bold"), fg=COLORS["text"],
            bg=COLORS["background"],
        ).pack(side="left", padx=(20, 8))

        self.boyut_secim = tk.StringVar(value="4")
        for boyut in (4, 6, 8):
            tk.Radiobutton(
                bilgi, text=f"{boyut} × {boyut}", value=str(boyut),
                variable=self.boyut_secim, command=self.yeni_oyun,
                font=("Arial", 11, "bold"), fg=COLORS["text"],
                bg=COLORS["background"], activebackground=COLORS["background"],
                selectcolor=COLORS["yellow"], cursor="hand2",
            ).pack(side="left", padx=5)

        self.hamle_yazisi = tk.Label(
            bilgi, text="Hamle: 0", font=("Arial", 12, "bold"),
            fg=COLORS["pink"], bg=COLORS["background"],
        )
        self.hamle_yazisi.pack(side="right", padx=22)

        self.oyun_alani = tk.Frame(
            self.pencere, bg=COLORS["panel"], padx=12, pady=12,
        )
        self.oyun_alani.pack(expand=True, fill="both", padx=18, pady=(0, 18))

        self.durum = tk.Label(
            self.pencere, text="Kartları aç ve eşlerini bul! 🎯",
            font=("Arial", 13, "bold"), fg=COLORS["green"],
            bg=COLORS["background"], pady=8,
        )
        self.durum.pack(fill="x")

    def yeni_oyun(self):
        if self.zaman_id:
            self.pencere.after_cancel(self.zaman_id)
            self.zaman_id = None

        self.boyut = int(self.boyut_secim.get())
        cift_sayisi = (self.boyut * self.boyut) // 2
        deste = (EMOJIS[:cift_sayisi] * 2)
        random.shuffle(deste)
        self.kartlar = deste
        self.butons = []
        self.acik_kartlar = []
        self.eslesenler = set()
        self.hamle = 0
        self.kilitli = False
        self.hamle_yazisi.config(text="Hamle: 0")
        self.durum.config(text="Kartları aç ve eşlerini bul! 🎯", fg=COLORS["green"])

        for cocuk in self.oyun_alani.winfo_children():
            cocuk.destroy()

        for satir in range(self.boyut):
            self.oyun_alani.rowconfigure(satir, weight=1)
            for sutun in range(self.boyut):
                self.oyun_alani.columnconfigure(sutun, weight=1)
                indeks = satir * self.boyut + sutun
                buton = tk.Button(
                    self.oyun_alani, text="❓", command=lambda i=indeks: self.karta_tikla(i),
                    font=("Segoe UI Emoji", max(12, 30 - self.boyut * 2), "bold"),
                    bg=COLORS["card_back"], fg="white", activebackground="#8C83FF",
                    relief="raised", bd=4, cursor="hand2",
                )
                buton.grid(row=satir, column=sutun, sticky="nsew", padx=4, pady=4)
                self.butons.append(buton)

    def karta_tikla(self, indeks):
        if self.kilitli or indeks in self.acik_kartlar or indeks in self.eslesenler:
            return

        self.butons[indeks].config(
            text=self.kartlar[indeks], bg=COLORS["card_open"],
            fg=COLORS["text"], relief="sunken",
        )
        self.acik_kartlar.append(indeks)
        self._ses("tik")

        if len(self.acik_kartlar) == 2:
            self.hamle += 1
            self.hamle_yazisi.config(text=f"Hamle: {self.hamle}")
            self.kilitli = True
            self.zaman_id = self.pencere.after(650, self.eslesmeyi_kontrol_et)

    def eslesmeyi_kontrol_et(self):
        self.zaman_id = None
        ilk, ikinci = self.acik_kartlar
        if self.kartlar[ilk] == self.kartlar[ikinci]:
            self.eslesenler.update((ilk, ikinci))
            for indeks in (ilk, ikinci):
                self.butons[indeks].config(bg="#B9F6D3", relief="groove")
            self._ses("dogru")
            self.durum.config(text="Harika! Eşleşen kartı buldun! 🎉", fg=COLORS["green"])
        else:
            self._ses("yanlis")
            self.durum.config(text="Bu kartlar farklı. Tekrar dene! 💪", fg=COLORS["pink"])
            self.pencere.after(500, self.kartlari_kapat)
            return

        self.acik_kartlar = []
        self.kilitli = False
        if len(self.eslesenler) == len(self.kartlar):
            self._ses("kazandi")
            self.durum.config(text=f"Tebrikler! Oyunu {self.hamle} hamlede bitirdin! 🏆", fg=COLORS["purple"])

    def kartlari_kapat(self):
        for indeks in self.acik_kartlar:
            if indeks not in self.eslesenler:
                self.butons[indeks].config(text="❓", bg=COLORS["card_back"], fg="white", relief="raised")
        self.acik_kartlar = []
        self.kilitli = False

    def _ses(self, tur):
        """Doğru, yanlış ve kazanç durumlarında kısa zil sesleri çalar."""
        if winsound:
            frekans = {"tik": 650, "dogru": 1000, "yanlis": 250, "kazandi": 1400}.get(tur, 650)
            sure = 90 if tur != "kazandi" else 220
            winsound.Beep(frekans, sure)
        else:
            self.pencere.bell()

    def yardim_penceresi(self):
        pencere = tk.Toplevel(self.pencere)
        pencere.title("❓ Nasıl Oynanır?")
        pencere.configure(bg=COLORS["background"])
        pencere.resizable(False, False)
        pencere.transient(self.pencere)
        tk.Label(
            pencere, text="🎮 NASIL OYNANIR?", font=("Arial", 18, "bold"),
            fg="white", bg=COLORS["purple"], padx=25, pady=12,
        ).pack(fill="x")
        aciklama = (
            "1. Bir oyun boyutu seç: 4×4, 6×6 veya 8×8.\n\n"
            "2. Bir karta tıkla ve hangi emoji olduğunu gör.\n\n"
            "3. Aynı emojinin eşini bulmaya çalış.\n\n"
            "4. Eşleşirse kartlar açık kalır ve zil çalar.\n\n"
            "5. Eşleşmezse kartlar kapanır. Hatırlamaya çalış!\n\n"
            "Bütün çiftleri bulduğunda oyunu kazanırsın! 🏆"
        )
        tk.Label(
            pencere, text=aciklama, justify="left", font=("Arial", 12),
            fg=COLORS["text"], bg=COLORS["background"], padx=24, pady=18,
        ).pack()
        tk.Button(
            pencere, text="Anladım! 👍", command=pencere.destroy,
            font=("Arial", 11, "bold"), bg=COLORS["green"], fg="white",
            relief="flat", padx=18, pady=8, cursor="hand2",
        ).pack(pady=(0, 18))


if __name__ == "__main__":
    ana_pencere = tk.Tk()
    HafizaOyunu(ana_pencere)
    ana_pencere.mainloop()
