#Döngüler
renkler = ["kırmızı", "mavi", "yeşil", "sarı", "mor"]

#for döngüsü ile liste öğelerini yazdırma
#for i in renkler:
#    print(i)  # listenin öğelerini tek tek yazdırır
#liste2 = sorted(renkler, reverse=True)  # listenin öğelerini tersine çevirir ve listeyi günceller
#print(renkler)  # ["mor", "sarı", "yeşil", "mavi", "kırmızı"] parçasını alır (listeyi yazdırır)
#print(liste2)  # ["mor", "sarı", "yeşil", "mavi", "kırmızı"] parçasını alır (tersine çevrilmiş listeyi yazdırır)
#print(min(renkler))  # "kırmızı" parçasını alır (listenin alfabetik olarak en küçük öğesini yazdırır   )
#print(max(renkler))  # "sarı" parçasını alır (listenin alfabetik olarak en büyük öğesini yazdırır  )
#renkler2 = renkler + [1]   # listenin sonuna 1 öğesini ekler
#print(renkler2[-1])  # 1 parçasını alır (listenin son öğesini yazdırır)

#print(sum([1, 2, 3, 4, 5]))  # 15 parçasını alır (listenin öğelerinin toplamını yazdırır)
#print(sum([1.5, 2.5, 3.5]))  # 7.5 parçasını alır (listenin öğelerinin toplamını yazdırır)
#print(sum([1, 2, 3], 10))  # 16 parçasını alır (listenin öğelerinin toplamını yazdırır ve başlangıç değerini ekler)
#print(sum([1, 2, 3], -5))  # 1 parçasını alır (listenin öğelerinin toplamını yazdırır ve başlangıç değerini ekler)
#print(sum([1, 2, 3], renkler2[-1]))  # 2 parçasını alır (listenin öğelerinin toplamını yazdırır ve başlangıç değerini ekler)
#print(list(enumerate(renkler)))  # [(0, 'kırmızı'), (1, 'mavi'), (2, 'yeşil'), (3, 'sarı'), (4, 'mor')] parçasını alır (listenin öğelerini indeksleri ile birlikte yazdırır)
#print(list(enumerate(renkler, start=1)))  # [(1, 'kırmızı'), (2, 'mavi'), (3, 'yeşil'), (4, 'sarı'), (5, 'mor')] parçasını alır (listenin öğelerini indeksleri ile birlikte yazdırır ve indeksleri 1'den başlatır)
#print(list(enumerate(renkler, start=5)))  # [(5, 'kırmızı'), (6, 'mavi'), (7, 'yeşil'), (8, 'sarı'), (9, 'mor')] parçasını alır (listenin öğelerini indeksleri ile birlikte yazdırır ve indeksleri 5'ten başlatır)
#print("sarı" in renkler)  # True parçasını alır (listenin içinde "sarı" öğesi var mı yok mu kontrol eder)
#print(15 in renkler)  # True parçasını alır (listenin içinde 5 öğesi var mı yok mu kontrol eder)


renkler = ["kırmızı", "mavi", "yeşil", "sarı", "mor"]

str_renkler = "".join(renkler) #listenin öğelerini birleştirir ve bir string oluşturur
#print(str_renkler)  # "kırmızımavizeşilsarımor" parçasını alır (birleştirilmiş stringi yazdırır) 
str_renkler2 = "-".join(renkler) #listenin öğelerini birleştirir ve bir string oluşturur
#print(str_renkler2)  # "kırmızı-mavi-yeşil-sarı-mor" parçasını alır (birleştirilmiş stringi yazdırır)
str_renkler3 = ", ".join(renkler) #listenin öğelerini birleştirir ve bir string oluşturur
#print(str_renkler3)  # "kırmızı, mavi, yeşil, sarı, mor" parçasını alır (birleştirilmiş stringi yazdırır)

for i in str_renkler.split("ı"):  # birleştirilmiş stringi parçalar ve listeye dönüştürür
    print(i)  # listenin öğelerini tek tek yazdırır

for i in str_renkler2.split("-"):  # birleştirilmiş stringi parçalar ve listeye dönüştürür
    print(i.upper()) # listenin öğelerini tek tek büyük harfe çevirerek yazdırır

for i in str_renkler3.split(", "):  # birleştirilmiş stringi parçalar ve listeye dönüştürür
    print(i)  # listenin öğelerini tek tek yazdırır


   

