#Matematiksel işlemler
import math

sayi1 = 10
sayi2 = 3
sayi3 = -5
sayi4 = 81
toplam  = sayi1 + sayi2
fark    = sayi1 - sayi2
carpim  = sayi1 * sayi2
bolum   = round(sayi1 / sayi2, 2)
kalan   = sayi1 % sayi2
mutlak_deger = abs(sayi3)
karekok = math.sqrt(sayi4)  # veya math.sqrt(sayi4)


print("Toplam: " + str(toplam))
print("Fark:   " + str(fark))     
print("Çarpım: " + str(carpim))
print("Bölüm: " + str(bolum))
print("Kalan: " + str(kalan))
print("Mutlak Değer: " + str(mutlak_deger))
print("Karekök: " + str(karekok))


print("Minimum Değer: " + str(min(sayi1, sayi2, sayi3, sayi4))) #minimum değer
print("Maximum Değer: " + str(max(sayi1, sayi2, sayi3, sayi4))) #maximum değer   
print("Ortalama Değer: " + str(avg := (sayi1 + sayi2 + sayi3 + sayi4) / 4)) #ortalama değer