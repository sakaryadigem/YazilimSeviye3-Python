#if, elif, else örnekleri içeren bir Python kodu:
#sayi = int(input("Sayı Giriniz: "))  
 
#if sayi > 0:
#    print("Sayı pozitiftir.")   
#elif sayi < 0:
#    print("Sayı negatiftir.") 
#else:
#    print("Sayı sıfırdır.")  
    
a = int(input("Bir sayı giriniz: "))
b = int(input("İkinci sayıyı giriniz: "))
if a > b:
    print(f"{a}, {b} sayısından büyüktür.")  # a, b'den büyüktür. parçasını alır (koşul doğruysa yazdırır)
else:
    print(f"{a}, {b} sayısından küçüktür.")  # a, b'den küçüktür. parçasını alır (koşul doğruysa yazdırır)

if a!= b:
    print(f"{a}, {b} sayısına eşit değildir.")  # a, b'ye eşit değildir. parçasını alır (koşul doğruysa yazdırır)12
else:
    print(f"{a}, {b} sayısına eşittir.")  # a, b'ye eşittir. parçasını alır (koşul doğruysa yazdırır)
    
#cumle = input("Bir kelime veya cümle yazın: ")
#if "a" in cumle:
#    print("Cümle/kelime içinde 'a' harfi vardır.") 
#else:
#    print("Cümle/kelime içinde a harfi yoktur")
    
#if "bulma" in cumle:
#    print("Cümle/kelime içinde 'bulma' kelimesi vardır.") 
#else:
#    print("Cümle/kelime içinde 'bulma' kelimesi yoktur.")  

#a = "Python"
#b = "Pytho"
#b+= "n"
#c = "Python"

#print("a: " + a)
#print("b: " + b)

#if a is b:
#    print("a ve b tam olarak aynı nesnedir.")  
#elif a is c:
#    print("a ve c tam olarak aynı nesnedir.")  
#    if a == b:
#        print("a ve b eşittir.")      
#elif a == b:
#    print("a ve b eşittir.")  
#else:   
#    print("Diğer durum")    
    
#print(id(a))
#print(id(b))