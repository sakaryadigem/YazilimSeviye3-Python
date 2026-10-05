#döngüleri içeren örnek bir Python kodu:
#for döngüsü ile 1'den 10'a kadar olan sayıları yazdır

sayilar = [1, 3, 6, 8, 9]
#for rakam in sayilar:   
#    print(rakam)

cumle = "Ali ata bak"
#for i in cumle:
#    print(i)
    
#for rakam in sayilar:  
#    for harf in cumle:
#        print(rakam, harf)

#i = 0
#while i < 10:
#    i += 1
#    print(i)

#for i in range(1, 11):
#    print(i)

#for i in range(10): # range(0, 10)
#    print(i)

sonuc = 0
#for i in range(15):
    #sonuc+=i+2*i
    #print(sonuc)
#print(sonuc)
    
#print(list(range(1, 11)))  # range(1, 11) parçasını alır (range nesnesini yazdırır)
#print(set(range(1, 11)))  # set(range(1, 11)) parçasını alır (range nesnesini küme olarak yazdırır)

liste = range(100)
dur = input("0 dan 100 e kadar bir sayı Giriniz: ")

for i in liste:
    if i % 3 != 0:
        continue
    if i > int(dur):
        break
    print(i)