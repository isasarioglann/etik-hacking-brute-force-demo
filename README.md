# etik-hacking-brute-force-demo

# Brute Force Ethical Hacking Tool

benim kayıt yaptığım password:i12 username:isa

## Amaç
Bu uygulama, siber güvenlik dersleri ve etik hacking çalışmalıları kapsamında kullanılmak üzere geliştirilmiştir.
Amaç, öğrenme amaçlı olarak bir brute force (kaba kuvvet) sınıfındaki siber sızma yöntemini anlamak ve test etmektir. Kod, bir HTTP POST formunu hedef alarak kullanıcı adı ve şire listelerini sistematik bir şekilde deneyerek giriş yapmayı dener.

> **Uyarı:** Bu yazılım, sadece izinli test ortamlarında kullanılmalıdır. Etik olmayan kullanım, yasaları çiğnemek anlamına gelebilir ve hukuki yaptırımlara yol açabilir.

## Özellikler
1. **Kullanıcı Adı ve Şifre Listesi Oluşturma**: Belirtilen karakter seti ve uzunluk aralığına göre kullanıcı adı ve şire listeleri oluşturur.
2. **Hedef URL Testi**: Hedef URL'nin erişilebilirliğini kontrol eder.
3. **Brute Force Saldırısı**: Kullanıcı adı ve şire listelerini kullanarak HTTP POST formları üzerinden kaba kuvvet saldırısı dener.
4. **GUI Desteği**: Kullanıcı dostu bir grafik arayüz ile listeler ve saldırı yönetilir.

## Gereksinimler
Bu yazılım Python ile yazılmıştır ve şu kütüphaneleri gerektirir:
- `requests`
- `itertools` (Python standart kütüphanesinin bir parçasıdır)
- `tkinter`
- `threading`
- `time`

Bu kütüphaneler Python 3.x kurulumuyla birlikte gelebilir. `requests` modülü ayrıca yüklenmelidir:
```bash
pip install requests
```

## Nasıl Kullanılır?

### Adım 1: Uygulamaya Genel Bakış
Uygulama iki ana bölümden oluşmaktadır:
- **Kullanıcı Adı ve Şifre Listesi Oluşturma**: Bu bölümde, belirli bir karakter seti ve uzunluğa dayalı olarak şire veya kullanıcı adı listeleri oluşturabilirsiniz.
- **Brute Force Saldırısı**: Hedef URL ve listeler yüklendikten sonra HTTP POST formu üzerinde kaba kuvvet denemesi yapabilirsiniz.

### Adım 2: Kullanıcı Arayüzü (GUI)
#### **1. Kullanıcı Adı ve Şifre Listesi Oluşturma:**
- **Characters**: Listede kullanılacak karakterleri girin (alfabetik, sayısal veya özel karakterler).
- **Minimum ve Maximum Length**: Liste elemanlarının uzunluk aralığını belirtin.
- **Generate Password List**: Şifre listesini oluşturur ve bir dosyaya kaydeder.
- **Generate Username List**: Kullanıcı adı listesini oluşturur ve bir dosyaya kaydeder.

#### **2. Brute Force Saldırısı:**
1. **Target URL**: Saldırı yapılacak hedef URL'yi girin.
2. **Username List File**: Daha önce oluşturduğunuz veya yüklediğiniz kullanıcı adı listesini seçin.
3. **Password List File**: Daha önce oluşturduğunuz veya yüklediğiniz şire listesini seçin.
4. **Start Attack**: "Start Attack" butonuna basarak kaba kuvvet denemesini başlatın.
5. **Attack Output**: Deneme sonuçları burada görülür. Başarılı bir giriş bulunursa bu alanda belirtilir ve bir log dosyasına kaydedilir.

### Adım 3: Erişilebilirlik Testi
Uygulama, hedef URL'ye erişilebilirlik testi yaparak sistemin mevcut olup olmadığını kontrol eder. Test başarılı değilse, saldırı başlatılmaz.

### Adım 4: Saldırı Sonuçlarını Kaydetme
Başarılı bir giriş tespit edilirse sonuçlar, “attack_results_log.txt” dosyasına kaydedilir.

## Kod Mantığı
1. **Listelerin Oluşturulması:**
   - İteratif olarak verilen karakter seti ve uzunluğa göre tüm kombinasyonlar oluşturulur.
   - Dosyaya kayıt edilir.
2. **Hedef URL Testi:**
   - Hedef URL, HTTP GET isteğiyle test edilir.
   - Sunucu yanıtı kontrol edilir.
3. **Kaba Kuvvet Saldırısı:**
   - Kullanıcı adı ve şire listeleri dosyalardan okunur.
   - HTTP POST isteği gönderilir.
   - Yanıt içeriği kontrol edilir. İlgili anahtar kelimeler "Login failed" veya "invalid" var ise başarısız kabul edilir. 302 durum kodu ve belirli bir "Location" header var ise başarılı olarak işaretlenir.

## Etik Kullanım ve Sorumluluk Reddi
Bu uygulama, yalnızca eğitim ve test amaçlı olarak, izinli sistemlerde kullanılmak üzere tasarlanmıştır. İzinsiz kullanımın tespiti halinde tüm yasal sorumluluk, uygulamayı kullanan kişiye aittir.
