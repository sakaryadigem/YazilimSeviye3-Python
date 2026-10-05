#pythonda fonksiyon kullanım örneği içeren python kodu
def merhaba(isim, yas):
    print("**"*32)
    print("**"*32)
    print(f"Merhaba, {isim}! {yas} yaşındasın.")
    print("**"*32)
    print("**"*32)

isim = input("İsminizi giriniz: ")
yas = int(input("Yaşınızı giriniz: "))


merhaba(isim, yas)