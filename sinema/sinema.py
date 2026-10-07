import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk


DATA_DIR = Path(__file__).resolve().parent


def read_json(filename, default):
    path = DATA_DIR / filename
    try:
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        write_json(filename, default)
        return default


def write_json(filename, data):
    with (DATA_DIR / filename).open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


@dataclass
class Film:
    id: str
    ad: str
    tur: str
    sure: int
    vizyon_tarihi: str


@dataclass
class Salon:
    id: str
    numara: int
    satir: int
    sutun: int

    @property
    def kapasite(self):
        return self.satir * self.sutun

    def koltuk_matrisi(self, dolu_koltuklar=None):
        dolu_koltuklar = set(dolu_koltuklar or [])
        return [
            [f"{chr(65 + row)}{col + 1}" in dolu_koltuklar
             for col in range(self.sutun)]
            for row in range(self.satir)
        ]


@dataclass
class Bilet:
    id: str
    seans_id: str
    film_id: str
    salon_id: str
    koltuk: str
    musteri: str
    fiyat: float
    satis_zamani: str


class SinemaVeri:
    """JSON dosyaları ile uygulama nesneleri arasındaki veri katmanı."""

    def __init__(self):
        self.filmler = [Film(**item) for item in read_json("filmler.json", [])]
        self.salonlar = [Salon(**item) for item in read_json("salonlar.json", [])]
        self.seanslar = read_json("seanslar.json", [])
        self.biletler = [Bilet(**item) for item in read_json("biletler.json", [])]

    def kaydet(self):
        write_json("filmler.json", [asdict(item) for item in self.filmler])
        write_json("salonlar.json", [asdict(item) for item in self.salonlar])
        write_json("seanslar.json", self.seanslar)
        write_json("biletler.json", [asdict(item) for item in self.biletler])

    def film(self, film_id):
        return next((item for item in self.filmler if item.id == film_id), None)

    def salon(self, salon_id):
        return next((item for item in self.salonlar if item.id == salon_id), None)

    def seans_etiketi(self, seans):
        film = self.film(seans["film_id"])
        salon = self.salon(seans["salon_id"])
        return f'{film.ad} | {seans["tarih"]} {seans["saat"]} | Salon {salon.numara}'

    def dolu_koltuklar(self, seans_id):
        return {ticket.koltuk for ticket in self.biletler if ticket.seans_id == seans_id}

    def seans_biletleri(self, seans_id):
        return [ticket for ticket in self.biletler if ticket.seans_id == seans_id]

    def bilet_sat(self, seans, koltuk, musteri):
        if koltuk in self.dolu_koltuklar(seans["id"]):
            raise ValueError("Bu koltuk zaten dolu.")
        salon = self.salon(seans["salon_id"])
        valid = {f"{chr(65 + row)}{col + 1}" for row in range(salon.satir)
                 for col in range(salon.sutun)}
        if koltuk not in valid:
            raise ValueError("Geçersiz koltuk numarası.")
        self.biletler.append(Bilet(
            id=uuid.uuid4().hex[:8], seans_id=seans["id"],
            film_id=seans["film_id"], salon_id=seans["salon_id"],
            koltuk=koltuk, musteri=musteri.strip(), fiyat=float(seans["fiyat"]),
            satis_zamani=datetime.now().strftime("%Y-%m-%d %H:%M")))
        self.kaydet()

    def bilet_iptal(self, bilet_id):
        self.biletler = [ticket for ticket in self.biletler if ticket.id != bilet_id]
        self.kaydet()


