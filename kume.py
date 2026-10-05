#Küme içeren bir örnek Python kodu:
#renkler = {"kırmızı", "mavi", "yeşil", "sarı", "mor"}
#print(renkler)  # {"kırmızı", "mavi", "yeşil", "sarı", "mor"} parçasını alır (küme'yi yazdırır)
#print(type(renkler))  # <class 'set'> parçasını alır (küme'ın veri tipini yazdırır)


#renkler.add("turuncu")  # Küme'ye yeni bir renk ekler
#print(renkler)  # {"kırmızı", "mavi", "yeşil", "sarı", "mor", "turuncu"} parçasını alır (güncellenmiş küme'yi yazdırır)
#renkler.remove("mavi")  # Küme'den bir renk çıkarır
#print(renkler)  # {"kırmızı", "yeşil", "sarı", "mor", "turuncu"} parçasını alır (güncellenmiş küme'yi yazdırır) 

#renkler.discard("gri")  # Küme'de olmayan bir öğeyi çıkarmaya çalışır, hata vermez  
#print(renkler)  # {"kırmızı", "yeşil", "sarı", "mor", "turuncu"} parçasını alır (güncellenmiş küme'yi yazdırır) 

#kume1 = {"kırmızı", "mavi", "yeşil"}
#kume2 = {"sarı", "mor", "yeşil"}
#kume3 = kume1.union(kume2)  # İki kümenin birleşimini alır
#print(kume3)  # {"kırmızı", "mavi", "yeşil", "sarı", "mor"} parçasını alır (iki kümenin birleşimi)
#kume4 = kume1.intersection(kume2)  # İki kümenin kesişimini alır
#print(kume4)  # {"yeşil"} parçasını alır (iki kümenin kesişimi) 


deneme_kume = set("Python")  # Bir string'den küme oluşturur
print(deneme_kume)  # {'P', 'y', 't', 'h', 'o', 'n'} parçasını alır (string'den oluşturulan küme)

deneme_kume2 = set([1, 2, 3, 4, 5])  # Bir liste'den küme oluşturur
print(deneme_kume2)  # {1, 2, 3, 4, 5} parçasını alır (liste'den oluşturulan küme)

deneme_kume3 = set((1, 2, 3, 4, 5))  # Bir tuple'dan küme oluşturur
print(deneme_kume3)  # {1, 2, 3, 4, 5} parçasını alır (tuple'dan oluşturulan küme)




