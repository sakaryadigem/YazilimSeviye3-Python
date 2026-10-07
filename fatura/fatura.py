import argparse
import json
from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Sequence


DATA_FILE = Path(__file__).with_name("fatura.json")
MONEY_FIELDS = {
    "Birim Fiyat",
    "Tüketim Ücreti",
    "Sabit Ücret",
    "Vergi",
    "Toplam Fatura",
}
MONTH_NAMES = (
    "Ocak",
    "Şubat",
    "Mart",
    "Nisan",
    "Mayıs",
    "Haziran",
    "Temmuz",
    "Ağustos",
    "Eylül",
    "Ekim",
    "Kasım",
    "Aralık",
)


def load_invoices() -> list[dict[str, Any]]:
    """Faturaları, kuruş hassasiyetini koruyarak JSON dosyasından yükler."""
    with DATA_FILE.open(encoding="utf-8") as file:
        invoices = json.load(file, parse_float=Decimal)

    if not isinstance(invoices, list):
        raise ValueError("fatura.json dosyasının kök verisi bir liste olmalıdır.")
    if not all(isinstance(invoice, dict) for invoice in invoices):
        raise ValueError("fatura.json içinde geçersiz fatura kaydı bulundu.")
    return invoices


def format_amount(amount: Decimal | int | float) -> str:
    """Tutarı Türkçe sayı biçiminde gösterir."""
    formatted = f"{amount:,.2f}"
    return formatted.replace(",", "_").replace(".", ",").replace("_", ".")


def get_total(invoice: dict[str, Any]) -> Decimal:
    return Decimal(str(invoice["Toplam Fatura"]))


def get_consumption(invoice: dict[str, Any]) -> int:
    return int(invoice["Tüketim Miktarı"])


def get_invoice_date(invoice: dict[str, Any]) -> datetime:
    return datetime.strptime(invoice["Tarih"], "%d.%m.%Y")


def print_summary(invoices: list[dict[str, Any]]) -> None:
    if not invoices:
        print("Özetlenecek fatura bulunamadı.")
        return

    grouped: dict[tuple[str, str], dict[str, Decimal | int]] = defaultdict(
        lambda: {"count": 0, "consumption": 0, "total": Decimal("0.00")}
    )
    for invoice in invoices:
        key = (str(invoice["İl"]), str(invoice["Fatura Tipi"]))
        grouped[key]["count"] += 1
        grouped[key]["consumption"] += get_consumption(invoice)
        grouped[key]["total"] += get_total(invoice)

    print("\nGenel Fatura Özeti")
    print("-" * 76)
    print(f"{'İl':<16} {'Fatura Tipi':<14} {'Adet':>6} {'Tüketim':>12} {'Toplam Tutar':>18}")
    print("-" * 76)

    for (city, invoice_type), values in sorted(grouped.items()):
        total = values["total"]
        print(
            f"{city:<16} {invoice_type:<14} {values['count']:>6} "
            f"{values['consumption']:>12} {format_amount(total):>15} TL"
        )

    print("-" * 76)
    total_amount = sum((get_total(invoice) for invoice in invoices), Decimal("0.00"))
    total_consumption = sum(get_consumption(invoice) for invoice in invoices)
    print(
        f"Genel toplam: {len(invoices)} fatura, "
        f"{total_consumption} tüketim, {format_amount(total_amount)} TL"
    )


def show_invoice_detail(invoices: list[dict[str, Any]]) -> None:
    # strip kullanımı ile kullanıcıdan alınan fatura numarasının başındaki ve sonundaki boşluklar temizlenir
    invoice_number = input("Fatura numarasını girin: ").strip()
    invoice = next(
        (
            item
            for item in invoices
            if str(item.get("Fatura No", "")).casefold() == invoice_number.casefold()
        ),
        None,
    )
    if invoice is None:
        print(f"'{invoice_number}' numaralı fatura bulunamadı.")
        return

    print("\nFatura Detayı")
    print("-" * 40)
    for field, value in invoice.items():
        if field in MONEY_FIELDS:
            print(f"{field}: {format_amount(Decimal(str(value)))} TL")
        else:
            print(f"{field}: {value}")


