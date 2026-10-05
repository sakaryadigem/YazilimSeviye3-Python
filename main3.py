#örnek metinlerden parça almak için kullanılan bir Python kodu
metin = "Merhaba, bu bir örnek metindir."

parca1 = metin[8:15]  # "bir örnek" parçasını alır
parca2 = metin[:7]    # "Merhaba" parçasını alır
parca3 = metin[16:]   # "metindir." parçasını alır
parca4 = metin[-8:]   # "metindir." parçasını alır (son 8 karakter) 
parca5 = metin[::2]   # "Mra a b rnkmtndr" parçasını alır (her 2. karakter)
parca6 = metin[::-1]  # " .dnitkrem ek örb u ,abahreM" parçasını alır (ters çevirir)
parca7 = metin[5:15:2] # "a a ör" parçasını alır (5. karakterden 15. karaktere kadar her 2. karakter)   
yazi_boyutu = len(metin)  # metin uzunluğunu alır

print("Parça 1: " + parca1)
print("Parça 2: " + parca2)
print("Parça 3: " + parca3)
print("Parça 4: " + parca4)
print("Parça 5: " + parca5)
print("Parça 6: " + parca6)
print("Parça 7: " + parca7)
print("Yazı Boyutu: " + str(yazi_boyutu))

print(metin.upper())  # "MERHABA, BU BİR ÖRNEK METINDIR." parçasını alır (tüm karakterleri büyük harfe çevirir)
print(metin.lower())  # "merhaba, bu bir örnek metindir." parçasını alır (tüm karakterleri küçük harfe çevirir)
print(metin.replace("örnek", "deneme"))  # "Merhaba, bu bir deneme metindir." parçasını alır (belirli bir kelimeyi değiştirir)
print(metin.find("örnek"))  # 14 parçasını alır (belirli bir kelimenin başlangıç indeksini bulur)
print(metin.count("e"))  # 3 parçasını alır (belirli bir karakterin kaç kez geçtiğini sayar)
print(metin.title())  # "Merhaba, Bu Bir Örnek Metindir." parçasını alır (her kelimenin ilk harfini büyük yapar)

