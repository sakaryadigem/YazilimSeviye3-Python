#Pythonda listeler ile çalışmak için kullanılan temel veri yapısıdır. Listeler, birden fazla öğeyi tek bir değişkende saklamamıza olanak tanır ve bu öğeler farklı veri tiplerinden olabilir. Listeler köşeli parantezler [] ile tanımlanır ve öğeler virgülle ayrılır.
#Örnek bir liste oluşturma  
renkler = ["kırmızı", "mavi", "yeşil", "sarı"]
sayi = [2, 3, 1,  4, 5]
#print(renkler)  # ["kırmızı", "mavi", "yeşil", "sarı"] parçasını alır (listeyi yazdırır)
#print(type(renkler))  # <class 'list'> parçasını alır (listenin veri tipini yazdırır)
#print(len(renkler))  # 4 parçasını alır (listenin uzunluğunu yazdırır)
#print(renkler[0])  # "kırmızı" parçasını alır (listenin ilk öğesini yazdırır)

#print(renkler[-1])  # "sarı" parçasını alır (listenin son öğesini yazdırır)
#print(renkler[1:3])  # ["mavi", "yeşil"] parçasını alır (listenin 1. ve 2. öğelerini yazdırır)
#print(renkler[::2])  # ["kırmızı", "yeşil"] parçasını alır (listenin her 2. öğesini yazdırır)

#print(renkler[::-1])  # ["sarı", "yeşil", "mavi", "kırmızı"] parçasını alır (listenin tersini yazdırır)
#print(renkler.index("yeşil"))  # 2 parçasını alır (belirli bir öğenin indeksini bulur)

#print(renkler.count("kırmızı"))  # 1 parçasını alır (belirli bir öğenin kaç kez geçtiğini sayar)

#print(sorted(renkler))  # ["kırmızı", "mavi", "sarı", "yeşil"] parçasını alır (listeyi alfabetik olarak sıralar)
#print(sorted(sayi))  # [1, 2, 3, 4, 5] parçasını alır (listeyi küçükten büyüğe sıralar)

#liste2 = renkler.sort()  # listenin öğelerini alfabetik olarak sıralar ve listeyi günceller
#print(renkler)  # ["kırmızı", "mavi", "sarı", "yeşil"] parçasını alır (listeyi yazdırır)
#print(liste2)  # None parçasını alır (sort() metodu listeyi günceller ve None döndürür)
renkler = ["kırmızı", "mavi", "yeşil", "sarı"]
sayi = [2, 3, 1,  4, 5]
#print(renkler[9])  # IndexError: list index out of range hatası verir (listenin 9. öğesi yoktur)
#Listeye öğe ekleme 
#renkler.append("mor")  # listenin sonuna "mor" öğesini ekler
#print(renkler)  # ["kırmızı", "mavi", "yeşil", "sarı", "mor"] parçasını alır (listeyi yazdırır)

#renkler.append(5)  # listenin sonuna 5 öğesini ekler
#print(renkler)  # ["kırmızı", "mavi", "yeşil", "sarı", "mor", 5] parçasını alır (listeyi yazdırır)

#Listeye öğe ekleme (belirli bir indeks)
renkler.insert(2, "turuncu")  # listenin 2. indeksine "turuncu" öğesini ekler
print(renkler)  # ["kırmızı", "mavi", "turuncu", "yeşil", "sarı", "mor"] parçasını alır (listeyi yazdırır)
#Liste öğesini silme (belirli bir indeks)   
del renkler[3]  # listenin 3. indeksindeki öğeyi siler
print(renkler)  # ["kırmızı", "mavi", "turuncu", "sarı", "mor"] parçasını alır (listeyi yazdırır)
del renkler[1:3] #  listenin 1. ve 2. indeksindeki öğeleri siler      
print(renkler)  # ["kırmızı", "sarı", "mor"] parçasını alır (listeyi yazdırır)
