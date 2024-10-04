# datamatrix
Webcam ile Data Matrix Kodu Girişi ve Sonuçları
Bu proje, Data Matrix kodlarını tarayarak her kod için bir tanım girişi yapılmasını sağlar. Pozitif/negatif sonuçlar ve ek bilgiler girildikten sonra bu sonuçlar kaydedilir ve clipboard'a kopyalanabilir. Program, sürekli olarak kameradan gelen görüntüleri tarar ve bir kod algıladığında gerekli giriş işlemlerini sağlar.

## Özellikler
- Data Matrix kodlarını kameradan tarar.
- Tanımlı olmayan kodlar için tanım girişi yapar ve kalıcı olarak `codes_memory.txt` dosyasına kaydeder.
- Pozitif/Negatif butonları ile sonuç girilir, ek bilgiler de eklenebilir.
- Tüm sonuçlar clipboard'a kopyalanabilir.
- "Hasta Yenile" butonu ile yeni hasta için sonuçlar sıfırlanır.
- Butonlar farklı renkte olup, kullanıcı dostu bir arayüz sunar.

## Gereksinimler

Aşağıdaki Python kütüphanelerinin kurulmuş olması gerekmektedir:

- `opencv-python`
- `pylibdmtx`
- `tkinter` (Python ile birlikte gelir)
- `pyperclip`
- `winsound` (Windows işletim sistemi için)

Kütüphaneleri kurmak için aşağıdaki komutu kullanabilirsiniz:

```bash
pip install opencv-python pylibdmtx pyperclip
```

## Kullanım

1. **Kamerayı Başlat**: Programı çalıştırdığınızda, kamera açılır ve sürekli olarak Data Matrix kodlarını tarar.

2. **Kod Tanımlama**: İlk kez bir kod tarandığında, program sizden bu kod için bir tanım girmenizi ister. Girdiğiniz tanım, kalıcı olarak `codes_memory.txt` dosyasına kaydedilir.

3. **Sonuç Girişi**: Her kod için "Pozitif", "Negatif" butonları ve ek sonuç girişi yapılabilir. Bu girişler sonucu programda listelenir.

4. **Sonuçları Kopyala**: Ana penceredeki "Kopyala" butonuna basarak tüm sonuçları clipboard'a kopyalayabilirsiniz.

5. **Hasta Yenile**: "Hasta Yenile" butonuna basarak tüm sonuçları sıfırlayabilir ve yeni bir hasta için giriş yapabilirsiniz.

## Dosyalar

- **datamatrix.py**: Ana Python dosyası, kodların taranmasını ve sonucun alınmasını sağlar.
- **codes_memory.txt**: Taranan her kod için girilen tanımları kalıcı olarak saklar.
- **datamatrix3.py**: Bu güncellenmiş kod, artık webcam kullanmadan COM4 portundan gelen barkod ve data matrix kodlarını işler. codes_memory.txt dosyasını kullanarak kodları ve tanımlarını yönetir. Program, COM4 portundan gelen kodları otomatik olarak alır ve arayüzde ilgili işlemleri gerçekleştirir.

## geliştirme
Agilent immunhistokimya preparat etiketlerinde matrix kodları var. Her etiketin farklı kodu olduğu için kullanılabilir değil. Aynı antikora ait tüm preparatlar benzersiz farklı kodlarda. Proje bu nedenle askıda.
