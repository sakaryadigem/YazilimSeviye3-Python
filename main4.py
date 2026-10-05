#mantıksal operatörler and, or, not
a = 5   
b = 10
c = 15

if a < b and b > c:
    print("a, b'den küçük ve b, c'den küçüktür.")  # a, b'den küçük ve b, c'den küçüktür. parçasını alır (koşul doğruysa yazdırır)  
else:
    print("Koşul 1 sağlanmadı.")  # Koşul sağlanmadı. parçasını alır (koşul yanlışsa yazdırır)

if a > b or b > c:
    print("a, b'den küçüktür veya b, c'den büyüktür.")  # a, b'den küçüktür veya b, c'den büyüktür. parçasını alır (koşul doğruysa yazdırır)
else:
    print("Koşul 2 sağlanmadı.")  # Koşul sağlanmadı. parçasını alır (koşul yanlışsa yazdırır)
    
if not (a < b):
    print("a, b'den büyük değildir.")  # a, b'den büyük değildir. parçasını alır (koşul doğruysa yazdırır)
else:
    print("Koşul 3 sağlanmadı.")  # Koşul sağlanmadı. parçasını alır (koşul yanlışsa yazdırır)





#hava güneşli ise güneş gözlüğü taksın [hava güneşli]

hava_gunesli_mi = True  # Havanın güneşli olduğunu varsayalım
if hava_gunesli_mi:
    print("Hava Güneşli: Güneş gözlüğü tak.")  # Güneş gözlüğü tak. parçasını alır (koşul doğruysa yazdırır)

#hava yağmurlu ise şemsiye alsın [hava yağmurlu]
hava_yagmurlu_mu = False  # Havanın yağmurlu olduğunu varsayalım
if hava_yagmurlu_mu:
    print("Hava Yağmurlu: Şemsiye alsın.")  # Şemsiye alsın. parçasını alır (koşul doğruysa yazdırır)

#hava yağmurlu veya güneşli ise şapka taksın [hava yağmurlu veya güneşli]
hava_yagmurlu_mu = False  # Havanın yağmurlu olduğunu varsayalım
hava_gunesli_mi = True  # Havanın güneşli olduğunu varsayalım
if hava_yagmurlu_mu or hava_gunesli_mi:
    print("Hava Yağmurlu veya Güneşli: Şapka taksın.")  # Şapka taksın. parçasını alır (koşul doğruysa yazdırır)

#hava yağmurlu ve rüzgarlı ise evde kalsın [yağmurlu ve rüzgarlı]
hava_yagmurlu_mu = True  # Havanın yağmurlu olduğunu varsayalım
hava_ruzgarlı_mi = True  # Havanın rüzgarlı olduğunu varsayalım
if hava_yagmurlu_mu and hava_ruzgarlı_mi:
    print("Hava Yağmurlu ve Rüzgarlı: Evde kalsın.")  # Evde kalsın. parçasını alır (koşul doğruysa yazdırır)
    
#hava güneşli değil ise denize gitmesin [hava güneşli değil]
hava_gunesli_mi = False  # Havanın güneşli olmadığını varsayalım
if not hava_gunesli_mi:
    print("Hava Güneşli Değil: Denize gitmesin.")  # Denize gitmesin. parçasını alır (koşul doğruysa yazdırır)
    