def select_from_list(title: str, options: list[str]) -> int | None:
    # Kullanıcıya bir liste sunar ve seçim yapmasını ister. Seçim geçerliyse seçilen indeks döndürülür, aksi halde None döndürülür.
    if not options:
        print("Seçilebilecek kayıt bulunamadı.")
        return None

    print(f"\n{title}")
    for index, option in enumerate(options, start=1):
        print(f"{index}) {option}")

    while True:
        choice = input("Seçim ID'sini girin: ").strip()
        try:
            selected_index = int(choice)
        except ValueError:
            print("Lütfen listede bulunan sayısal bir ID girin.")
            continue

        if 1 <= selected_index <= len(options):
            return selected_index - 1
        print(f"ID, 1 ile {len(options)} arasında olmalıdır.")


def show_city_summary(invoices: list[dict[str, Any]]) -> None:
    cities = sorted({str(invoice["İl"]) for invoice in invoices})
    selected_index = select_from_list("İller", cities)
    if selected_index is None:
        return

    city = cities[selected_index]
    city_invoices = [invoice for invoice in invoices if invoice["İl"] == city]
    print(f"\n{city} İlçe ve Fatura Tipi Özeti")
    print_summary(city_invoices)

    districts = sorted({str(invoice["İlçe"]) for invoice in city_invoices})
    print("\nİlçe Bazında")
    for district in districts:
        district_invoices = [
            invoice for invoice in city_invoices if invoice["İlçe"] == district
        ]
        district_total = sum(
            (get_total(invoice) for invoice in district_invoices), Decimal("0.00")
        )
        print(
            f"{district}: {len(district_invoices)} fatura, "
            f"{format_amount(district_total)} TL"
        )


def show_period_summary(invoices: list[dict[str, Any]]) -> None:
    periods = sorted({get_invoice_date(invoice).strftime("%Y-%m") for invoice in invoices})
    period_labels = [
        f"{MONTH_NAMES[int(period[5:7]) - 1]} {period[:4]}" for period in periods
    ]
    selected_index = select_from_list("Dönemler", period_labels)
    if selected_index is None:
        return

    selected_period = periods[selected_index]
    period_invoices = [
        invoice
        for invoice in invoices
        if get_invoice_date(invoice).strftime("%Y-%m") == selected_period
    ]
    print(f"\n{period_labels[selected_index]} Dönem Özeti")
    print_summary(period_invoices)


def print_menu() -> None:
    print(
        "\nFatura Uygulaması\n"
        "1) Genel özet ver\n"
        "2) Fatura numarasına göre detay ver\n"
        "3) İl bazlı detaylı özet\n"
        "4) Dönem özeti\n"
        "5) Çıkış"
    )


def run_option(option: str, invoices: list[dict[str, Any]]) -> bool:
    if option == "1":
        print_summary(invoices)
    elif option == "2":
        show_invoice_detail(invoices)
    elif option == "3":
        show_city_summary(invoices)
    elif option == "4":
        show_period_summary(invoices)
    elif option == "5":
        print("Uygulamadan çıkılıyor.")
        return False
    return True


def main(argv: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Fatura verilerini özetler ve görüntüler.")
    parser.add_argument(
        "option",
        nargs="?",
        choices=("1", "2", "3", "4", "5"),
        help="Menü seçeneği (1-5). Verilmezse etkileşimli menü açılır.",
    )
    args = parser.parse_args(argv)

    try:
        invoices = load_invoices()
    except (OSError, json.JSONDecodeError, ValueError) as error:
        parser.error(f"Faturalar yüklenemedi: {error}")

    if args.option is not None:
        run_option(args.option, invoices)
        return

    while True:
        print_menu()
        option = input("Seçiminiz (1-5): ").strip()
        if option not in {"1", "2", "3", "4", "5"}:
            print("Geçersiz seçim. Lütfen 1 ile 5 arasında bir seçenek girin.")
            continue
        if not run_option(option, invoices):
            break


if __name__ == "__main__":
    main()