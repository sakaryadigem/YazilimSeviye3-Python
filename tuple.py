#Tuple (Demet) örneklerini içeren bir Python kodu
#Tuple, birden fazla öğeyi tek bir değişkende saklamamıza olanak tanır ve bu öğeler farklı veri tiplerinden olabilir. Tuple'lar parantezler () ile tanımlanır ve öğeler virgülle ayrılır. Tuple'lar değiştirilemez (immutable) veri yapılarıdır, yani bir kez oluşturulduktan sonra öğeleri değiştirilemez.
#Örnek bir tuple oluşturma
renkler = ("kırmızı", "mavi", "yeşil", "sarı", "mor")
print(renkler)  # ("kırmızı", "mavi", "yeşil", "sarı", "mor") parçasını alır (tuple'ı yazdırır)
print(type(renkler))  # <class 'tuple'> parçasını alır (tuple'ın veri tipini yazdırır)
print(len(renkler))  # 5 parçasını alır (tuple'ın uzunluğunu yazdırır)
print(renkler[0])  # "kırmızı" parçasını alır (tuple'ın ilk öğesini yazdırır)
print(renkler[-1])  # "mor" parçasını alır (tuple'ın son öğesini yazdırır)
renkler[2] = "turuncu"  # TypeError: 'tuple' object does not support item assignment hatası verir (tuple'lar değiştirilemez)    
