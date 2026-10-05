#list örneklerini içeren bir Python kodu
liste1 = [1, 2, 3, 4, 5]
print(liste1)  # [1, 2, 3, 4, 5] parçasını alır (listeyi yazdırır)
print(type(liste1))  # <class 'list'> parçasını alır (listenin veri tipini yazdırır)
print(len(liste1))  # 5 parçasını alır (listenin uzunluğunu yazdırır)
print(liste1[0])  # 1 parçasını alır (listenin ilk öğesini yazdırır)
print(liste1[-1])  # 5 parçasını alır (listenin son öğesini yazdırır)


print(liste1[2:5])  # [3, 4, 5] parçasını alır (listenin 2. ve 4. öğelerini yazdırır)
print(liste1[:3:-1])  # [5, 4, 3] parçasını alır (listenin son 3 öğesini tersten yazdırır)


renkler = ["kırmızı", "mavi", "yeşil", "sarı"]
print(renkler)  # ["kırmızı", "mavi", "yeşil", "sarı"] parçasını alır (listeyi yazdırır)
renkler.append("mor")  # listenin sonuna "mor" öğesini ekler
print(renkler)  # ["kırmızı", "mavi", "yeşil", "sarı", "mor"] parçasını alır (listeyi yazdırır)