class SinemaUygulamasi(tk.Tk):
    BG = "#111827"
    PANEL = "#1f2937"
    TEXT = "#f9fafb"
    MUTED = "#9ca3af"
    ACCENT = "#f59e0b"

    def __init__(self):
        super().__init__()
        self.title("Perde Yönetim Sistemi")
        self.geometry("1120x720")
        self.minsize(950, 620)
        self.configure(bg=self.BG)
        self.data = SinemaVeri()
        self.selected_seans = None
        self.seat_buttons = {}
        self._style()
        self._build()
        self.refresh_all()

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook", background=self.BG, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.PANEL, foreground=self.TEXT,
                        padding=(18, 10), font=("Segoe UI", 10, "bold"))
        style.map("TNotebook.Tab", background=[("selected", self.ACCENT)],
                  foreground=[("selected", "#111827")])
        style.configure("Treeview", background="#172033", fieldbackground="#172033",
                        foreground=self.TEXT, rowheight=30, borderwidth=0)
        style.configure("Treeview.Heading", background="#374151", foreground=self.TEXT)
        style.configure("TCombobox", fieldbackground="#374151", foreground=self.TEXT)
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=7)

    def _build(self):
        header = tk.Frame(self, bg=self.BG)
        header.pack(fill="x", padx=28, pady=(24, 8))
        tk.Label(header, text="PERDE", bg=self.BG, fg=self.ACCENT,
                 font=("Segoe UI", 25, "bold")).pack(side="left")
        tk.Label(header, text="  Sinema Yönetim Sistemi", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 18)).pack(side="left", pady=4)
        self.status = tk.Label(header, text="", bg=self.BG, fg=self.MUTED,
                               font=("Segoe UI", 10))
        self.status.pack(side="right", pady=8)

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=22, pady=(8, 22))
        self.sales_tab = tk.Frame(self.tabs, bg=self.BG)
        self.management_tab = tk.Frame(self.tabs, bg=self.BG)
        self.report_tab = tk.Frame(self.tabs, bg=self.BG)
        self.tabs.add(self.sales_tab, text="  Bilet Satışı  ")
        self.tabs.add(self.management_tab, text="  Film / Seans Yönetimi  ")
        self.tabs.add(self.report_tab, text="  Kasa ve Rapor  ")
        self._build_sales()
        self._build_management()
        self._build_report()

    def _build_sales(self):
        left = tk.Frame(self.sales_tab, bg=self.PANEL, padx=18, pady=18)
        left.pack(side="left", fill="y", padx=(0, 16), pady=4)
        tk.Label(left, text="Seans seçin", bg=self.PANEL, fg=self.TEXT,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")
        self.session_var = tk.StringVar()
        self.session_combo = ttk.Combobox(left, textvariable=self.session_var,
                                          state="readonly", width=38)
        self.session_combo.pack(pady=(10, 22))
        self.session_combo.bind("<<ComboboxSelected>>", self.select_session)
        tk.Label(left, text="Müşteri adı", bg=self.PANEL, fg=self.MUTED).pack(anchor="w")
        self.customer_entry = tk.Entry(left, bg="#374151", fg=self.TEXT,
                                       insertbackground=self.TEXT, relief="flat", width=32)
        self.customer_entry.pack(pady=(6, 14), ipady=7)
        self.selected_label = tk.Label(left, text="Koltuk: -", bg=self.PANEL,
                                       fg=self.ACCENT, font=("Segoe UI", 12, "bold"))
        self.selected_label.pack(anchor="w", pady=5)
        tk.Button(left, text="Bileti Sat", command=self.sell_ticket, bg=self.ACCENT,
                  fg="#111827", relief="flat", cursor="hand2", width=27).pack(pady=15)
        tk.Label(left, text="Yeşil: boş   Kırmızı: dolu\nSeçmek için koltuğa tıklayın",
                 justify="left", bg=self.PANEL, fg=self.MUTED).pack(anchor="w", pady=15)

        self.seats_frame = tk.Frame(self.sales_tab, bg=self.BG)
        self.seats_frame.pack(side="left", fill="both", expand=True, pady=4)
        self.seat_title = tk.Label(self.seats_frame, text="Bir seans seçin", bg=self.BG,
                                   fg=self.TEXT, font=("Segoe UI", 15, "bold"))
        self.seat_title.pack(pady=(28, 15))
        self.seat_grid = tk.Frame(self.seats_frame, bg=self.BG)
        self.seat_grid.pack()

    def _build_management(self):
        self.management_tab.columnconfigure(0, weight=1)
        self.management_tab.columnconfigure(1, weight=1)
        movie = tk.LabelFrame(self.management_tab, text="Yeni film ekle", bg=self.PANEL,
                              fg=self.TEXT, padx=16, pady=16)
        movie.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=4)
        self.movie_fields = {}
        for row, (key, label) in enumerate([("ad", "Film adı"), ("tur", "Tür"),
                                             ("sure", "Süre (dakika)"),
                                             ("vizyon_tarihi", "Vizyon tarihi")]):
            tk.Label(movie, text=label, bg=self.PANEL, fg=self.MUTED).grid(row=row, column=0, sticky="w", pady=6)
            entry = tk.Entry(movie, bg="#374151", fg=self.TEXT, insertbackground=self.TEXT,
                             relief="flat", width=30)
            entry.grid(row=row, column=1, padx=12, ipady=5)
            self.movie_fields[key] = entry
        tk.Button(movie, text="Filmi Kaydet", command=self.add_movie, bg=self.ACCENT,
                  fg="#111827", relief="flat").grid(row=4, column=1, sticky="e", pady=14)

        show = tk.LabelFrame(self.management_tab, text="Yeni seans tanımla", bg=self.PANEL,
                             fg=self.TEXT, padx=16, pady=16)
        show.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=4)
        self.show_fields = {}
        for row, key in enumerate(["film_id", "salon_id", "tarih", "saat", "fiyat"]):
            label = {"film_id": "Film", "salon_id": "Salon", "tarih": "Tarih (YYYY-AA-GG)",
                     "saat": "Saat", "fiyat": "Bilet fiyatı"}[key]
            tk.Label(show, text=label, bg=self.PANEL, fg=self.MUTED).grid(row=row, column=0, sticky="w", pady=6)
            if key in ("film_id", "salon_id"):
                var = tk.StringVar()
                widget = ttk.Combobox(show, textvariable=var, state="readonly", width=27)
                self.show_fields[key] = (var, widget)
            else:
                widget = tk.Entry(show, bg="#374151", fg=self.TEXT, insertbackground=self.TEXT,
                                  relief="flat", width=30)
                self.show_fields[key] = widget
            widget.grid(row=row, column=1, padx=12, ipady=4)
        tk.Button(show, text="Seansı Kaydet", command=self.add_session, bg=self.ACCENT,
                  fg="#111827", relief="flat").grid(row=5, column=1, sticky="e", pady=14)
        self.session_list = tk.Listbox(self.management_tab, bg="#172033", fg=self.TEXT,
                                       relief="flat", height=12)
        self.session_list.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(16, 0))
        self.management_tab.rowconfigure(1, weight=1)

    def _build_report(self):
        self.stats = {}
        for col, (key, label) in enumerate([("count", "Satılan bilet"), ("revenue", "Toplam hasılat")]):
            card = tk.Frame(self.report_tab, bg=self.PANEL, padx=25, pady=20)
            card.grid(row=0, column=col, sticky="ew", padx=(0, 12) if col == 0 else (12, 0), pady=10)
            tk.Label(card, text=label, bg=self.PANEL, fg=self.MUTED,
                     font=("Segoe UI", 11)).pack(anchor="w")
            self.stats[key] = tk.Label(card, text="0", bg=self.PANEL, fg=self.ACCENT,
                                       font=("Segoe UI", 27, "bold"))
            self.stats[key].pack(anchor="w", pady=(8, 0))
        self.report_tab.columnconfigure(0, weight=1)
        self.report_tab.columnconfigure(1, weight=1)
        tk.Label(self.report_tab, text="Satış kayıtları", bg=self.BG, fg=self.TEXT,
                 font=("Segoe UI", 14, "bold")).grid(row=1, column=0, columnspan=2, sticky="w", pady=(20, 8))
        columns = ("id", "film", "seans", "koltuk", "musteri", "fiyat")
        self.ticket_tree = ttk.Treeview(self.report_tab, columns=columns, show="headings")
        heads = {"id": "No", "film": "Film", "seans": "Seans", "koltuk": "Koltuk",
                 "musteri": "Müşteri", "fiyat": "Fiyat"}
        for column in columns:
            self.ticket_tree.heading(column, text=heads[column])
            self.ticket_tree.column(column, width=120)
        self.ticket_tree.grid(row=2, column=0, columnspan=2, sticky="nsew")
        tk.Button(self.report_tab, text="Seçili bileti iptal et", command=self.cancel_ticket,
                  bg="#dc2626", fg="white", relief="flat").grid(row=3, column=1, sticky="e", pady=12)
        self.report_tab.rowconfigure(2, weight=1)

    def refresh_all(self):
        labels = [self.data.seans_etiketi(item) for item in self.data.seanslar]
        self.session_combo["values"] = labels
        self.session_map = dict(zip(labels, self.data.seanslar))
        film_values = [f"{item.id} - {item.ad}" for item in self.data.filmler]
        self.show_fields["film_id"][1]["values"] = film_values
        salon_values = [f"{item.id} - Salon {item.numara}" for item in self.data.salonlar]
        self.show_fields["salon_id"][1]["values"] = salon_values
        self.session_list.delete(0, tk.END)
        for item in self.data.seanslar:
            self.session_list.insert(tk.END, self.data.seans_etiketi(item) + f' | {item["fiyat"]:.2f} TL')
        self.refresh_report()
        if self.selected_seans:
            self.draw_seats()

    def select_session(self, _event=None):
        self.selected_seans = self.session_map.get(self.session_var.get())
        self.draw_seats()

    def draw_seats(self):
        for widget in self.seat_grid.winfo_children():
            widget.destroy()
        if not self.selected_seans:
            return
        film = self.data.film(self.selected_seans["film_id"])
        salon = self.data.salon(self.selected_seans["salon_id"])
        self.seat_title.config(text=f"{film.ad}  •  Salon {salon.numara}  •  {self.selected_seans['saat']}")
        tk.Label(self.seat_grid, text="PERDE", bg="#374151", fg=self.TEXT,
                 font=("Segoe UI", 10, "bold"), width=45, pady=6).grid(row=0, column=0, columnspan=salon.sutun + 1, pady=(0, 22))
        self.seat_buttons = {}
        occupied = self.data.dolu_koltuklar(self.selected_seans["id"])
        for row in range(salon.satir):
            tk.Label(self.seat_grid, text=chr(65 + row), bg=self.BG, fg=self.MUTED,
                     width=3).grid(row=row + 1, column=0)
            for col in range(salon.sutun):
                seat = f"{chr(65 + row)}{col + 1}"
                button = tk.Button(self.seat_grid, text=seat, width=7, height=2,
                                   relief="flat", command=lambda s=seat: self.choose_seat(s))
                button.grid(row=row + 1, column=col + 1, padx=5, pady=5)
                button.config(bg="#dc2626" if seat in occupied else "#16a34a",
                              fg="white", state="disabled" if seat in occupied else "normal")
                self.seat_buttons[seat] = button

    def choose_seat(self, seat):
        self.selected_label.config(text=f"Koltuk: {seat}")
        for name, button in self.seat_buttons.items():
            if button["state"] != "disabled":
                button.config(bg="#2563eb" if name == seat else "#16a34a")

    def sell_ticket(self):
        if not self.selected_seans:
            messagebox.showwarning("Eksik bilgi", "Önce bir seans seçin.")
            return
        seat = self.selected_label.cget("text").replace("Koltuk: ", "")
        customer = self.customer_entry.get().strip()
        if seat == "-" or not customer:
            messagebox.showwarning("Eksik bilgi", "Koltuk ve müşteri adı girin.")
            return
        try:
            self.data.bilet_sat(self.selected_seans, seat, customer)
        except ValueError as error:
            messagebox.showerror("Satış yapılamadı", str(error))
            return
        messagebox.showinfo("Başarılı", f"{seat} koltuğu için bilet satıldı.")
        self.customer_entry.delete(0, tk.END)
        self.selected_label.config(text="Koltuk: -")
        self.refresh_all()

    def add_movie(self):
        values = {key: entry.get().strip() for key, entry in self.movie_fields.items()}
        if not all(values.values()):
            messagebox.showwarning("Eksik bilgi", "Tüm film alanlarını doldurun.")
            return
        try:
            values["sure"] = int(values["sure"])
        except ValueError:
            messagebox.showerror("Hatalı bilgi", "Süre sayı olmalıdır.")
            return
        self.data.filmler.append(Film(id="film_" + uuid.uuid4().hex[:6], **values))
        self.data.kaydet()
        for entry in self.movie_fields.values(): entry.delete(0, tk.END)
        self.refresh_all()
        messagebox.showinfo("Başarılı", "Film kaydedildi.")

    def add_session(self):
        film_value = self.show_fields["film_id"][0].get()
        salon_value = self.show_fields["salon_id"][0].get()
        values = {"tarih": self.show_fields["tarih"].get().strip(),
                  "saat": self.show_fields["saat"].get().strip(),
                  "fiyat": self.show_fields["fiyat"].get().strip()}
        if not film_value or not salon_value or not all(values.values()):
            messagebox.showwarning("Eksik bilgi", "Tüm seans alanlarını doldurun.")
            return
        try:
            datetime.strptime(values["tarih"], "%Y-%m-%d")
            values["fiyat"] = float(values["fiyat"])
        except ValueError:
            messagebox.showerror("Hatalı bilgi", "Tarih YYYY-AA-GG, fiyat sayı olmalıdır.")
            return
        self.data.seanslar.append({"id": "seans_" + uuid.uuid4().hex[:6],
                                  "film_id": film_value.split(" - ")[0],
                                  "salon_id": salon_value.split(" - ")[0], **values})
        self.data.kaydet()
        self.refresh_all()
        messagebox.showinfo("Başarılı", "Seans kaydedildi.")

    def refresh_report(self):
        self.stats["count"].config(text=str(len(self.data.biletler)))
        self.stats["revenue"].config(text=f"{sum(item.fiyat for item in self.data.biletler):,.2f} TL")
        for row in self.ticket_tree.get_children(): self.ticket_tree.delete(row)
        for ticket in self.data.biletler:
            seans = next((item for item in self.data.seanslar if item["id"] == ticket.seans_id), None)
            film = self.data.film(ticket.film_id)
            self.ticket_tree.insert("", "end", iid=ticket.id,
                                    values=(ticket.id, film.ad if film else "-",
                                            f'{seans["tarih"]} {seans["saat"]}' if seans else "-",
                                            ticket.koltuk, ticket.musteri, f"{ticket.fiyat:.2f} TL"))

    def cancel_ticket(self):
        selected = self.ticket_tree.selection()
        if not selected:
            messagebox.showwarning("Seçim yok", "İptal etmek için bir bilet seçin.")
            return
        if messagebox.askyesno("Bilet iptali", "Seçili bilet iptal edilsin mi?"):
            self.data.bilet_iptal(selected[0])
            self.refresh_all()


if __name__ == "__main__":
    SinemaUygulamasi().mainloop()
